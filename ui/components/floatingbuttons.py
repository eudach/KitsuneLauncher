from typing import List, Literal
import flet as ft

from ui.components.button import ButtonRefreshModsLocal, ButtonOpenFolder
from ui.components.container import ContainerLocal
from ui.resources.Fonts import BaseFonts


class SearchButtonsNavigation:
    def __init__(self, page: ft.Page, modrinth_instance):
        self.page = page
        self.modrinth_instance = modrinth_instance
        self.page.views[0].floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_FLOAT

    # ------------------------------
    async def reload_local(self, e):
        """Recarga la lista de mods locales"""
        self.promt_list_mods = self.page.launcher.get_list_mods()
        self.containers_mods_local.reload()
        self.total_local_mods.value = f"{self.page.t('total_mods_loaded')}: {len(self.promt_list_mods)}"
        self.list_installed_mods.scroll_to(offset=0, duration=300)
        self.list_installed_mods.update()
    
    def buid_section_installed(self, section: Literal["mod", "resourcepack", "shader"], update:bool=True):
        
        warp_sections = {
            "mod": 0,
            "resourcepack": 1,
            "shader": 2
        }
        
        get_funcs = {
            "mod": self.page.launcher.get_list_mods,
            "resourcepack": self.page.launcher.get_list_resourcepacks,
            "shader": self.page.launcher.get_list_shaderpacks,
        }
        
        lista = get_funcs[section]()
        self.page.global_vars["project_type"] = section

        cache = [path.path for path in lista]
        self.page.temp_config_modrinth["list_mods_cache_installed"] = cache
        self.page.temp_config_modrinth["mods_index_installed"] = {p: i for i, p in enumerate(cache)}

        container_local = ContainerLocal(
            page=self.page,
            on_click=self.modrinth_instance.get_description_installed,
            data_list=lista,
            tipo=section
        )

        # 4️⃣ Crear lista visual
        list_view = ft.ListView(
            controls=container_local.get(),
            spacing=5,
            padding=ft.Padding(5, 5, 5, 5),
            expand=True
        )
        
        # 3️⃣ Texto total
        texto_map = {
            "mod": self.page.t("total_mods_loaded"),
            "resourcepack": "Resourcepacks total",
            "shader": "Shaderpacks total",
        }
        texto_total = ft.Text(
            selectable=True,
            value=f"{texto_map[section]}: {len(lista)}",
            font_family=BaseFonts.texts,
            size=self.page.window.width / 70,
        )
        
        self.tabs_sections.tabs[warp_sections[section]].content.controls = [
                texto_total,
                list_view
            ]
        
        self.dialog.actions = [
            ButtonRefreshModsLocal(page=self.page, on_click=self.reload_local).get(),
            ButtonOpenFolder(page=self.page, type=section).get()
        ]
        
        if update:
            self.page.update()
    
    async def change_section_installed(self, e):
        
        if e.data == "0":
            return self.buid_section_installed("mod")
            
        if e.data == "1":
            return self.buid_section_installed("resourcepack")
            
        if e.data == "2":
            return self.buid_section_installed("shader")

    # ------------------------------
    def __open_generic_installed(self, tipo: Literal["mod", "resourcepack", "shader"]):
        """Abre un diálogo genérico para mods/resourcepacks/shaderpacks"""

        self.tabs_sections = ft.Tabs(
            label_color=self.page.global_vars["primary_color"],
            indicator_color=self.page.global_vars["primary_color"],
            tab_alignment=ft.TabAlignment.FILL,
            scrollable=False,
            
            on_click=self.change_section_installed,
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    icon=ft.Container(
                        width=25,
                        height=25,
                        alignment=ft.alignment.center,
                        content=ft.Image(
                            src="iconos/foxy.png",
                            fit=ft.ImageFit.FILL
                        )
                    ),
                    tab_content=ft.Text(value="Mods", size=self.page.window.width/70, font_family=BaseFonts.buttons),
                    content=ft.Column(
                        controls=[
                        ],
                        expand=True
                    )
                ),
                
                ft.Tab(
                    icon=ft.Container(
                        width=25,
                        height=25,
                        alignment=ft.alignment.center,
                        content=ft.Image(
                            src="iconos/paint.png",
                            fit=ft.ImageFit.FILL
                        )
                    ),
                    tab_content=ft.Text(value="Resource Packs", size=self.page.window.width/70, font_family=BaseFonts.buttons),
                    content=ft.Column(
                        controls=[
                        ],
                        expand=True
                    )
                ),
                
                ft.Tab(
                    icon=ft.Container(
                        width=30,
                        height=30,
                        alignment=ft.alignment.center,
                        content=ft.Image(
                            src="iconos/shaders.gif",
                            fit=ft.ImageFit.FILL
                        )
                    ),
                    tab_content=ft.Text(value="Shader Packs", size=self.page.window.width/70, font_family=BaseFonts.buttons),
                    content=ft.Column(
                        controls=[
                        ],
                        expand=True
                    )
                )
            ],
            expand=True
        )
        
        
        # 6️⃣ Crear y abrir diálogo
        self.dialog = ft.AlertDialog(
            inset_padding=20,
            content_padding=0,
            actions_padding=10,
            title_padding=0,
            icon_padding=ft.Padding(left=5, right=5, top=5, bottom=0),
            icon=ft.Container(
                content=ft.Row(controls=[
                    ft.Row(expand=True),
                    ft.Text(value=self.page.t("local_downloaded"), size=self.page.window.width/50, font_family=BaseFonts.titles),
                    ft.Row(expand=True),
                    ft.IconButton(icon=ft.Icons.CLOSE, icon_color=self.page.global_vars["primary_color"], on_click=self.page.close_alert)
                ],
                alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                #bgcolor=ft.Colors.
            ),
            shape=ft.BeveledRectangleBorder(5),
            bgcolor=ft.Colors.BLACK,
            content=ft.Container(
                padding=ft.Padding(left=5, right=5, top=5, bottom=5),
                content=ft.Column(
                    controls=[
                        self.tabs_sections
                    ],
                    expand=True,
                ),
                width=self.page.window.width / 1,
                height=self.page.window.height / 1,
                #bgcolor=ft.Colors.WHITE10,
            ),
            action_button_padding=0,
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        self.buid_section_installed(tipo, False)
        
        self.page.open(self.dialog)

    # ------------------------------
    def build(self, button_back, button_home, button_next):
        """Construye el menú inferior"""
        self.page.views[0].floating_action_button = ft.Row(
            controls=[
                button_back,
                button_home,
                button_next,
                ft.PopupMenuButton(
                    visible=True,
                    style=ft.ButtonStyle(
                        bgcolor=self.page.global_vars["primary_color"], shape=ft.RoundedRectangleBorder(radius=5)
                    ),
                    splash_radius=5,
                    icon_color=ft.Colors.WHITE,
                    icon=ft.Icons.FORMAT_LIST_BULLETED,
                    bgcolor=ft.Colors.BLACK87,
                    items=[
                        ft.PopupMenuItem(
                            content=ft.Row(
                                controls=[
                                    ft.Image(src="iconos/files.png", width=20, height=20),
                                    ft.Text(value="Instalados"),
                                ]
                            ),
                            on_click=lambda e: self.__open_generic_installed("mod"),
                        ),
                    ],
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def update(self):
        ...
