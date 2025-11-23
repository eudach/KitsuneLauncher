import asyncio
import flet as ft

from ui.components.button import ButtonDeleteAll, ButtonSave, ButtonReport
from ui.components.dropdown import DropdownLenguage
from ui.components.color_picker import ColorPicker

from core.utils import return_appdata

from ui.components.input import InputJavaPath, InputMinecraftPath
from ui.components.slider import SliderOpacity, SliderRam
from ui.components.iconbutton import (IconButtonWallpaper,IconButtonJavaPath, IconButtonMcPath)


from ui.sections.Settings.Save import save_settings
from ui.resources.Fonts import BaseFonts

class Settings:
    def __init__(self, page, select_ver):
        self.page = page
        self.select_ver = select_ver
    
    async def change_wallaper_presets(self, e):
        page = self.page
        try:
            page.launcher.config.set("wallpaper_launcher", e.control.data)
            
            page.views[0].decoration.image.src = e.control.data
            self.image_wallpaper_widget.src = e.control.data
            
            self.image_wallpaper_widget.update()
            page.views[0].update()
            
            page.launcher.config.save()
            page.logger.info("Wallpaper cambiado exitosamente")
        except Exception as ex:
            page.logger.error(f"Error cambiando wallpaper: {ex}")
        
    async def show_list_wallpaper(self, e):
        page = self.page
        self.page.open(
            ft.AlertDialog(
                bgcolor=ft.Colors.BLACK87,
                shape=ft.BeveledRectangleBorder(3),
                icon=ft.Row(controls=[
                        ft.Row(expand=True),
                        ft.IconButton(icon=ft.Icons.CLOSE, icon_color=self.page.global_vars["primary_color"], on_click=page.close_alert)
                    ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                open=True,
                content=ft.Row(
                    wrap=True,
                    spacing=100,
                    run_spacing=50,
                    controls=[
                        ft.Container(
                            content=ft.Image(
                                src=f"imgs/wallpaper{e}.gif",
                                width=page.window.width*0.10,
                                height=page.window.height*0.10,
                                border_radius=10,
                                fit=ft.ImageFit.FILL
                                
                            ),
                            ink=True,
                            on_click=self.change_wallaper_presets,
                            data=f"imgs/wallpaper{e}.gif",
                            border_radius=10,
                            padding=1,
                            bgcolor=page.global_vars["primary_color"]
                        )
                    for e in range(1, 9)
                    ]+[
                        
                        ft.Container(
                            content=ft.Image(
                                src=f"imgs/wallpaper.png",
                                width=page.window.width*0.10,
                                height=page.window.height*0.10,
                                border_radius=10,
                                fit=ft.ImageFit.FILL
                            ),
                            ink=True,
                            on_click=self.change_wallaper_presets,
                            data=f"imgs/wallpaper.png",
                            border_radius=10,
                            padding=1,
                            bgcolor=page.global_vars["primary_color"]
                        )
                    ],
                expand=True
                )
            )
        )
        
    async def ram_change_function(self, e):
        self.text_ram.value = f"{round(self.slider_ram.value)} GB"
        self.text_ram.update()
        
    async def filepicker_select_bin_javaw(self, e:ft.FilePickerResultEvent):
        page = self.page
        try:
            from pathlib import Path
            if e.files:
                java_path = e.files[0].path
            elif e.path:
                candidate_dir = Path(e.path)
                java_candidates = [candidate_dir / "bin" / "java", candidate_dir / "bin" / "java.exe"]
                java_path = None
                for cand in java_candidates:
                    if cand.exists():
                        java_path = str(cand)
                        break
                if java_path is None:
                    java_path = e.path
            else:
                page.logger.debug("Selección de Java cancelada")
                return

            page.logger.info(f"Ruta de Java seleccionada: {java_path}")
            self.input_java_path.value = java_path
            self.input_java_path.update()
            # Aplicar inmediatamente al launcher y config
            if page.launcher.set_java(java_path):
                page.logger.info("Java path establecido correctamente (pendiente de guardar definitivo si necesario).")
            else:
                page.logger.warning("La ruta seleccionada no contiene ejecutable Java válido.")
            page.run_task(self.validate_java_path)
        except Exception as ex:
            page.logger.error(f"Error seleccionando archivo Java: {ex}")
        
    async def filepicker_select_minecraft_path(self, e:ft.FilePickerResultEvent):
        page = self.page
        try:
            if not e.path:
                page.logger.debug("Selección de directorio de Minecraft cancelada")
                return

            minecraft_path = e.path
            page.logger.info(f"Directorio de Minecraft seleccionado: {minecraft_path}")
            self.input_minecraft_path.value = minecraft_path
            self.input_minecraft_path.update()
        except Exception as ex:
            page.logger.error(f"Error seleccionando directorio de Minecraft: {ex}")
        
    async def select_img_wallpaper(self, e:ft.FilePickerResultEvent):
        page = self.page
        try:
            if e.files is None:
                page.logger.debug("Selección de imagen de wallpaper cancelada")
                return
            
            wallpaper_path = e.files[0].path
            page.logger.info(f"Imagen de wallpaper seleccionada: {wallpaper_path}")
            self.image_wallpaper_widget.src = wallpaper_path
            self.image_wallpaper_widget.update()
        except Exception as ex:
            page.logger.error(f"Error seleccionando imagen de wallpaper: {ex}")
    
    async def bttn_img_wallpaper(self, e):
        self.filepicker_wallapaper.pick_files(
            self.page.t('select_img_wallpaper'),
            allowed_extensions=["jpg", "png", "jpeg", "gif"]
        )
    
    async def bttn_check_minecraft_path(self, e):
        self.filepicker_minecraft_path.get_directory_path(
            dialog_title="Select new .miecraft",
            initial_directory=return_appdata()
        )
        
    async def bttn_select_java_bin(self, e):
        import sys
        if sys.platform.startswith("win"):
            self.filepicker_javaw.pick_files(
                f"{self.page.t('select_javaw')} javaw.exe",
                allowed_extensions=["exe"]
            )
        else:
            self.filepicker_javaw.get_directory_path(
                dialog_title=self.page.t('select_javaw') + " JAVA_HOME"
            )

    async def validate_java_path(self):
        page = self.page
        from pathlib import Path
        import subprocess, sys, asyncio
        from ui.components import toast
        exe_path = self.input_java_path.value
        if not exe_path:
            return
        p = Path(exe_path)
        if p.is_dir():
            pt = p / 'bin' / ('java.exe' if sys.platform.startswith('win') else 'java')
            if pt.exists():
                p = pt
        if not p.exists():
            page.toaster.show_toast(toast.Toast(content=ft.Text(value=page.t('file_not_found'), font_family=BaseFonts.texts), toast_type=toast.ToastType.ERROR), duration=3)
            return
        try:
            proc = await asyncio.to_thread(lambda: subprocess.run([str(p), '-version'], capture_output=True, text=True))
            output = proc.stderr or proc.stdout
            if proc.returncode == 0 and 'version' in output.lower():
                page.toaster.show_toast(toast.Toast(content=ft.Text(value=page.t('java_found'), font_family=BaseFonts.texts), toast_type=toast.ToastType.SUCCESS), duration=3)
                page.logger.info(f"Java válido detectado: {output.splitlines()[0]}")
            else:
                page.toaster.show_toast(toast.Toast(content=ft.Text(value=page.t('java_invalid'), font_family=BaseFonts.texts), toast_type=toast.ToastType.ERROR), duration=4)
                page.logger.warning(f"Java inválido o error: {output}")
        except Exception as ex:
            page.toaster.show_toast(toast.Toast(content=ft.Text(value=f"Java error: {ex}", font_family=BaseFonts.texts), toast_type=toast.ToastType.ERROR), duration=4)
            page.logger.error(f"Error validando Java: {ex}")
        
    async def load_last_colors(self, e):
        self.color_picker.set_color(e.control.bgcolor)
        
    async def reload_last_colors(self):
        for cont in range(len(self.list_colors)):
            self.row_witha_last_colors.controls[cont].bgcolor = self.list_colors[cont]
        
        self.row_witha_last_colors.update()

    async def load(self):
        page:ft.Page = self.page
        page.global_vars["current_section"] = 'settings'
        page.content_menu.alignment= ft.alignment.top_left
        # Placeholder inmediato para no quedar en loading global
        page.content_menu.content = ft.Column(
            controls=[ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.ProgressRing(), ft.Text("Cargando configuración...")])],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        page.update()
            
        self.text_delete_all = ft.Text(
            value=page.t('delete_all_'),
            font_family=BaseFonts.texts,
            size=page.window.width/60,
            text_align=ft.TextAlign.CENTER
        )
        self.text_ram = ft.Text(
            value=page.t('ram_usage'),
            max_lines=2, size=page.window.width/70,
            text_align=ft.TextAlign.CENTER,
            font_family=BaseFonts.texts
        )
        self.text_opacity = ft.Text(
            value=page.t('opacity'),
            max_lines=2, size=page.window.width/70,
            text_align=ft.TextAlign.CENTER,
            font_family=BaseFonts.texts
        )
        
        self.discord_presence_allow = ft.Switch(
            value=page.launcher.config.get("discord_presence"),
            active_color=page.global_vars["primary_color"],
            track_color=page.launcher.config.get("dark_color_schema"),
            thumb_color=page.launcher.config.get("light_color_schema"),
            track_outline_color='transparent',
            inactive_track_color=page.launcher.config.get("dark_color_schema"),
            inactive_thumb_color=page.launcher.config.get("light_color_schema")
        )
        
        self.app_background_allow = ft.Switch(
            value=page.launcher.config.get("app_background"),
            active_color=page.global_vars["primary_color"],
            track_color=page.launcher.config.get("dark_color_schema"),
            thumb_color=page.launcher.config.get("light_color_schema"),
            track_outline_color='transparent',
            inactive_track_color=page.launcher.config.get("dark_color_schema"),
            inactive_thumb_color=page.launcher.config.get("light_color_schema")
        )
        self.image_wallpaper_widget = ft.Image(
            src=page.launcher.config.get("wallpaper_launcher", page.global_vars["default_wallpaper"]),
            width=page.window.width*0.10,
            height=page.window.height*0.10,
            border_radius=10,
            fit=ft.ImageFit.FILL
        )
        self.text_discord_rich = ft.Text(
            value = page.t('discord_rich'),
            max_lines=2, size=page.window.width/70,
            text_align=ft.TextAlign.CENTER,
            font_family=BaseFonts.texts
        )
        self.text_wallpaper = ft.Text(
            value=page.t('wallpaper_save'),
            max_lines=2, size=page.window.width/70,
            text_align=ft.TextAlign.CENTER,
            font_family=BaseFonts.texts
        )
        self.text_close_app = ft.Text(
            value=page.t('no_close_app'),
            max_lines=2, size=page.window.width/60,
            text_align=ft.TextAlign.CENTER,
            font_family=BaseFonts.texts,
        )
        
        self.color_picker = ColorPicker(color=page.global_vars["primary_color"], width=page.window.width/4, height=page.window.height/4)
        
        self.button_save = ButtonSave(page, lambda a: page.run_task(save_settings, self, a)).get()
        self.button_report = ButtonReport(page).get()
        self.button_delete_all = ButtonDeleteAll(page).get()
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
            bgcolor=page.global_vars["primary_color"],
            on_click=self.show_list_wallpaper
        )
        
        
        self.list_colors = page.launcher.config.get("last_colors") or []
        # Asegurar al menos 6 colores
        while len(self.list_colors) < 6:
            self.list_colors.append(page.global_vars["primary_color"])
        try:
            self.row_witha_last_colors = ft.Row(
                controls=[
                    ft.Container(
                        data=cont,
                        width=25, height=25,
                        bgcolor = self.list_colors[cont-2],
                        border_radius=5,
                        ink=True,
                        on_click=self.load_last_colors
                    )
                for cont in range(2,8)], alignment=ft.MainAxisAlignment.CENTER
            )
        except Exception as ex:
            page.logger.error(f"Error construyendo paleta de colores: {ex}")
            self.row_witha_last_colors = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
        
        self.column_java_recomendations = ft.Column(
            controls=[
                ft.Text(
                    size=page.window.width/70,
                    text_align=ft.TextAlign.CENTER,
                    font_family=BaseFonts.texts,
                    spans=[
                        ft.TextSpan(text="Minecraft [1.0 – 1.16.5] → ", style=ft.TextStyle(font_family=BaseFonts.texts)),
                        ft.TextSpan(
                            text="Java 8",
                            
                            style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True, decoration=ft.TextDecoration.UNDERLINE, font_family=BaseFonts.texts, decoration_color=page.global_vars["primary_color"], color=page.global_vars["primary_color"]),
                            url="https://adoptium.net/es/temurin/releases?variant=openjdk8&jvmVariant=hotspot&version=8&os=any&arch=any"
                        )
                    ]
                ),
                ft.Text(
                    size=page.window.width/70,
                    text_align=ft.TextAlign.CENTER,
                    font_family=BaseFonts.texts,
                    spans=[
                        ft.TextSpan(text="Minecraft [1.17 – 1.17.1] → ", style=ft.TextStyle(font_family=BaseFonts.texts)),
                        ft.TextSpan(
                            text="Java 11",
                            style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True, decoration=ft.TextDecoration.UNDERLINE, font_family=BaseFonts.texts, decoration_color=page.global_vars["primary_color"], color=page.global_vars["primary_color"]),
                            url="https://adoptium.net/es/temurin/releases?variant=openjdk8&jvmVariant=hotspot&version=11&os=any&arch=any"
                        )
                    ]
                ),
                ft.Text(
                    size=page.window.width/70,
                    text_align=ft.TextAlign.CENTER,
                    font_family=BaseFonts.texts,
                    spans=[
                        ft.TextSpan(text="Minecraft [1.18 – 1.20.1] → ", style=ft.TextStyle(font_family=BaseFonts.texts)),
                        ft.TextSpan(
                            text="Java 17",
                            style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True, decoration=ft.TextDecoration.UNDERLINE, font_family=BaseFonts.texts, decoration_color=page.global_vars["primary_color"], color=page.global_vars["primary_color"]),
                            url="https://adoptium.net/es/temurin/releases?variant=openjdk16&jvmVariant=hotspot&version=17&os=any&arch=any"
                        )
                    ]
                ),
                ft.Text(
                    size=page.window.width/70,
                    text_align=ft.TextAlign.CENTER,
                    font_family=BaseFonts.texts,
                    spans=[
                        ft.TextSpan(text="Minecraft [1.20.2 – 1.20.4] → ", style=ft.TextStyle(font_family=BaseFonts.texts)),
                        ft.TextSpan(
                            text="Java 21",
                            style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True, decoration=ft.TextDecoration.UNDERLINE, font_family=BaseFonts.texts, decoration_color=page.global_vars["primary_color"], color=page.global_vars["primary_color"]),
                            url="https://adoptium.net/es/temurin/releases?variant=openjdk16&jvmVariant=hotspot&version=21&os=any&arch=any"
                        )
                    ]
                ),
                ft.Text(
                    size=page.window.width/70,
                    text_align=ft.TextAlign.CENTER,
                    font_family=BaseFonts.texts,
                    spans=[
                        ft.TextSpan(text="Minecraft [1.20.5 – 1.21.x+] → ", style=ft.TextStyle(font_family=BaseFonts.texts)),
                        ft.TextSpan(
                            text="Java 21+",
                            style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True, decoration=ft.TextDecoration.UNDERLINE, font_family=BaseFonts.texts, decoration_color=page.global_vars["primary_color"], color=page.global_vars["primary_color"]),
                            url="https://adoptium.net/es/temurin/releases?variant=openjdk16&jvmVariant=hotspot&version=21&os=any&arch=any"
                        )
                    ],
                )
            ], tight=True, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.BASELINE
        )
        
        page.views[0].floating_action_button = ft.Row(
            controls=[
                self.button_report,
                self.button_save,
                self.button_delete_all,
                ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.END
            )
        
        try:
            page.content_menu.content= ft.ResponsiveRow(columns=14,
            spacing=5, run_spacing=5,
            controls=[
                ft.Column(controls=
                    [
                        ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, content=self.input_java_path, margin=0),
                        ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, content=self.input_minecraft_path, margin=0),
                        ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, content=self.dropdown_language, margin=0),
                        ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, padding=5, content=
                            ft.Column(
                                controls=[
                                    self.text_ram,
                                    self.slider_ram,
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, tight=True
                            ), margin=0
                        ),
                        ft.Container(alignment=ft.alignment.center, bgcolor=ft.Colors.WHITE10, border=ft.border.all(1, ft.Colors.BLACK), padding=5, margin=0,
                            content=
                                ft.Column(
                                    controls=[
                                        self.text_close_app,
                                        self.app_background_allow,
                                    ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER,
                            )
                        )
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
                                ,tight=True), margin=0, alignment=ft.alignment.center
                            ),
                            ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, padding=10, margin=0, content=ft.Column(
                                controls=[
                                    self.text_wallpaper,
                                    ft.Row(controls=
                                        [
                                            self.container_wallpaper,
                                            self.iconbutton_wallpaper
                                            ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER, tight=True
                                        ),
                                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True
                                )
                            ),
                            ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, padding=10, margin=0, content=ft.Column(
                                controls=[
                                    self.text_opacity,
                                    self.slider_opacity
                                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True
                                )
                            )
                        ], 
                        col=3, 
                        alignment=ft.MainAxisAlignment.START, 
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5
                ),
                ft.Column(
                    col=3,
                    alignment=ft.MainAxisAlignment.START, 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                    controls=[
                        ft.Container(
                            padding=5, bgcolor=ft.Colors.WHITE10, border=ft.border.all(1, ft.Colors.BLACK),
                            alignment=ft.alignment.center,
                            content=ft.Column(
                                controls=[
                                    self.color_picker,
                                    self.row_witha_last_colors
                                ]
                            )
                            ,
                            margin=0
                        ),
                        
                        
                    ]
                ),
                
                ft.Container(
                    col=4,
                    border=ft.border.all(1, ft.Colors.BLACK),
                    padding=10,
                    content=self.column_java_recomendations,
                    bgcolor=ft.Colors.WHITE10, 
                )
            ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START
            )
        except Exception as ex:
            page.logger.error(f"Error final construyendo Settings: {ex}")
            page.content_menu.content = ft.Container(
                bgcolor=ft.Colors.RED_900,
                padding=20,
                border_radius=10,
                content=ft.Column(
                    controls=[
                        ft.Text(value="Error cargando Settings", color=ft.Colors.WHITE, size=24),
                        ft.Text(value=str(ex), color=ft.Colors.WHITE70, selectable=True, size=14),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.START
                )
            )
        await asyncio.sleep(0)

    # Live color change removed: theme updates apply on save only.