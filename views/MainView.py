import threading
import flet as ft
from flet_route import Params,Basket
from flet_contrib.color_picker import ColorPicker
from Tools import generar_degradado, alerta

async def MainView(page:ft.Page, params:Params, basket:Basket):
    
    async def clr_data_modal(e):
        page.launcher.config.reset()
        page.window.close()
    
    async def delte_all_data(e):
        alrt = ft.AlertDialog(
            icon=ft.Icon(name=ft.Icons.WARNING_AMBER),
            title=ft.Text(value=page.t("data_elimination"), text_align=ft.TextAlign.CENTER),
            content=ft.Text(value=page.t("data_elimination_sure"), text_align=ft.TextAlign.CENTER),
            actions=[
                ft.TextButton(page.t("data_question_y"), on_click=clr_data_modal),
                ft.TextButton("No", on_click=lambda e: page.close(alrt)),
            ],
            bgcolor=ft.Colors.BLACK,
            shape=ft.BeveledRectangleBorder(3),
            icon_color=page.launcher.config.get("primary_color_schema"),
            alignment=ft.alignment.center,
        )
        page.open(
            alrt
        )
    
    async def save_settings(e):
        changes_ = []
        global need_restart
        need_restart = False
        
        
        #JAVA PATH
        if not page.launcher.set_java(java_path.value, False):
            page.open(
                alerta(
                    titulo= "Error",
                    descripcion= page.t("file_not_found")
                )
            )
            return

        if page.launcher.java_path != java_path.value:
            page.launcher.set_java(java_path.value)
            changes_.append("Java dir")
        
        #MINECRAFT PATH
        if minecraft_path.value != page.launcher.minecraft_path:
            page.launcher.set_minecraft_path(minecraft_path.value)
            changes_.append("Minecraft dir")
            need_restart = True
        
        #RAM
        if page.launcher.config.get("ram") != round(ram_slider.value):
            page.launcher.config.set("ram", round(ram_slider.value))
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
        if page.launcher.config.get("wallpaper_launcher") != wallpaper_widget.src:
            page.launcher.config.set("wallpaper_launcher", wallpaper_widget.src)
            
            page.views[0].decoration.image.src = wallpaper_widget.src
            page.views[0].update()
            changes_.append("Wallpaper")
        
        #COLOR PICKER
        if page.launcher.config.get("primary_color_schema") != color_picker.color:
            degrados = generar_degradado(color_picker.color)
            
            page.launcher.config.set("primary_color_schema", color_picker.color)
            page.launcher.config.set("light_color_schema", degrados[1])
            page.launcher.config.set("dark_color_schema", degrados[0])
            
            changes_.append("Thema")
        
        #LENGUAJE
        if page.launcher.config.get("language") != language_control.value:
            page.launcher.config.set("language", language_control.value)
            changes_.append("Language")
            
            need_restart = True
        
        #SAVE
        if len(changes_) == 0:
            return
        
        page.launcher.config.save()
        
        if need_restart:
            page.open(
                
                ft.BottomSheet(
                    animation_style=ft.AnimationStyle(curve=ft.AnimationCurve.BOUNCE_IN, duration=300),
                    content=
                    ft.Container(
                        ft.Column(
                            [
                                ft.Text(value=page.t("need_restart"), font_family="liberation", size=page.ancho/70,),
                                ft.ElevatedButton("Restart", on_click=lambda _: page.window.close(), color=page.launcher.config.get("primary_color_schema")),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            tight=True,
                        ),
                        padding=50,
                    ),
                    dismissible=False, bgcolor=ft.Colors.BLACK87
                ) 
            )
        else:
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
                    ft.TextButton(page.t("data_question_y"), data=version,on_click=install_minecraft_version),
                    ft.TextButton("No", on_click=dismiss_installation)
                ],
                bgcolor=ft.Colors.BLACK,
                shape=ft.BeveledRectangleBorder(3),
                icon_color=page.launcher.config.get("primary_color_schema"),
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
        wallpaper_widget.src = e.files[0].path
        
        wallpaper_widget.update()
    
    #FILEPICKER WIDGET
    async def filepicker_select_bin_javaw(e:ft.FilePickerResultEvent):
        if e.files is None:
            return
        
        java_path.value = e.files[0].path
        java_path.update()
        
    async def filepicker_select_minecraft_path(e:ft.FilePickerResultEvent):
        if not e.path:
            return

        minecraft_path.value = e.path
        minecraft_path.update()
    
    async def ram_change_function(e):
        ram_text.value = f"{round(ram_slider.value)} GB"
        ram_text.update()
    
    async def bttn_img_wallpaper(e):
        filepicker_wallapaper.pick_files(page.t('select_img_wallpaper'), allowed_extensions=["jpg", "png", "jpeg"])
    
    #WIDGETS
    java_path = ft.TextField(
        cursor_color=page.launcher.config.get("primary_color_schema"),
        label="Java",
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
        suffix= ft.IconButton(icon=ft.Icons.FOLDER, icon_color=page.launcher.config.get("primary_color_schema"), padding=0, hover_color=ft.Colors.BLACK12, on_click=bttn_select_java_bin),
        expand=True,
    )
    
    minecraft_path = ft.TextField(
        cursor_color=page.launcher.config.get("primary_color_schema"),
        label="Minecraft Dir",
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
        suffix= ft.IconButton(icon=ft.Icons.FOLDER, icon_color=page.launcher.config.get("primary_color_schema"), padding=0, hover_color=ft.Colors.BLACK12, on_click=bttn_check_minecraft_path),
        expand=True,
    )
    
    ram_slider = ft.Slider(
        on_change=ram_change_function,
        min=2,
        max=16,
        round=0,
        value=page.launcher.config.get("ram"),
        divisions=14,
        label="{value}GB",
        active_color=page.launcher.config.get("primary_color_schema")
    )
    ram_text = ft.Text(
        font_family="Monkey",
        size=page.ancho/65,
        color=page.launcher.config.get("primary_color_schema"),
        value=f'{page.launcher.config.get("ram")} GB'
    )
    discord_presence_allow = ft.Switch(
        value=page.launcher.config.get("discord_presence"),
        active_color=page.launcher.config.get("primary_color_schema"),
        inactive_track_color=page.launcher.config.get("light_color_schema"),
        inactive_thumb_color=page.launcher.config.get("dark_color_schema")
    )
    
    wallpaper_widget = ft.Image(
        src=page.launcher.config.get("wallpaper_launcher"),
        width=page.ancho*0.10,
        height=page.alto*0.10,
        border_radius=10
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
            selected_button.style.bgcolor = ft.Colors.BLACK54
            selected_button.style.side = ft.BorderSide(1, color=page.launcher.config.get("primary_color_schema"), stroke_align=ft.BorderSideStrokeAlign.INSIDE)
            page.update()
        
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
                                    ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, content=java_path, margin=0),
                                    ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, content=minecraft_path, margin=0),
                                    ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, content=language_control, margin=0),
                                    ft.Container(border=ft.border.all(2, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, padding=5, content=
                                        ft.Column(
                                            controls=[
                                                ft.Text(page.t('ram_usage'), max_lines=2, size=page.ancho/70, text_align=ft.TextAlign.CENTER, font_family="liberation"),
                                                ram_slider,
                                                ram_text
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
                                                        ft.Text(page.t('discord_rich'), max_lines=2, size=page.ancho/70, text_align=ft.TextAlign.CENTER, font_family="liberation"),
                                                        discord_presence_allow
                                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER
                                                ), margin=0, alignment=ft.alignment.center
                                            ),
                                            ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, padding=10, margin=0, content=ft.Column(
                                                controls=[
                                                    ft.Text(page.t('wallpaper_save'), max_lines=2, size=page.ancho/70, text_align=ft.TextAlign.CENTER, font_family="liberation"),
                                                    ft.Row(controls=
                                                        [
                                                            wallpaper_widget,
                                                            ft.IconButton(icon=ft.Icons.EDIT, on_click=bttn_img_wallpaper, bgcolor=ft.Colors.TRANSPARENT, icon_color=page.launcher.config.get("primary_color_schema"))
                                                            ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER
                                                        ),
                                                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                                )
                                            )
                                        ], col=3, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                ),
                                
                                
                                ft.Container(col=4, border=ft.border.all(1, ft.Colors.BLACK), padding=10, bgcolor=ft.Colors.WHITE10, content=
                                    ft.Column(
                                        controls=[
                                            ft.Text(page.t('color_picker_text'), max_lines=2, size=page.ancho/70, text_align=ft.TextAlign.CENTER, font_family="liberation"),
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
                                ft.OutlinedButton(
                                    
                                    content=ft.Text(value=page.t('save_'), font_family="lokeya", size=page.ancho/60, text_align=ft.TextAlign.CENTER),
                                    width=page.ancho*0.10,
                                    height=page.alto*0.07,
                                    on_click=save_settings,
                                    style=ft.ButtonStyle(
                                        shape=ft.BeveledRectangleBorder(0),
                                        overlay_color=ft.Colors.WHITE10,
                                        color={
                                            ft.ControlState.DEFAULT: ft.Colors.WHITE,
                                            ft.ControlState.HOVERED: page.launcher.config.get("primary_color_schema"),
                                            },
                                        bgcolor=ft.Colors.WHITE10
                                        
                                        ),
                                    ),
                                ft.OutlinedButton(
                                    
                                    content=ft.Text(value=page.t('restore_'), font_family="lokeya", size=page.ancho/60, text_align=ft.TextAlign.CENTER),
                                    width=page.ancho*0.10,
                                    height=page.alto*0.07,
                                    style=
                                        ft.ButtonStyle(
                                            shape=ft.BeveledRectangleBorder(0),
                                            overlay_color=ft.Colors.WHITE10,
                                            color={
                                                ft.ControlState.DEFAULT: ft.Colors.WHITE,
                                                ft.ControlState.HOVERED: ft.Colors.RED,
                                                ft.ControlState.FOCUSED: ft.Colors.RED_ACCENT_100},
                                            bgcolor=ft.Colors.WHITE10
                                        ),
                                    disabled=True
                                    ),
                                ft.OutlinedButton(
                                    
                                    content=ft.Text(value=page.t('delete_all_'), font_family="lokeya", size=page.ancho/70, text_align=ft.TextAlign.CENTER),
                                    width=page.ancho*0.10,
                                    height=page.alto*0.07,
                                    tooltip=page.t('delete_all_confirmation_'),
                                    style=ft.ButtonStyle(
                                        shape=ft.BeveledRectangleBorder(0),
                                        overlay_color=ft.Colors.WHITE10,
                                        color={
                                            ft.ControlState.DEFAULT: ft.Colors.WHITE,
                                            ft.ControlState.HOVERED: ft.Colors.RED,
                                            ft.ControlState.FOCUSED: ft.Colors.RED_ACCENT_100},
                                        bgcolor=ft.Colors.WHITE10
                                        
                                        ),
                                    on_click=delte_all_data
                                    ),
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
                            ft.Text(font_family="console", value=page.t('console_msg'), size=page.ancho/65, selectable=True, expand=True)
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
                    ft.Image(
                        filter_quality=ft.FilterQuality.MEDIUM,
                        anti_alias=True,
                        fit=ft.ImageFit.CONTAIN,
                        src=page.launcher.config.get("photo_perfil"),
                        border_radius=(page.ancho*0.35)/2,
                        width=page.ancho*0.25, height=page.alto*0.25
                    ),
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
                    ft.OutlinedButton(
                                    
                        content=ft.Text(value=page.t('session_close'), font_family="liberation", size=page.ancho/40, text_align=ft.TextAlign.CENTER),
                        width=page.ancho*0.20,
                        height=page.alto*0.10,
                        on_click=close_session,
                        style=ft.ButtonStyle(
                            shape=ft.BeveledRectangleBorder(0),
                            overlay_color=ft.Colors.WHITE10,
                            color={
                                ft.ControlState.DEFAULT: ft.Colors.WHITE,
                                ft.ControlState.HOVERED: page.launcher.config.get("primary_color_schema"),
                                },
                            bgcolor=ft.Colors.WHITE10
                            
                            ),
                        )    
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
    
    language_control = ft.DropdownM2(
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
        border=ft.border.all(1, page.launcher.config.get("primary_color_schema")),
        expand=8,
        bgcolor=ft.Colors.BLACK87,
        margin=0,
        padding=5,
        alignment=ft.alignment.top_left
        )
    
    async def hover_bttn_play(e):
        boton_jugar.bgcolor =page.launcher.config.get("dark_color_schema") if boton_jugar.bgcolor == page.launcher.config.get("primary_color_schema") else page.launcher.config.get("primary_color_schema")
        boton_jugar.update()
        
    all_versions = page.launcher.versions
    boton_jugar = ft.FloatingActionButton(
        width=300,
        height=80,
        bgcolor=page.launcher.config.get("primary_color_schema"),
        
        content=ft.Container(content=
            ft.Row
            (
                [
                    ft.Icon(ft.Icons.PLAY_ARROW),
                    ft.Text(page.t("play_button"), size=page.ancho/30,font_family='katana', text_align=ft.TextAlign.CENTER)
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
        color=page.launcher.config.get("primary_color_schema")
    )

    color_picker = ColorPicker(color=page.launcher.config.get("primary_color_schema"))
    list_vers = ft.DropdownM2(
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
                        ft.Text(value=e[0], font_family='liberation', size=page.ancho*0.011, tooltip=ft.Tooltip(message=page.t('installation_needed')) if not e[1] else None )
                        
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
        f"{page.t("sections_main")}",
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
        f"{page.t("sections_settings")}",
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
            overlay_color=ft.Colors.BLACK12,
            icon_size=page.ancho/50,
            text_style=ft.TextStyle(
                size=page.ancho/50,
                font_family="Monkey",
                weight=ft.FontWeight.W_100,
            ),
            
            
        )
    )
    
    perfil_button = ft.OutlinedButton(
        f"{page.t("sections_profile")}",
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
    
    return ft.View(
        "/",
        controls=[
            ft.Container(expand=True, bgcolor=ft.Colors.BLACK38, border_radius=5, content=ft.Column(
                controls=[
                    ft.Container(
                        border_radius=5,
                        expand=1,
                        bgcolor=ft.Colors.BLACK12,
                        margin=ft.Margin(3, 3, 3, 0),
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
                        
                    ),
                    content_menu,
                    ft.Container(
                        margin=ft.Margin(0, 10, 0, 0),
                        border_radius=5,
                        expand=2,
                        content=ft.ResponsiveRow(
                            controls=[
                                list_vers,#Lista de versiones
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
                        bgcolor=ft.Colors.BLACK87
                    )
                ], expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                run_spacing=0
            ))
            
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
