import flet as ft

from ui.components.button import ButtonDeleteAll, ButtonSave
from ui.components.dropdown import DropdownLenguage
from ui.components.color_picker import ColorPicker

from core.utils import generar_degradado, alerta, TYPES_COLORS

from ui.components.input import InputJavaPath, InputMinecraftPath
from ui.components.slider import SliderOpacity, SliderRam
from ui.components.iconbutton import (IconButtonWallpaper,IconButtonJavaPath, IconButtonMcPath)

class Settings:
    def __init__(self, page, select_ver):
        self.page = page
        self.select_ver = select_ver
        
    async def reload_all_versions(self):
        page = self.page
        page.dropdown_versions.value = None
        page.dropdown_versions.options=[
            ft.dropdownm2.Option(key=e[0], data=e, content=
                ft.Row(controls=
                    [   
                        ft.Image(src="mc_icon.png" if not e[1] else "icono.png", width=30, height=30),
                        ft.Text(value=e[0], font_family='liberation', size=page.ancho*0.011, tooltip=page.tooltip_installation_needed if not e[1] else None )
                        
                    ], alignment=ft.MainAxisAlignment.START
                ),
                on_click=self.select_ver
            ) for e in page.launcher.versions
        ]
        page.dropdown_versions.update()
        
    async def change_thema_on_time(self):
        page = self.page
        prim = page.launcher.config.get("primary_color_schema")
        light = page.launcher.config.get("light_color_schema")
        dark = page.launcher.config.get("dark_color_schema")
        page.color_init = prim
        color_map = [
            ("iconbutton_wallpaper", "icon_color", prim),
            ("iconbutton_java_path", "icon_color", prim),
            ("iconbutton_mc_path", "icon_color", prim),
            ("input_java_path", "cursor_color", prim),
            ("input_minecraft_path", "cursor_color", prim),
            ("slider_ram", "active_color", prim),
            ("slider_opacity", "active_color", prim),
            ("discord_presence_allow", "active_color", prim),
            ("discord_presence_allow", "inactive_track_color", light),
            ("discord_presence_allow", "inactive_thumb_color", dark),
            ("container_wallpaper", "bgcolor", prim)
        ]

        for attr, prop, value in color_map:
            control = getattr(self, attr, None)  # Busca el control en page
            if control and hasattr(control, prop):
                setattr(control, prop, value)

        if hasattr(page, "progress_bar"):
            page.progress_bar.color = prim
        if hasattr(page, "content_menu"):
            page.content_menu.border = ft.border.all(1, prim)
            
        page.button_play.bgcolor = prim
        page.borderside_sections.color = prim
        page.iconbutton_console.icon_color = prim
        page.update()

    
    async def change_language_on_time(self):
        page = self.page

        translation_map = [
            ("input_java_path", "label", "java_path_"),
            ("dropdown_language", "label", "lenguaje_dropdown"),
            ("input_minecraft_path", "label", "mc_path_"),
            ("dropdown_versions", "label", "versions_dropdown_label"),
            ("dropdown_versions", "hint_text", "versions_dropdown"),
            ("text_discord_rich", "value", "discord_rich"),
            ("text_opacity", "value", "opacity"),
            ("text_ram", "value", "ram_usage"),
            ("text_wallpaper", "value", "wallpaper_save"),
            ("text_save", "value", "save_"),
            ("text_delete_all", "value", "delete_all_"),
            ("text_play", "value", "play_button"),
            ("text_color_picker", "value", "color_picker_text"),
            ("tooltip_installation_needed", "message", "installation_needed"),
        ]

        for attr, prop, key in translation_map:
            control = getattr(self, attr, None)  # Busca el control en page
            if control and hasattr(control, prop):
                setattr(control, prop, page.t(key))

        for attr, prop, key in [
            ("home_button", "text", "sections_main"),
            ("settings_button", "text", "sections_settings"),
            ("perfil_button", "text", "sections_profile"),
            ]:
            control = getattr(page, attr, None)  # Busca el control en page
            if control and hasattr(control, prop):
                setattr(control, prop, page.t(key))
        
        page.update()
    
    async def change_wallaper_presets(self, e):
        page = self.page
        page.launcher.config.set("wallpaper_launcher", e.control.data)
        
        page.views[0].decoration.image.src = e.control.data
        self.image_wallpaper_widget.src = e.control.data
        
        self.image_wallpaper_widget.update()
        page.views[0].update()
        
        page.launcher.config.save()
    
    async def save_settings(self, e):
        page = self.page
        changes_ = []
        #OPACITY
        
        if page.launcher.config.get("opacity") != round(self.slider_opacity.value):
            opacity_value = round(self.slider_opacity.value)
            color = TYPES_COLORS[opacity_value]

            # Mapeo: (atributo de page, propiedad, valor)
            updates = [
                ("content_menu", "bgcolor", color[2]),
                ("content_sidebar", "bgcolor", color[2]),
                ("slider_opacity", "inactive_color", color[0]),
                ("slider_ram", "inactive_color", color[0]),
                ("home_button", "style.bgcolor", "transparent"),
                ("perfil_button", "style.bgcolor", "transparent"),
                ("settings_button", "style.bgcolor", "transparent"),
            ]

            # Appbar y sections de la vista principal
            if page.views and len(page.views) > 0:
                page.views[0].appbar.bgcolor = color[1]
            page.content_sections.bgcolor = color[1]

            # Aplicar actualizaciones
            for attr, prop, value in updates:
                control = getattr(page, attr, None)
                if control:
                    if "." in prop:  # para casos como "style.bgcolor"
                        obj, subprop = prop.split(".")
                        if hasattr(control, obj):
                            setattr(getattr(control, obj), subprop, value)
                    else:
                        setattr(control, prop, value)

            page.update()
            changes_.append("Opacity")
            page.launcher.config.set("opacity", opacity_value)

        #JAVA PATH
        if not page.launcher.set_java(self.input_java_path.value, False):
            page.open(
                alerta(
                    titulo= "Error",
                    descripcion= page.t("file_not_found")
                )
            )
            return

        if page.launcher.java_path != self.input_java_path.value:
            page.launcher.set_java(self.input_java_path.value)
            changes_.append("Java dir")
        
        #MINECRAFT PATH
        if self.input_minecraft_path.value != page.launcher.minecraft_path:
            page.launcher.set_minecraft_path(self.input_minecraft_path.value)
            changes_.append("Minecraft dir")
            
            page.run_task(self.reload_all_versions)
        
        #RAM
        if page.launcher.config.get("ram") != round(self.slider_ram.value):
            page.launcher.config.set("ram", round(self.slider_ram.value))
            changes_.append("Ram")
        
        #DISCORD
        if page.launcher.config.get("discord_presence") != self.discord_presence_allow.value:
            page.launcher.config.set("discord_presence", self.discord_presence_allow.value) 
            changes_.append("Discord")
            
            if page.launcher.config.get("discord_presence"):
                page.presence.update()
            else:
                page.presence.clear()
        
        #WALLPAPER
        if page.launcher.config.get("wallpaper_launcher") != self.image_wallpaper_widget.src:
            page.launcher.config.set("wallpaper_launcher", self.image_wallpaper_widget.src)
            
            page.views[0].decoration.image.src = self.image_wallpaper_widget.src
            page.views[0].update()
            changes_.append("Wallpaper")
        
        #COLOR PICKER
        if page.launcher.config.get("primary_color_schema") != self.color_picker.color_displayed:
            degrados = generar_degradado(self.color_picker.color_displayed)
            
            page.launcher.config.set("primary_color_schema", self.color_picker.color_displayed)
            page.launcher.config.set("light_color_schema", degrados[1])
            page.launcher.config.set("dark_color_schema", degrados[0])
            
            page.run_task(self.change_thema_on_time)
            
            changes_.append("Thema")
        
        #LENGUAJE
        if page.launcher.config.get("language") != self.dropdown_language.value:
            page.launcher.config.set("language", self.dropdown_language.value)
            changes_.append("Language")
            
            page.run_task(self.change_language_on_time)
        
        #SAVE
        if len(changes_) == 0:
            return
        
        page.launcher.config.save()

        page.open(
            alerta(
                titulo= page.t("settings_saved"),
                descripcion= f"{page.t('setting_saved_description')}:\n {','.join(changes_)}",
                success=True
                )
            )
    
    async def show_list_wallpaper(self, e):
        page = self.page
        self.page.open(
            ft.AlertDialog(
                bgcolor=ft.Colors.BLACK87,
                open=True,
                content=ft.Row(
                    wrap=True,
                    spacing=100,
                    run_spacing=50,
                    controls=[
                        ft.Container(
                            content=ft.Image(
                                src=f"imgs/wallpaper{e}.gif",
                                width=page.ancho*0.10,
                                height=page.alto*0.10,
                                border_radius=10,
                                fit=ft.ImageFit.FILL
                                
                            ),
                            ink=True,
                            on_click=self.change_wallaper_presets,
                            data=f"imgs/wallpaper{e}.gif",
                            border_radius=10,
                            padding=1,
                            bgcolor=page.color_init
                        )
                    for e in range(1, 9)
                    ],
                expand=True
                )
            )
        )
    
    async def clr_data_modal(self, e):
        page = self.page
        page.launcher.config.reset()
        page.window.close()
    
    async def delte_all_data(self, e):
        page = self.page
        
        alrt = ft.AlertDialog(
            icon=ft.Icon(name=ft.Icons.WARNING_AMBER),
            title=ft.Text(value=page.t("data_elimination"), text_align=ft.TextAlign.CENTER),
            content=ft.Text(value=page.t("data_elimination_sure"), text_align=ft.TextAlign.CENTER),
            actions=[
                ft.TextButton(
                    text=page.t("data_question_y"),
                    on_click=self.clr_data_modal,
                    style=ft.ButtonStyle(
                        color=page.color_init
                    )
                ),
                ft.TextButton(
                    text="No",
                    style=ft.ButtonStyle(
                        color=page.color_init
                    ),
                    on_click=lambda e: page.close(alrt)
                ),
            ],
            bgcolor=ft.Colors.BLACK,
            shape=ft.BeveledRectangleBorder(3),
            icon_color=page.color_init,
            alignment=ft.alignment.center,
        )
        page.open(
            alrt
        )
        
    async def ram_change_function(self, e):
        page = self.page
        self.text_ram.value = f"{round(self.slider_ram.value)} GB"
        self.text_ram.update()
        
    async def filepicker_select_bin_javaw(self, e:ft.FilePickerResultEvent):
        page = self.page
        if e.files is None:
            return
        
        self.input_java_path.value = e.files[0].path
        self.input_java_path.update()
        
    async def filepicker_select_minecraft_path(self, e:ft.FilePickerResultEvent):
        page = self.page
        if not e.path:
            return

        self.input_minecraft_path.value = e.path
        self.input_minecraft_path.update()
        
    async def select_img_wallpaper(self, e:ft.FilePickerResultEvent):
        page = self.page
        if e.files is None:
            return
        
        #page.wallpaper_launcher = e.files[0].path
        self.image_wallpaper_widget.src = e.files[0].path
        
        self.image_wallpaper_widget.update()
    
    async def bttn_img_wallpaper(self, e):
        self.filepicker_wallapaper.pick_files(
            self.page.t('select_img_wallpaper'),
            allowed_extensions=["jpg", "png", "jpeg", "gif"]
        )
    
    async def bttn_check_minecraft_path(self, e):
        self.filepicker_minecraft_path.get_directory_path(
            dialog_title="Select new .miecraft",
            initial_directory=self.page.launcher.return_appdata()
        )
        
    async def bttn_select_java_bin(self, e):
        self.filepicker_javaw.pick_files(
            f"{self.page.t('select_javaw')} javaw.exe",
            allowed_extensions=["exe"]
        )

    async def load(self):
        page:ft.Page = self.page
        page.current_section = 'settings'
        page.content_menu.alignment= ft.alignment.top_left
        
        self.text_save = ft.Text(
            value=page.t('save_'),
            font_family="lokeya",
            size=page.ancho/60,
            text_align=ft.TextAlign.CENTER
        )
        self.text_delete_all = ft.Text(
            value=page.t('delete_all_'),
            font_family="lokeya",
            size=page.ancho/60,
            text_align=ft.TextAlign.CENTER
        )
        self.text_ram = ft.Text(
            value=page.t('ram_usage'),
            max_lines=2, size=page.ancho/70,
            text_align=ft.TextAlign.CENTER,
            font_family="liberation"
        )
        self.text_opacity = ft.Text(
            value=page.t('opacity'),
            max_lines=2, size=page.ancho/70,
            text_align=ft.TextAlign.CENTER,
            font_family="liberation"
        )
        
        self.discord_presence_allow = ft.Switch(
            value=page.launcher.config.get("discord_presence"),
            active_color=page.color_init,
            track_color=page.launcher.config.get("dark_color_schema"),
            thumb_color=page.launcher.config.get("light_color_schema"),
            track_outline_color='transparent',
            inactive_track_color=page.launcher.config.get("dark_color_schema"),
            inactive_thumb_color=page.launcher.config.get("light_color_schema")
        )
        self.image_wallpaper_widget = ft.Image(
            src=page.launcher.config.get("wallpaper_launcher", page.default_wallpaper),
            width=page.ancho*0.10,
            height=page.alto*0.10,
            border_radius=10,
            fit=ft.ImageFit.FILL
        )
        self.text_discord_rich = ft.Text(
            value = page.t('discord_rich'),
            max_lines=2, size=page.ancho/70,
            text_align=ft.TextAlign.CENTER,
            font_family="liberation"
        )
        self.text_wallpaper = ft.Text(
            value=page.t('wallpaper_save'),
            max_lines=2, size=page.ancho/70,
            text_align=ft.TextAlign.CENTER,
            font_family="liberation"
        )
        
        self.color_picker = ColorPicker(color=page.color_init, width=page.ancho/4, height=page.alto/4)
        self.text_color_picker = ft.Text(
            value=page.t('color_picker_text'),
            max_lines=2, size=page.ancho/60,
            text_align=ft.TextAlign.CENTER,
            font_family="liberation"
        )
        
        button_save = ButtonSave(page, self.text_save, self.save_settings).get()
        button_delete_all = ButtonDeleteAll(page, self.text_delete_all , self.delte_all_data).get()
        self.slider_opacity = SliderOpacity(page).get()
        self.slider_ram = SliderRam(page, self.ram_change_function).get()
        
        self.filepicker_wallapaper = ft.FilePicker(on_result=self.select_img_wallpaper)
        self.filepicker_javaw = ft.FilePicker(on_result=self.filepicker_select_bin_javaw)
        self.filepicker_minecraft_path = ft.FilePicker(on_result=self.filepicker_select_minecraft_path)
        
        self.iconbutton_wallpaper = IconButtonWallpaper(page, self.bttn_img_wallpaper).get()
        self.iconbutton_java_path = IconButtonJavaPath(page, self.bttn_select_java_bin).get()
        self.iconbutton_mc_path = IconButtonMcPath(page, self.bttn_check_minecraft_path).get()
        
        self.input_java_path = InputJavaPath(page, self.iconbutton_java_path).get()
        self.input_minecraft_path = InputMinecraftPath(page, self.iconbutton_mc_path).get()
        self.dropdown_language = DropdownLenguage(page).get()
        
        page.overlay.append(self.filepicker_javaw)
        page.overlay.append(self.filepicker_minecraft_path)
        page.overlay.append(self.filepicker_wallapaper)
        
        self.container_wallpaper = ft.Container(
            content=self.image_wallpaper_widget,
            padding=1, ink=True,
            border_radius=10,
            bgcolor=page.color_init,
            on_click=self.show_list_wallpaper
        )
        
        page.content_menu.content= ft.Column(
            controls=[
                
                ft.Container(expand=9, padding=5, content=
                    ft.ResponsiveRow(columns=14,
                        spacing=5, run_spacing=5,
                        controls=[
                            ft.Column(controls=
                                [
                                ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, content=self.input_java_path, margin=0),
                                ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, content=self.input_minecraft_path, margin=0),
                                ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, content=self.dropdown_language, margin=0),
                                ft.Container(border=ft.border.all(2, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, padding=5, content=
                                    ft.Column(
                                        controls=[
                                            self.text_ram,
                                            self.slider_ram,
                                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, 
                                    ), margin=0
                                ),
                                ],
                                col=4, 
                                spacing=5,
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            ft.Column(
                                controls=
                                    [
                                        ft.Container(border=ft.border.all(1, ft.Colors.BLACK), padding=10, bgcolor=ft.Colors.WHITE10, content=
                                            ft.Column(
                                                controls=[
                                                    self.text_discord_rich,
                                                    self.discord_presence_allow
                                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER
                                            ), margin=0, alignment=ft.alignment.center
                                        ),
                                        ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, padding=10, margin=0, content=ft.Column(
                                            controls=[
                                                self.text_wallpaper,
                                                ft.Row(controls=
                                                    [
                                                        self.container_wallpaper,
                                                        self.iconbutton_wallpaper
                                                        ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER
                                                    ),
                                                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                            )
                                        ),
                                        ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, padding=10, margin=0, content=ft.Column(
                                            controls=[
                                                self.text_opacity,
                                                self.slider_opacity
                                                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                            )
                                        )
                                    ], 
                                    col=3, 
                                    alignment=ft.MainAxisAlignment.START, 
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=5
                            ),
                            ft.Container(col=4,
                                padding=5, bgcolor=ft.Colors.WHITE10,
                                border_radius=10,
                                content=
                                    ft.Column(
                                        controls=[
                                            self.text_color_picker,
                                            self.color_picker,
                                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER,
                                        tight=True
                                    ), margin=0
                            ),
                        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START
                    )
                ),
            
                ft.Container(expand=1, content=
                    ft.Row(
                        controls=[
                            button_save,
                            button_delete_all,
                            ], alignment=ft.MainAxisAlignment.SPACE_AROUND, vertical_alignment=ft.CrossAxisAlignment.END
                        )
                    )
            ],
        )