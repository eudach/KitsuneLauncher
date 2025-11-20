from typing import Literal
import flet as ft

from ui.resources.Fonts import BaseFonts

class DropdownLenguage:
    def __init__(self, page):
        self.page = page
        self.dropdown = ft.DropdownM2(
            label=page.t('lenguaje_dropdown'),
            hint_text=page.t('lenguaje_dropdown_description'),
            value=page.launcher.config.get("language"),
            options=[
                ft.dropdownm2.Option(key="es", content=ft.Text("Español")),
                ft.dropdownm2.Option(key="en", content=ft.Text("English")),
            ],
            focused_color='white',
            border="underline",
            border_color=ft.Colors.TRANSPARENT,
            fill_color=ft.Colors.TRANSPARENT,
            bgcolor=ft.Colors.BLACK87,
            border_radius=3,
            label_style=ft.TextStyle(
                color=ft.Colors.WHITE,
                font_family=BaseFonts.texts,
                size=page.window.width * 0.02,
            ),
        )

    def get(self):
        return self.dropdown
    
class DropdownVersions:
    def __init__(self, page, select_ver, tooltip_installation_needed):
        self.page = page
        self.dropdown_versions = ft.DropdownM2(
            col=4,
            label=page.t('versions_dropdown_label'),
            item_height=50,
            value=f"{page.launcher.last_played_version[0]}",
            max_menu_height=page.window.height/2,
            hint_text=page.t('versions_dropdown'),
            options=[
                ft.dropdownm2.Option(key=e[0], data=e, content=
                    ft.Row(controls=
                        [   
                            ft.Image(src="iconos/minecraft.png" if not e[1] else "iconos/icono.png", width=30, height=30),
                            ft.Text(value=e[0], font_family=BaseFonts.texts, size=page.window.width*0.011, tooltip=tooltip_installation_needed if not e[1] else None )
                            
                        ], alignment=ft.MainAxisAlignment.START
                    ),
                    on_click=select_ver
                ) for e in page.launcher.versions
            ],
            width=page.window.width*0.35,
            focused_color='white',
            border="underline",
            border_color=ft.Colors.TRANSPARENT,
            fill_color=ft.Colors.WHITE10,
            bgcolor=ft.Colors.BLACK87,
            border_radius=3,
            label_style=ft.TextStyle(color=ft.Colors.WHITE, font_family=BaseFonts.texts, size=page.window.width*0.02)
        )
        
    def get(self):
        return self.dropdown_versions
    
class DropdownLimitSearch:
    
    def __init__(self, page, change_limit_research_mod):
        self.page = page
        
        self.dropdown_limit_search = ft.DropdownM2(
            label=page.t('limit_search'),
            width=page.window.width/10,
            value=10,
            options=[
                ft.dropdownm2.Option(key=10, content=
                    ft.Text("10")
                ),
                ft.dropdownm2.Option(key=20, content=
                    ft.Text("20")
                ),
                ft.dropdownm2.Option(key=30, content=
                    ft.Text("30")
                ),
                ft.dropdownm2.Option(key=40, content=
                    ft.Text("40")
                ),
                ft.dropdownm2.Option(key=50, content=
                    ft.Text("50")
                )
                
            ],
            focused_color='white',
            border="underline",
            border_color=ft.Colors.TRANSPARENT,
            fill_color=ft.Colors.TRANSPARENT,
            bgcolor=ft.Colors.WHITE30,
            on_change=change_limit_research_mod,
            border_radius=3,
            label_style=ft.TextStyle(color=ft.Colors.WHITE, font_family=BaseFonts.texts, size=page.window.width*0.02)
        )
    
    def get(self):
        return self.dropdown_limit_search
    
class DropdownLoaders:
    
    def __init__(self, page, change_loader_mod):
        self.page = page
        
        self.dropdown_loaders = ft.DropdownM2(
            label=page.t('loaders'),
            width=page.window.width/10,
            options=[
            ],
            focused_color='white',
            border="underline",
            border_color=ft.Colors.TRANSPARENT,
            fill_color=ft.Colors.TRANSPARENT,
            bgcolor=ft.Colors.WHITE30,
            on_change=change_loader_mod,
            border_radius=3,
            label_style=ft.TextStyle(color=ft.Colors.WHITE, font_family=BaseFonts.texts, size=page.window.width*0.02)
        )
        
        self.update("mod")
        
    def update(self, project_type: Literal["mod", "resourcepack", "shader", "plugin", "datapack"]):
        self.dropdown_loaders.visible = True
        warps_loaders = {
            "mod": ["Forge", "Fabric", "NeoForge", "Quilt"],
            "modpack": ["Forge", "Fabric", "NeoForge", "Quilt"],
            "plugin": ["Bukkit", "Spigot", "Paper", "Purpur", "Sponge", "Folia"],
            "shader": ["Canvas", "Iris", "Optifine", "Vanilla"],
            "resourcepack": [],
            "datapack": []
        }

        if project_type not in warps_loaders:
            self.dropdown_loaders.visible = False
            return

        loaders = warps_loaders[project_type]

        if not loaders:
            self.dropdown_loaders.visible = False
            self.dropdown_loaders.value = None
            return

        self.dropdown_loaders.options.clear()
        for e in loaders:
            self.dropdown_loaders.options.append(
                ft.dropdownm2.Option(key=e, content=ft.Text(e))
            )

        self.dropdown_loaders.value = self.dropdown_loaders.options[0].key
        
    def get(self):
        return self.dropdown_loaders