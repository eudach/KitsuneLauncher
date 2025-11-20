import flet as ft
from core.utils import generar_degradado, alerta, TYPES_COLORS

async def change_language_on_time(self):
    page: ft.Page = self.page
    try:
        page.logger.info("Cambiando idioma de la interfaz")

        self.input_java_path.label = page.t("java_path_")
        self.dropdown_language.label = page.t("lenguaje_dropdown")
        self.input_minecraft_path.label = page.t("mc_path_")
        self.text_discord_rich.value = page.t("discord_rich")
        self.text_opacity.value = page.t("opacity")
        self.text_ram.value = page.t("ram_usage")
        self.text_wallpaper.value = page.t("wallpaper_save")
        
        self.text_close_app.value = page.t("no_close_app")
        
        self.button_save.content.controls[1].value = page.t('save_')
        self.button_report.content.controls[1].value = page.t('report')
        self.button_delete_all.content.controls[1].value = page.t('delete_all_')
        
        page.dropdown_versions.label = page.t("versions_dropdown_label")
        page.dropdown_versions.hint_text = page.t("versions_dropdown")
        page.settings_button.content.controls[1].value = page.t("sections_settings")
        page.perfil_button.content.controls[1].value = page.t("sections_profile")  
        page.iconbutton_console.tooltip.message = page.t("sections_main")
        page.button_play.content.controls[1].content.value = page.t("play_button")
        
        
        page.update()
        if page.launcher.config.get("app_background"):
            self.page.stray.update()
        page.logger.info("Idioma de la interfaz cambiado exitosamente")
    except Exception as e:
        page.logger.error(f"Error cambiando idioma: {e}")

async def change_thema_on_time(self):
    page = self.page
    try:
        page.logger.info("Aplicando tema de colores")
        prim = page.launcher.config.get("primary_color_schema")
        light = page.launcher.config.get("light_color_schema")
        dark = page.launcher.config.get("dark_color_schema")
        page.global_vars["primary_color"] = prim
        
        
        self.container_wallpaper.bgcolor = prim
        
        self.app_background_allow.active_color = prim
        self.app_background_allow.inactive_track_color = light
        self.app_background_allow.thumb_color = light
        self.app_background_allow.inactive_thumb_color = dark
        self.app_background_allow.track_color = dark
        
        self.discord_presence_allow.active_color = prim
        self.discord_presence_allow.inactive_track_color = light
        self.discord_presence_allow.thumb_color = light
        self.discord_presence_allow.inactive_thumb_color = prim
        self.discord_presence_allow.track_color = dark
        
        self.slider_ram.active_color = prim
        self.slider_opacity.active_color = prim
        
        self.iconbutton_wallpaper.icon_color = prim
        self.iconbutton_java_path.icon_color = prim
        self.iconbutton_mc_path.icon_color = prim
        
        self.input_java_path.cursor_color = prim
        self.input_java_path.selection_color = prim
        
        self.input_minecraft_path.cursor_color = prim
        self.input_minecraft_path.selection_color = prim
        
        for text in self.column_java_recomendations.controls:
            text.spans[1].style.decoration_color = prim
            text.spans[1].style.color = prim

        page.progress_bar.color = prim
        page.content_menu.border = ft.border.all(1, prim)
            
        page.button_play.style.bgcolor = prim
        page.borderside_sections.color = prim
        
        page.update()
        page.logger.info("Tema de colores aplicado exitosamente")
    except Exception as e:
        page.logger.error(f"Error aplicando tema de colores: {e}")

async def reload_all_versions(self):
    page = self.page
    try:
        page.logger.info("Recargando lista de versiones de Minecraft")
        page.dropdown_versions.value = None
        page.dropdown_versions.options=[
            ft.dropdownm2.Option(key=e[0], data=e, content=
                ft.Row(controls=
                    [   
                        ft.Image(src="iconos/minecraft.png" if not e[1] else "iconos/icono.png", width=30, height=30),
                        ft.Text(value=e[0], font_family='liberation', size=page.window.width*0.011, tooltip=page.tooltip_installation_needed if not e[1] else None )
                        
                    ], alignment=ft.MainAxisAlignment.START
                ),
                on_click=self.select_ver
            ) for e in page.launcher.versions
        ]
        
        page.launcher.check_launcher_profiles()
        page.dropdown_versions.update()
    except Exception as e:
        page.logger.error(f"Error recargando versiones: {e}")

async def save_settings(self, e):
    page = self.page
    try:
        page.logger.info("Iniciando guardado de configuraciones")
        #OPACITY
    
        if page.launcher.config.get("opacity") != round(self.slider_opacity.value):
            opacity_value = round(self.slider_opacity.value)
            color = TYPES_COLORS[opacity_value]

            # Mapeo: (atributo de page, propiedad, valor)
            updates = [
                ("content_menu", "bgcolor", color[2]),
                ("bottom_bar", "bgcolor", color[2]),
                ("slider_opacity", "inactive_color", color[0]),
                ("slider_ram", "inactive_color", color[0]),
                ("home_button", "style.bgcolor", "transparent"),
                ("perfil_button", "style.bgcolor", "transparent"),
                ("settings_button", "style.bgcolor", "transparent"),
                ("settings_button", "style.bgcolor", "transparent")
            ]
            
            page.selected_button.style.bgcolor = color[1]

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
            page.temp_config_modrinth["list_changes"].append("Opacity")
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
            page.temp_config_modrinth["list_changes"].append("Java dir")
        
        #MINECRAFT PATH
        if self.input_minecraft_path.value != page.launcher.minecraft_path:
            page.launcher.set_minecraft_path(self.input_minecraft_path.value)
            page.temp_config_modrinth["list_changes"].append("Minecraft dir")
            
            
            
            page.run_task(reload_all_versions, self)
        
        #RAM
        if page.launcher.config.get("ram") != round(self.slider_ram.value):
            page.launcher.config.set("ram", round(self.slider_ram.value))
            page.temp_config_modrinth["list_changes"].append("Ram")
        
        #DISCORD
        if page.launcher.config.get("discord_presence") != self.discord_presence_allow.value:
            page.launcher.config.set("discord_presence", self.discord_presence_allow.value) 
            page.temp_config_modrinth["list_changes"].append("Discord")
            
            if page.launcher.config.get("discord_presence"):
                page.presence.update()
            else:
                page.presence.clear()
        
        #STRAY
        if page.launcher.config.get("app_background") != self.app_background_allow.value:
            page.launcher.config.set("app_background", self.app_background_allow.value)
            if page.launcher.config.get("app_background"):
                page.stray.start()
            else:
                page.stray.stop()
            page.temp_config_modrinth["list_changes"].append("Stray")
        
        #WALLPAPER
        if page.launcher.config.get("wallpaper_launcher") != self.image_wallpaper_widget.src:
            page.launcher.config.set("wallpaper_launcher", self.image_wallpaper_widget.src)
            
            page.views[0].decoration.image.src = self.image_wallpaper_widget.src
            page.views[0].update()
            page.temp_config_modrinth["list_changes"].append("Wallpaper")
        
        #COLOR PICKER
        if page.launcher.config.get("primary_color_schema") != self.color_picker.current_color:
            degrados = generar_degradado(self.color_picker.current_color)
            
            page.launcher.config.set("primary_color_schema", self.color_picker.current_color)
            page.launcher.config.set("light_color_schema", degrados[1])
            page.launcher.config.set("dark_color_schema", degrados[0])
            
            colorss = page.launcher.config.get("last_colors")
            colorss.insert(0, self.color_picker.current_color)
            colorss.pop()
            
            page.launcher.config.set("last_colors", colorss)
            
            page.run_task(change_thema_on_time, self)
            
            await self.reload_last_colors()
            
            page.temp_config_modrinth["list_changes"].append("Thema")
        
        #LENGUAJE
        if page.launcher.config.get("language") != self.dropdown_language.value:
            page.launcher.config.set("language", self.dropdown_language.value)
            page.temp_config_modrinth["list_changes"].append("Language")
            
            page.run_task(change_language_on_time, self)
    
        #SAVE
        if len(page.temp_config_modrinth["list_changes"]) == 0:
            page.logger.info("No hay cambios para guardar")
            return

        changes = page.temp_config_modrinth["list_changes"]
        page.logger.info(f"Guardando configuraciones: {', '.join(changes)}")
        
        page.open(
            alerta(
                titulo= page.t("settings_saved"),
                descripcion= f"{page.t('setting_saved_description')}:\n {','.join(changes)}",
                success=True
                )
            )
        
        page.launcher.config.save()
        page.temp_config_modrinth["list_changes"] = []
        page.logger.info("Configuraciones guardadas exitosamente")
    except Exception as ex:
        page.logger.error(f"Error guardando configuraciones: {ex}")
        page.open(
            alerta(
                titulo="Error",
                descripcion=f"Error al guardar configuraciones: {str(ex)}"
            )
        )