import asyncio
import threading
import flet as ft
from flet_route import Params,Basket
from flet_contrib.color_picker import ColorPicker
from Tools import generar_degradado, alerta, TYPES_COLORS

async def MainView(page:ft.Page, params:Params, basket:Basket):
    
    async def clr_data_modal(e):
        page.launcher.config.reset()
        page.window.close()
        
    async def change_thema_on_time():
        prim = page.launcher.config.get("primary_color_schema")
        
        iconbutton_wallpaper.icon_color = prim
        iconbutton_java_path.icon_color = prim
        iconbutton_mc_path.icon_color = prim
        input_java_path.cursor_color = prim
        input_minecraft_path.cursor_color = prim
        slider_ram.active_color = prim
        slider_opacity.active_color = prim
        discord_presence_allow.active_color = prim
        discord_presence_allow.inactive_track_color = page.launcher.config.get("light_color_schema")
        discord_presence_allow.inactive_thumb_color = page.launcher.config.get("dark_color_schema")
        button_save.style.color[ft.ControlState.HOVERED] = prim
        button_close_session.style.color[ft.ControlState.HOVERED] = prim
        borderside_sections.color = prim
        content_menu.border = ft.border.all(1, prim)
        boton_jugar.bgcolor = prim
        page.progress_bar.color = prim
        
        page.update()
        
        
    async def reload_all_versions():
        dropdown_versions.value = None
        dropdown_versions.options=[
            ft.dropdownm2.Option(key=e[0], data=e, content=
                ft.Row(controls=
                    [   
                        ft.Image(src="mc_icon.png" if not e[1] else "icono.png", width=30, height=30),
                        ft.Text(value=e[0], font_family='liberation', size=page.ancho*0.011, tooltip=tooltip_installation_needed if not e[1] else None )
                        
                    ], alignment=ft.MainAxisAlignment.START
                ),
                on_click=select_ver
            ) for e in page.launcher.versions
        ]
        dropdown_versions.update()
    
    async def delte_all_data(e):
        alrt = ft.AlertDialog(
            icon=ft.Icon(name=ft.Icons.WARNING_AMBER),
            title=ft.Text(value=page.t("data_elimination"), text_align=ft.TextAlign.CENTER),
            content=ft.Text(value=page.t("data_elimination_sure"), text_align=ft.TextAlign.CENTER),
            actions=[
                ft.TextButton(page.t("data_question_y"), on_click=clr_data_modal, style=ft.ButtonStyle(color=page.color_init)),
                ft.TextButton("No", style=ft.ButtonStyle(color=page.color_init), on_click=lambda e: page.close(alrt)),
            ],
            bgcolor=ft.Colors.BLACK,
            shape=ft.BeveledRectangleBorder(3),
            icon_color=page.color_init,
            alignment=ft.alignment.center,
        )
        page.open(
            alrt
        )
    
    async def save_settings(e):
        changes_ = []
        global need_restart
        need_restart = False
        
        #OPACITY
        
        if page.launcher.config.get("opacity") != round(slider_opacity.value):
            color = TYPES_COLORS[round(slider_opacity.value)]
            
            content_menu.bgcolor = color[2]
            content_sidebar.bgcolor = color[2]
            
            
            page.views[0].appbar.bgcolor = color[1]
            content_sections.bgcolor = color[1]
            
            home_button.style.bgcolor = 'transparent'
            perfil_button.style.bgcolor = 'transparent'
            settings_button.style.bgcolor = 'transparent'
            slider_opacity.inactive_color = color[0]
            slider_ram.inactive_color  = color[0]
            
            page.update()
            changes_.append("Opacity")
            page.launcher.config.set("opacity", round(slider_opacity.value))
        
        
        #JAVA PATH
        if not page.launcher.set_java(input_java_path.value, False):
            page.open(
                alerta(
                    titulo= "Error",
                    descripcion= page.t("file_not_found")
                )
            )
            return

        if page.launcher.java_path != input_java_path.value:
            page.launcher.set_java(input_java_path.value)
            changes_.append("Java dir")
        
        #MINECRAFT PATH
        if input_minecraft_path.value != page.launcher.minecraft_path:
            page.launcher.set_minecraft_path(input_minecraft_path.value)
            changes_.append("Minecraft dir")
            
            asyncio.create_task(reload_all_versions())
        
        #RAM
        if page.launcher.config.get("ram") != round(slider_ram.value):
            page.launcher.config.set("ram", round(slider_ram.value))
            changes_.append("Ram")
        
        #DISCORD
        if page.launcher.config.get("discord_presence") != discord_presence_allow.value:
            page.launcher.config.set("discord_presence", discord_presence_allow.value) 
            changes_.append("Discord")
            
            if page.launcher.config.get("discord_presence"):
                page.presence.set(
                    {
                    "state": page.t("user_state_discord_mainpage"),
                    "details": f"{page.launcher.config.get("username")} {page.t("user_state_discord_conect")}",
                    "timestamps": {"start": page.discord_times},
                    }
                )
            else:
                page.presence.clear()
        
        #WALLPAPER
        if page.launcher.config.get("wallpaper_launcher") != image_wallpaper_widget.src:
            page.launcher.config.set("wallpaper_launcher", image_wallpaper_widget.src)
            
            page.views[0].decoration.image.src = image_wallpaper_widget.src
            page.views[0].update()
            changes_.append("Wallpaper")
        
        #COLOR PICKER
        if page.color_init != color_picker.color:
            degrados = generar_degradado(color_picker.color)
            
            page.launcher.config.set("primary_color_schema", color_picker.color)
            page.launcher.config.set("light_color_schema", degrados[1])
            page.launcher.config.set("dark_color_schema", degrados[0])
            
            asyncio.create_task(change_thema_on_time())
            
            changes_.append("Thema")
        
        #LENGUAJE
        if page.launcher.config.get("language") != dropdown_language.value:
            page.launcher.config.set("language", dropdown_language.value)
            changes_.append("Language")
            
            asyncio.create_task(change_lenguage_on_time())
        
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
        
    async def close_session(e):
        page.open(
            alerta(
                titulo= page.t("session_closed"),
                descripcion= f"{page.t('session_closed_description')} {page.launcher.config.get("username")}",
                success=True
            )
        )
        
        page.launcher.config.set("username", None)
        page.launcher.config.save()
        page.go("/login")
    
    async def install_minecraft_version(e):
        page.close(page.overlay[-1])
        boton_jugar.disabled = True
        boton_jugar.content.content.controls[1].value = page.t("play_button_installing")
        boton_jugar.update()
        page.launcher.instalar_minecraft_en_hilo(page, e.control.data)
    
    async def dismiss_installation(e):
        page.close(page.overlay[-1])
        
        boton_jugar.disabled = True
        boton_jugar.content.content.controls[1].value = page.t("version_not_installed")
        boton_jugar.update()
        
    async def select_ver(e:ft.ControlEvent):
        installed = page.launcher.set_version(e.control.data)
        version = e.control.data[0]
        
        if not installed:
        
            alrt = ft.AlertDialog(
                icon=ft.Icon(name=ft.Icons.WARNING_AMBER),
                title=ft.Text(value=page.t('installation_sucess'), text_align=ft.TextAlign.CENTER),
                content=ft.Text(value=f"{version} {page.t('installation_sucess_description')}", text_align=ft.TextAlign.CENTER),
                actions=[
                    ft.TextButton(page.t("data_question_y"), data=version, on_click=install_minecraft_version, style=ft.ButtonStyle(color=page.color_init)),
                    ft.TextButton("No", on_click=dismiss_installation, style=ft.ButtonStyle(color=page.color_init))
                ],
                bgcolor=ft.Colors.BLACK,
                shape=ft.BeveledRectangleBorder(3),
                icon_color=page.color_init,
                alignment=ft.alignment.center,
            )
            
            page.open(alrt)
    
    async def bttn_check_minecraft_path(e):
        filepicker_minecraft_path.get_directory_path(dialog_title="Select new .miecraft", initial_directory=page.launcher.return_appdata())
        
        
    #BUTTON
    async def bttn_select_java_bin(e):
        filepicker_javaw.pick_files(f"{page.t('select_javaw')} javaw.exe", allowed_extensions=["exe"])
        
    async def select_img_wallpaper(e:ft.FilePickerResultEvent):
        if e.files is None:
            return
        
        #page.wallpaper_launcher = e.files[0].path
        image_wallpaper_widget.src = e.files[0].path
        
        image_wallpaper_widget.update()
    
    #FILEPICKER WIDGET
    async def filepicker_select_bin_javaw(e:ft.FilePickerResultEvent):
        if e.files is None:
            return
        
        input_java_path.value = e.files[0].path
        input_java_path.update()
        
    async def filepicker_select_minecraft_path(e:ft.FilePickerResultEvent):
        if not e.path:
            return

        input_minecraft_path.value = e.path
        input_minecraft_path.update()
    
    async def ram_change_function(e):
        text_ram.value = f"{round(slider_ram.value)} GB"
        text_ram.update()
    
    async def opacity_slider_change(e):
        pass
            
        
    
    async def change_lenguage_on_time():
        input_java_path.label = page.t('java_path_')
        dropdown_language.label = page.t('lenguaje_dropdown')
        input_minecraft_path.label = page.t('mc_path_')
        dropdown_versions.label = page.t('versions_dropdown_label')
        dropdown_versions.hint_text = page.t('versions_dropdown'),
        home_button.text = page.t("sections_main")
        settings_button.text = page.t("sections_settings")
        perfil_button.text = page.t("sections_profile")
        tooltip_delete_all.message=page.t('delete_all_confirmation_')
        tooltip_installation_needed.message=page.t('installation_needed')
        
        
        text_discord_rich.value = page.t('discord_rich')
        text_opacity.value = page.t('opacity')
        text_ram.value = page.t('ram_usage')
        text_wallpaper.value = page.t('wallpaper_save')
        text_save.value = page.t('save_')
        text_delete_all.value = page.t('delete_all_')
        text_close_session.value = page.t('session_close')
        text_play.value = page.t("play_button")
        text_color_picker.value = page.t('color_picker_text')
        
        page.update()
        
    
    async def bttn_img_wallpaper(e):
        filepicker_wallapaper.pick_files(page.t('select_img_wallpaper'), allowed_extensions=["jpg", "png", "jpeg"])
    
    #WIDGETS
    tooltip_delete_all = ft.Tooltip(
        message=page.t('delete_all_confirmation_')
    )
    tooltip_installation_needed = ft.Tooltip(
        message=page.t('installation_needed')
    )

    iconbutton_wallpaper = ft.IconButton(
        icon=ft.Icons.EDIT,
        on_click=bttn_img_wallpaper,
        bgcolor=ft.Colors.TRANSPARENT,
        icon_color=page.color_init
    )
    iconbutton_java_path = ft.IconButton(
        icon=ft.Icons.FOLDER,
        icon_color=page.color_init,
        padding=0,
        hover_color=ft.Colors.BLACK12,
        on_click=bttn_select_java_bin
    )
    iconbutton_mc_path = ft.IconButton(icon=ft.Icons.FOLDER, 
        icon_color=page.color_init, 
        padding=0, 
        hover_color=ft.Colors.BLACK12, 
        on_click=bttn_check_minecraft_path
    )
    
    input_java_path = ft.TextField(
        cursor_color=page.color_init,
        label=page.t('java_path_'),
        bgcolor=ft.Colors.TRANSPARENT,
        border=ft.InputBorder.NONE,
        filled=True,
        value=page.launcher.java_path,
        fill_color=ft.Colors.TRANSPARENT,
        max_lines=1,
        border_radius=3,
        focused_border_color=ft.Colors.WHITE,
        label_style=ft.TextStyle(color=ft.Colors.WHITE,font_family='liberation', size=page.ancho*0.018),
        multiline=True,
        suffix= iconbutton_java_path,
        expand=True,
    )
    input_minecraft_path = ft.TextField(
        cursor_color=page.color_init,
        label=page.t('mc_path_'),
        bgcolor=ft.Colors.TRANSPARENT,
        border=ft.InputBorder.NONE,
        filled=True,
        value=page.launcher.minecraft_path,
        fill_color=ft.Colors.TRANSPARENT,
        max_lines=1,
        border_radius=3,
        focused_border_color=ft.Colors.WHITE,
        label_style=ft.TextStyle(color=ft.Colors.WHITE, font_family='liberation', size=page.ancho*0.018),
        multiline=True,
        suffix= iconbutton_mc_path,
        expand=True,
    )
    
    slider_ram = ft.Slider(
        on_change=ram_change_function,
        min=2,
        max=16,
        round=0,
        value=page.launcher.config.get("ram"),
        divisions=14,
        label="{value}GB",
        inactive_color=TYPES_COLORS[page.launcher.config.get("opacity")][0],
        active_color=page.color_init
    )
    slider_opacity = ft.Slider(
        on_change=opacity_slider_change,
        min=0,
        max=6,
        value=page.launcher.config.get("opacity"),
        label="{value}°",
        divisions=6,
        inactive_color=TYPES_COLORS[page.launcher.config.get("opacity")][0],
        active_color=page.color_init
    )
    
    text_ram = ft.Text(
        value=page.t('ram_usage'),
        max_lines=2, size=page.ancho/70,
        text_align=ft.TextAlign.CENTER,
        font_family="liberation"
    )
    text_opacity = ft.Text(
        value=page.t('opacity'),
        max_lines=2, size=page.ancho/70,
        text_align=ft.TextAlign.CENTER,
        font_family="liberation"
    )
    discord_presence_allow = ft.Switch(
        value=page.launcher.config.get("discord_presence"),
        active_color=page.color_init,
        inactive_track_color=page.launcher.config.get("light_color_schema"),
        inactive_thumb_color=page.launcher.config.get("dark_color_schema")
    )
    text_discord_rich = ft.Text(
        value = page.t('discord_rich'),
        max_lines=2, size=page.ancho/70,
        text_align=ft.TextAlign.CENTER,
        font_family="liberation"
    )
    
    image_wallpaper_widget = ft.Image(
        src=page.launcher.config.get("wallpaper_launcher"),
        width=page.ancho*0.10,
        height=page.alto*0.10,
        border_radius=10
    )
    text_wallpaper = ft.Text(
        value=page.t('wallpaper_save'),
        max_lines=2, size=page.ancho/70,
        text_align=ft.TextAlign.CENTER,
        font_family="liberation"
    )
    
    text_save = ft.Text(
        value=page.t('save_'),
        font_family="lokeya",
        size=page.ancho/60,
        text_align=ft.TextAlign.CENTER
    )
    text_delete_all = ft.Text(
        value=page.t('delete_all_'),
        font_family="lokeya",
        size=page.ancho/70,
        text_align=ft.TextAlign.CENTER
    )
    text_close_session = ft.Text(
        value=page.t('session_close'),
        font_family="liberation",
        size=page.ancho/35,
        text_align=ft.TextAlign.CENTER
    )
    text_play = ft.Text(
        value=page.t("play_button"),
        size=page.ancho/30,
        font_family='katana',
        text_align=ft.TextAlign.CENTER
    )
    text_console = ft.Text(
        value="",
        font_family="console",
        size=page.ancho/65, 
        selectable=True, 
        expand=True
    )
    
    button_save = ft.OutlinedButton(                    
        content=text_save,
        width=page.ancho*0.10,
        height=page.alto*0.07,
        on_click=save_settings,
        style=ft.ButtonStyle(
            overlay_color=ft.Colors.WHITE10 ,
            color={
                ft.ControlState.DEFAULT: ft.Colors.WHITE,
                ft.ControlState.HOVERED: page.color_init,
                },
            side=ft.BorderSide(1, color=ft.Colors.WHITE10),
            shape=ft.RoundedRectangleBorder(10),
            bgcolor=ft.Colors.WHITE10
        ),
    )
    button_delete_all = ft.OutlinedButton(                     
        content=text_delete_all,
        width=page.ancho*0.10,
        height=page.alto*0.07,
        tooltip=tooltip_delete_all,
        style=ft.ButtonStyle(
            overlay_color=ft.Colors.WHITE10,
            color={
                ft.ControlState.DEFAULT: ft.Colors.WHITE,
                ft.ControlState.HOVERED: ft.Colors.RED,
                ft.ControlState.FOCUSED: ft.Colors.RED_ACCENT_100
            },
            side=ft.BorderSide(1, color=ft.Colors.WHITE10),
            shape=ft.RoundedRectangleBorder(10),
            bgcolor=ft.Colors.WHITE10
        ),
        on_click=delte_all_data
    )
    button_close_session = ft.OutlinedButton(                           
        content=text_close_session,
        width=page.ancho*0.20,
        height=page.alto*0.10,
        on_click=close_session,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(10),
            overlay_color=ft.Colors.WHITE10,
            color={
                ft.ControlState.DEFAULT: ft.Colors.WHITE,
                ft.ControlState.HOVERED: page.color_init,
                },
            bgcolor=ft.Colors.WHITE10,
            side=ft.BorderSide(1, color=ft.Colors.WHITE10),
            
            ),
    )
    
    borderside_sections = ft.BorderSide(1, 
        color=page.color_init,
        stroke_align=ft.BorderSideStrokeAlign.INSIDE
    )
    filepicker_wallapaper = ft.FilePicker(on_result=select_img_wallpaper)
    filepicker_javaw = ft.FilePicker(on_result=filepicker_select_bin_javaw)
    filepicker_minecraft_path= ft.FilePicker(on_result=filepicker_select_minecraft_path)
    
    page.overlay.append(filepicker_javaw)
    page.overlay.append(filepicker_minecraft_path)
    page.overlay.append(filepicker_wallapaper)
    #END WIDGETS
        
    async def function_content(e):
        buttons = [home_button, perfil_button, settings_button]

        # Reiniciar los bordes
        for btn in buttons:
            if btn.data != e.data:
                btn.style.bgcolor = None
                btn.style.side = {
                    ft.ControlState.DEFAULT: ft.BorderSide(0, color=ft.Colors.TRANSPARENT),
                    ft.ControlState.HOVERED: ft.BorderSide(2, color=ft.Colors.WHITE10),
                    
                    }
            
        button_map = {
            'home': home_button,
            'perfil': perfil_button,
            'settings': settings_button,
            }

        # Cambiar el borde del botón seleccionado
        selected_button = button_map.get(e.control.data)
        
        if selected_button:
            selected_button.style.bgcolor = TYPES_COLORS[page.launcher.config.get("opacity")][0]
            selected_button.style.side = borderside_sections
            selected_button.update()
        
        if selected_button.data == 'settings':
            content_menu.alignment= ft.alignment.top_left
            content_menu.content= ft.Column(
                controls=[
                    
                    ft.Container(expand=9, padding=5, content=
                        ft.ResponsiveRow(columns=14,
                            spacing=5, run_spacing=5,
                            controls=[
                                ft.Column(controls=
                                    [
                                    ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, content=input_java_path, margin=0),
                                    ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, content=input_minecraft_path, margin=0),
                                    ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, content=dropdown_language, margin=0),
                                    ft.Container(border=ft.border.all(2, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, padding=5, content=
                                        ft.Column(
                                            controls=[
                                                text_ram,
                                                slider_ram,
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
                                                        text_discord_rich,
                                                        discord_presence_allow
                                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER
                                                ), margin=0, alignment=ft.alignment.center
                                            ),
                                            ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, padding=10, margin=0, content=ft.Column(
                                                controls=[
                                                    text_wallpaper,
                                                    ft.Row(controls=
                                                        [
                                                            image_wallpaper_widget,
                                                            iconbutton_wallpaper
                                                            ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER
                                                        ),
                                                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                                )
                                            ),
                                            ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, padding=10, margin=0, content=ft.Column(
                                                controls=[
                                                    text_opacity,
                                                    slider_opacity
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
                                    border=ft.border.all(1, ft.Colors.BLACK),
                                    padding=0, bgcolor=ft.Colors.WHITE10,
                                    border_radius=10,
                                    content=
                                        ft.Column(
                                            controls=[
                                                text_color_picker,
                                                color_picker,
                                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER
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
        
        if selected_button.data == 'home':
            content_menu.alignment = ft.alignment.top_left
            
            #AREA DE CONSOLA
            if not hasattr(page, "Text_Console"):
                page.Text_Console = ft.ListView(
                    controls=
                        [
                            text_console
                        ],
                    spacing=5,
                    padding=3,
                    expand=True,
                    auto_scroll=True
                )
            
            
            #AGREGAR CONSOLA
            content_menu.content= ft.Container(
                bgcolor=ft.Colors.WHITE12,
                expand=True,
                content=page.Text_Console,
                
            )
             
        if selected_button.data == 'perfil':
            content_menu.alignment= ft.alignment.center
            content_menu.content= ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Image(
                            filter_quality=ft.FilterQuality.MEDIUM,
                            anti_alias=True,
                            fit=ft.ImageFit.CONTAIN,
                            src=page.launcher.config.get("photo_perfil"),
                            border_radius=(page.ancho*0.35)/2,
                            width=page.ancho*0.25, height=page.alto*0.25
                        ),
                        padding=0,
                        alignment=ft.alignment.center,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        width=page.ancho*0.35, height=page.alto*0.35,
                        bgcolor=ft.Colors.TRANSPARENT,
                        border=ft.border.all(2, ft.Colors.TRANSPARENT),
                        shape=ft.BoxShape.CIRCLE,
                        
                    )
                    ,
                    ft.Container(
                        content=ft.Text(
                            selectable=True,
                            value=page.launcher.config.get("username") ,
                            font_family="liberation", 
                            size=page.ancho/30,
                        ), 
                        bgcolor=ft.Colors.BLACK12,
                        border_radius=10,
                        ink=True, 
                        padding=5
                    ),
                    button_close_session    
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        page.update()
    
        
    async def jugar_func(e):
        version_ = page.launcher.last_played_version
        
        #SI NO SELECIONA UNA VERSION
        if version_ is None:
            page.open(
                alerta(
                    titulo= page.t("error_select_dialg_title"),
                    descripcion= page.t("error_select_dialg_description")
                    )
                )
            return
        
        #SI NO ES UNA VERSION VALIDA
        if not (page.launcher.set_version(version_)):
            page.open(
                alerta(
                    titulo= page.t("invalid_version"),
                    descripcion= f"{version_} {page.t('invalid_version_description')}"
                    )
                )
            return
        
        threading.Thread(target=page.launcher.start_minecraft(page), daemon=True).start()
    
    dropdown_language = ft.DropdownM2(
        label=page.t('lenguaje_dropdown'),
        hint_text=page.t('lenguaje_dropdown_description'),
        value=page.launcher.config.get("language"),
        options=[
            ft.dropdownm2.Option(key="es", content=
                ft.Text("Español")
            ),
            ft.dropdownm2.Option(key="en", content=
                ft.Text("English")
            )
        ],
        focused_color='white',
        border="underline",
        border_color=ft.Colors.TRANSPARENT,
        fill_color=ft.Colors.TRANSPARENT,
        bgcolor=ft.Colors.BLACK87,
        border_radius=3,
        label_style=ft.TextStyle(color=ft.Colors.WHITE, font_family='liberation', size=page.ancho*0.02)
    )
        
    
    content_menu = ft.Container(
        border=ft.border.all(1, page.color_init),
        expand=8,
        bgcolor=TYPES_COLORS[page.launcher.config.get("opacity")][2],
        margin=0,
        padding=5,
        alignment=ft.alignment.top_left
    )
    
    async def hover_bttn_play(e):
        boton_jugar.bgcolor =page.launcher.config.get("dark_color_schema") if boton_jugar.bgcolor == page.color_init else page.color_init
        boton_jugar.update()
        
    all_versions = page.launcher.versions
    boton_jugar = ft.FloatingActionButton(
        width=300,
        height=80,
        bgcolor=page.color_init,
        
        content=ft.Container(content=
            ft.Row
            (
                [
                    ft.Icon(ft.Icons.PLAY_ARROW),
                    text_play
                ], 
                alignment="center",
                spacing=5
            ),
            on_click=jugar_func,
            on_hover=hover_bttn_play
        , expand=True, padding=0),
        shape=ft.RoundedRectangleBorder(radius=5),
        mini=True,
    )
    page.boton_jugar = boton_jugar
    page.progress_time_remain = ft.Text(value="progess", visible=False, text_align=ft.TextAlign.CENTER, font_family="Monkey")
    page.progress_bar = ft.ProgressBar(
        value=0, 
        visible=False, 
        width=page.ancho/3, 
        height=page.alto/30, 
        bgcolor=ft.Colors.WHITE10, 
        border_radius=5, 
        color=page.color_init
    )

    color_picker = ColorPicker(color=page.color_init, width=page.ancho/4)
    text_color_picker = ft.Text(
        value=page.t('color_picker_text'),
        max_lines=2, size=page.ancho/60,
        text_align=ft.TextAlign.CENTER,
        font_family="liberation"
    )
    
    dropdown_versions = ft.DropdownM2(
        col=4,
        label=page.t('versions_dropdown_label'),
        item_height=50,
        value=f"{page.launcher.last_played_version[0]}",
        max_menu_height=300,
        hint_text=page.t('versions_dropdown'),
        options=[
            ft.dropdownm2.Option(key=e[0], data=e, content=
                ft.Row(controls=
                    [   
                        ft.Image(src="mc_icon.png" if not e[1] else "icono.png", width=30, height=30),
                        ft.Text(value=e[0], font_family='liberation', size=page.ancho*0.011, tooltip=tooltip_installation_needed if not e[1] else None )
                        
                    ], alignment=ft.MainAxisAlignment.START
                ),
                on_click=select_ver
            ) for e in all_versions
        ],
        width=page.ancho*0.35,
        focused_color='white',
        border="underline",
        border_color=ft.Colors.TRANSPARENT,
        fill_color=ft.Colors.WHITE10,
        bgcolor=ft.Colors.BLACK87,
        border_radius=3,
        label_style=ft.TextStyle(color=ft.Colors.WHITE, font_family='liberation', size=page.ancho*0.02)
    )
    
    home_button = ft.OutlinedButton(
        text=page.t("sections_main"),
        col=4,
        data='home',
        on_click=function_content,
        icon="HOME",
        icon_color=ft.Colors.WHITE,
        width=page.ancho/4,
        height=page.alto/10,
        
        
        style=ft.ButtonStyle(
            shape=ft.ContinuousRectangleBorder(3),
            color=ft.Colors.WHITE,
            side={
                    ft.ControlState.DEFAULT: ft.BorderSide(0, color=ft.Colors.TRANSPARENT),
                    ft.ControlState.HOVERED: ft.BorderSide(2, color=ft.Colors.WHITE10)
                },
            overlay_color=ft.Colors.BLACK12,
            icon_size=page.ancho/50,
            text_style=ft.TextStyle(
                size=page.ancho/50,
                font_family="Monkey",
                weight=ft.FontWeight.W_100,
            ),
    )   )
    
    settings_button = ft.OutlinedButton(
        text=page.t("sections_settings"),
        data="settings",
        col=4,
        on_click=function_content,
        icon="SETTINGS", 
        icon_color=ft.Colors.WHITE,
        width=page.ancho/4,
        height=page.alto/10,
        
        style=ft.ButtonStyle(
            shape=ft.ContinuousRectangleBorder(3),
            color=ft.Colors.WHITE,
            side={
                    ft.ControlState.DEFAULT: ft.BorderSide(0, color=ft.Colors.TRANSPARENT),
                    ft.ControlState.HOVERED: ft.BorderSide(2, color=ft.Colors.WHITE10)
                },
            overlay_color=ft.Colors.BLACK26,
            icon_size=page.ancho/50,
            text_style=ft.TextStyle(
                size=page.ancho/50,
                font_family="Monkey",
                weight=ft.FontWeight.W_100,
            ),
            
            
        )
    )
    
    perfil_button = ft.OutlinedButton(
        text=page.t("sections_profile"),
        icon="PERSON",
        col=4,
        data="perfil",
        on_click=function_content,
        icon_color=ft.Colors.WHITE,
        width=page.ancho/4,
        height=page.alto/10,
        
        style=ft.ButtonStyle(
            shape=ft.ContinuousRectangleBorder(3),
            color=ft.Colors.WHITE,
            side={
                ft.ControlState.DEFAULT: ft.BorderSide(0, color=ft.Colors.TRANSPARENT),
                ft.ControlState.HOVERED: ft.BorderSide(2, color=ft.Colors.WHITE10)
                },
            overlay_color=ft.Colors.BLACK12,
            icon_size=page.ancho/50,
            text_style=ft.TextStyle(
                size=page.ancho/50,
                font_family="Monkey",
                weight=ft.FontWeight.W_100,
            )
            
        )
    )
    
    content_sections = ft.Container(
        expand=1,
        border_radius=ft.BorderRadius(5, 5, 0, 0),
        bgcolor=TYPES_COLORS[page.launcher.config.get("opacity")][1],
        content=
        ft.ResponsiveRow(
            controls=[
                home_button,
                perfil_button,
                settings_button     
            ], 
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ), alignment=ft.alignment.center
        
    )
    
    content_sidebar = ft.Container(
        margin=ft.Margin(0, 10, 0, 0),
        border_radius=5,
        expand=2,
        content=ft.ResponsiveRow(
            controls=[
                dropdown_versions,#Lista de versiones
                ft.Column(
                    col=4,
                    controls=[
                        page.progress_bar,
                        page.progress_time_remain
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER
        ), 
        padding=10,
        bgcolor=TYPES_COLORS[page.launcher.config.get("opacity")][2]
    )
    
    return ft.View(
        "/",
        controls=[
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.TRANSPARENT,
                content=ft.Column(
                    controls=[
                        content_sections,
                        content_menu,
                        content_sidebar
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                    run_spacing=0
                ),
            )
        ],
        decoration=ft.BoxDecoration(
            image=ft.DecorationImage( 
                src=page.launcher.config.get("wallpaper_launcher"), 
                fit=ft.ImageFit.COVER,
                opacity= 0.8
            ),
        ),
        bgcolor=ft.Colors.TRANSPARENT,
        floating_action_button=boton_jugar,
        floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT,
    )
