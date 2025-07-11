import os
import threading
import flet as ft
from flet_route import Params,Basket
from Utils import versiones, iniciar_minecraft_no_premium, alerta, alerta_good, valid_version

async def MainView(page:ft.Page, params:Params, basket:Basket):
    
    async def clr_data_modal(e):
        await page.client_storage.clear_async()
        page.window.close()
    
    async def delte_all_data(e):
        alrt = ft.AlertDialog(
            icon=ft.Icon(name=ft.Icons.WARNING_AMBER),
            title=ft.Text(value=page.trad["data_elimination"][page.lenguage], text_align=ft.TextAlign.CENTER),
            content=ft.Text(value=page.trad["data_elimination_sure"][page.lenguage], text_align=ft.TextAlign.CENTER),
            actions=[
                ft.TextButton(page.trad["data_question_y"][page.lenguage], on_click=clr_data_modal),
                ft.TextButton("No", on_click=lambda e: page.close(alrt)),
            ],
            bgcolor=ft.Colors.BLACK,
            shape=ft.BeveledRectangleBorder(3),
            icon_color=ft.Colors.ORANGE,
            alignment=ft.alignment.center,
        )
        page.open(
            alrt
        )
    
    async def save_settings(e):
        changes_ = []
        
        #JAVA PATH
        if not os.path.isfile(java_path.value):
            page.open(
                await alerta(
                    titulo= "Error",
                    descripcion= page.trad["file_not_found"][page.lenguage]
                )
            )
            return
        else:
            if page.java_path != java_path.value:
                page.java_path = java_path.value
                await page.client_storage.set_async("java_path", page.java_path)
                changes_.append("Java Path")
        
        #RAM
        if page.ram_usage != round(ram_slider.value):
            page.ram_usage = round(ram_slider.value)
            await page.client_storage.set_async("ram_usage", page.ram_usage)
        

            page.jvw_args = f"-Xmx{page.ram_usage}G -Xms{page.ram_usage}G --enable-native-access=ALL-UNNAMED".split(" ")
            await page.client_storage.set_async("jvw_args", page.jvw_args)
            changes_.append("RAM")
        
        #DISCORD
        if page.discord_presence_allow != discord_presence_allow.value:
            page.discord_presence_allow = discord_presence_allow.value
            await page.client_storage.set_async("discord_presence_allow", page.discord_presence_allow)
            changes_.append("Discord")
            if page.discord_presence_allow:
                page.presence.set(
                    {
                    "state": page.trad["user_state_discord_mainpage"][page.lenguage],
                    "details": f"{page.username} {page.trad["user_state_discord_conect"][page.lenguage]}",
                    "timestamps": {"start": page.times},
                    }
                )
            else:
                page.presence.close()
        
        #WALLPAPER
        if page.wallpaper_launcher != wallpaper_widget.src:
            page.wallpaper_launcher = wallpaper_widget.src
            page.views[0].decoration.image.src = page.wallpaper_launcher
            page.views[0].update()
            await page.client_storage.set_async("wallpaper_launcher", page.wallpaper_launcher)
            changes_.append("Wallpaper")
        
        #LENGUAJE
        if lenguaje_control.value != page.lenguage:
            page.lenguage = int(lenguaje_control.value)
            await page.client_storage.set_async("lenguaje", int(lenguaje_control.value))
            changes_.append("Lenguage")
        
        #SAVE
        if len(changes_) == 0:
            return
        page.open(
            await alerta_good(
                titulo= page.trad["settings_saved"][page.lenguage],
                descripcion= f"{page.trad['setting_saved_description'][page.lenguage]}:\n {','.join(changes_)}"
                )
            )
    
    async def close_session(e):
        page.open(
            await alerta_good(
                titulo= page.trad["session_closed"][page.lenguage],
                descripcion= f"{page.trad['session_closed_description'][page.lenguage]} {page.username}"
            )
        )
        
        await page.client_storage.remove_async("username")
        page.username = None
        
        page.go("/login")
        
    
    async def select_ver(e:ft.ControlEvent):
        pass
    
    
    #BUTTON
    async def bttn_select_java_bin(e):
        filepicker_javaw.pick_files(f"{page.trad['select_javaw'][page.lenguage]} javaw.exe", allowed_extensions=["exe"])
        
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
    
    async def bttn_img_wallpaper(e):
        filepicker_wallapaper.pick_files(page.trad['select_img_wallpaper'][page.lenguage], allowed_extensions=["jpg", "png", "jpeg"])
    
    #WIDGETS
    java_path = ft.TextField(
        cursor_color=ft.Colors.ORANGE,
        label="Java",
        bgcolor=ft.Colors.TRANSPARENT,
        width=page.ancho*0.30,
        height=page.alto*0.10,
        border=ft.InputBorder.NONE,
        filled=True,
        value=page.java_path,
        fill_color=ft.Colors.TRANSPARENT,
        max_lines=1,
        border_radius=3,
        focused_border_color=ft.Colors.WHITE,
        label_style=ft.TextStyle(color=ft.Colors.WHITE,font_family='liberation', size=page.ancho*0.018),
        multiline=True,
        suffix= ft.IconButton(icon=ft.Icons.FOLDER, icon_color=ft.Colors.ORANGE, padding=0, hover_color=ft.Colors.BLACK12, on_click=bttn_select_java_bin),
        expand=True,
    )
    
    ram_slider = ft.Slider(min=2, max=16, round=0, value=page.ram_usage, divisions=14, width=page.ancho*0.40, label="{value}GB", active_color="#f79824")
    
    discord_presence_allow = ft.Switch(value=page.discord_presence_allow, active_color="#f79824", inactive_track_color="#ffd683", inactive_thumb_color="#a0844c")
    
    wallpaper_widget = ft.Image(src=page.wallpaper_launcher, width=page.ancho*0.10, height=page.alto*0.10, border_radius=10)
    filepicker_wallapaper = ft.FilePicker(on_result=select_img_wallpaper)
    filepicker_javaw = ft.FilePicker(on_result=filepicker_select_bin_javaw)
    page.overlay.append(filepicker_javaw)
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
            selected_button.style.side = ft.BorderSide(1, color=ft.Colors.ORANGE, stroke_align=ft.BorderSideStrokeAlign.INSIDE)
            page.update()
        
        if selected_button.data == 'settings':
            content_menu.alignment= ft.alignment.top_left
            content_menu.content= ft.Column(
                controls=[
                    
                    ft.Container(expand=9, padding=15, content=
                        ft.Column(
                            wrap=True, spacing=10, run_spacing=10,
                            controls=[
                                ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, content=java_path),
                                ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, content=lenguaje_control),
                                ft.Container(border=ft.border.all(1, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, padding=5, content=
                                    ft.Text(
                                        selectable=True,
                                        text_align=ft.TextAlign.CENTER,
                                        value=f"{page.trad['java_recommended'][page.lenguage]}\n",
                                        spans=[
                                            ft.TextSpan(
                                                "Link Java",
                                                ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE, color=ft.Colors.ORANGE),
                                                url="https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html"
                                            )
                                        ]
                                    )
                                ),
                                ft.Container(border=ft.border.all(1, ft.Colors.BLACK), padding=10, bgcolor=ft.Colors.WHITE10, content=
                                    ft.Column(
                                        controls=[
                                            ft.Text(page.trad['discord_rich'][page.lenguage], max_lines=2, size=page.ancho/70, text_align=ft.TextAlign.CENTER, font_family="liberation"),
                                            discord_presence_allow
                                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, height=page.ancho/5, width=page.ancho*0.14
                                    )
                                ),
                                ft.Container(border=ft.border.all(2, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, content=
                                    ft.Column(
                                        controls=[
                                            ft.Text(page.trad['ram_usage'][page.lenguage], max_lines=2, size=page.ancho/70, text_align=ft.TextAlign.CENTER, font_family="liberation"),
                                            ram_slider,
                                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, height=page.ancho/10, width=page.ancho*0.28
                                    )
                                ),
                                ft.Container(border=ft.border.all(2, ft.Colors.BLACK), bgcolor=ft.Colors.WHITE10, content=
                                    ft.Column(
                                        controls=[
                                            ft.Text(page.trad['wallpaper_save'][page.lenguage], max_lines=2, size=page.ancho/70, text_align=ft.TextAlign.CENTER, font_family="liberation"),
                                            ft.Row(controls=
                                                [
                                                    wallpaper_widget,
                                                    ft.TextButton(text=f"{page.trad['select_javaw'][page.lenguage]}", icon=ft.Icons.REFRESH_ROUNDED, on_click=bttn_img_wallpaper, style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE, color=ft.Colors.BLACK))
                                                
                                                ], vertical_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER
                                            )
                                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, height=page.ancho/10, width=page.ancho*0.28
                                    )
                                ),
                                
                            ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ),
                
                    ft.Container(expand=1, content=
                        ft.Row(
                            controls=[
                                ft.OutlinedButton(
                                    
                                    content=ft.Text(value=page.trad['save_'][page.lenguage], font_family="lokeya", size=page.ancho/60, text_align=ft.TextAlign.CENTER),
                                    width=page.ancho*0.10,
                                    height=page.alto*0.07,
                                    on_click=save_settings,
                                    style=ft.ButtonStyle(
                                        shape=ft.BeveledRectangleBorder(0),
                                        overlay_color=ft.Colors.WHITE10,
                                        color={
                                            ft.ControlState.DEFAULT: ft.Colors.WHITE,
                                            ft.ControlState.HOVERED: ft.Colors.ORANGE,
                                            ft.ControlState.FOCUSED: ft.Colors.DEEP_ORANGE_ACCENT},
                                        bgcolor=ft.Colors.WHITE10
                                        
                                        ),
                                    ),
                                ft.OutlinedButton(
                                    
                                    content=ft.Text(value=page.trad['restore_'][page.lenguage], font_family="lokeya", size=page.ancho/60, text_align=ft.TextAlign.CENTER),
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
                                    
                                    content=ft.Text(value=page.trad['delete_all_'][page.lenguage], font_family="lokeya", size=page.ancho/70, text_align=ft.TextAlign.CENTER),
                                    width=page.ancho*0.10,
                                    height=page.alto*0.07,
                                    tooltip=page.trad['delete_all_confirmation_'][page.lenguage],
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
            page.Text_Console = ft.ListView(
                controls=
                    [
                        ft.Text(font_family="console", value=page.trad['console_msg'][page.lenguage], size=page.ancho/65, selectable=True, expand=True)
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
                content=page.Text_Console
            )
            
            
            
        if selected_button.data == 'perfil':
            content_menu.alignment= ft.alignment.center
            content_menu.content= ft.Column(
                controls=[
                    ft.Image(
                        filter_quality=ft.FilterQuality.MEDIUM,
                        anti_alias=True,
                        fit=ft.ImageFit.CONTAIN,
                        src=page.photo_perfil_path,
                        border_radius=(page.ancho*0.35)/2,
                        width=page.ancho*0.25, height=page.alto*0.25
                    ),
                    ft.Container(
                        content=ft.Text(
                            selectable=True,
                            value=page.username ,
                            font_family="liberation", 
                            size=page.ancho/30,
                        ), 
                        bgcolor=ft.Colors.BLACK12,
                        border_radius=10,
                        ink=True, 
                        padding=5
                    ),
                    ft.OutlinedButton(
                                    
                        content=ft.Text(value=page.trad['session_close'][page.lenguage], font_family="liberation", size=page.ancho/40, text_align=ft.TextAlign.CENTER),
                        width=page.ancho*0.20,
                        height=page.alto*0.10,
                        on_click=close_session,
                        style=ft.ButtonStyle(
                            shape=ft.BeveledRectangleBorder(0),
                            overlay_color=ft.Colors.WHITE10,
                            color={
                                ft.ControlState.DEFAULT: ft.Colors.WHITE,
                                ft.ControlState.HOVERED: ft.Colors.ORANGE,
                                ft.ControlState.FOCUSED: ft.Colors.DEEP_ORANGE_ACCENT},
                            bgcolor=ft.Colors.WHITE10
                            
                            ),
                        )    
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        
        page.update()
    
        
    async def jugar_func(e):
        version_ = list_vers.value
        
        #SI NO SELECIONA UNA VERSION
        if version_ is None:
            page.open(
                await alerta(
                    titulo= page.trad["error_select_dialg_title"][page.lenguage],
                    descripcion= page.trad["error_select_dialg_description"][page.lenguage]
                    )
                )
            return
        
        #SI NO ES UNA VERSION VALIDA
        if not await valid_version(version_):
            page.open(
                await alerta(
                    titulo= page.trad["invalid_version"][page.lenguage],
                    descripcion= f"{version_} {page.trad['invalid_version_description'][page.lenguage]}"
                    )
                )
            return
        
        page.presence.set(
            {
            "state": f"{page.trad["user_state_discord_playing"][page.lenguage]} {version_}",
            "details": f"{page.username} {page.trad["user_state_discord_conect"][page.lenguage]}",
            "timestamps": {"start": page.times},
            }
        )
        
        await page.client_storage.set_async("select_version", version_)
        page.select_version = version_
        threading.Thread(target=await iniciar_minecraft_no_premium(name=f"{page.username}", version=f"{version_}", page=page), daemon=True).start()
    
    lenguaje_control = ft.DropdownM2(
        label=page.trad['lenguaje_dropdown'][page.lenguage],
        hint_text=page.trad['lenguaje_dropdown_description'][page.lenguage],
        value=page.lenguage,
        options=[
            ft.dropdownm2.Option(key=0, content=
                ft.Text("Español")
            ),
            ft.dropdownm2.Option(key=1, content=
                ft.Text("English")
            )
        ],
        width=page.ancho*0.30,
        focused_color='white',
        border="underline",
        border_color=ft.Colors.TRANSPARENT,
        fill_color=ft.Colors.TRANSPARENT,
        bgcolor=ft.Colors.BLACK87,
        border_radius=3,
        label_style=ft.TextStyle(color=ft.Colors.WHITE, font_family='liberation', size=page.ancho*0.02)
    )
        
    
    content_menu = ft.Container(
        border=ft.border.all(1, ft.Colors.ORANGE_300),
        expand=8,
        bgcolor=ft.Colors.BLACK87,
        margin=0,
        padding=10,
        alignment=ft.alignment.top_left
    )
    
    async def hover_bttn_play(e):
        boton_jugar.bgcolor ="#ff7900" if boton_jugar.bgcolor == "#f79824" else "#f79824"
        boton_jugar.update()
    
    all_versions = versiones()
    boton_jugar = ft.FloatingActionButton(
        width=300,
        height=80,
        bgcolor="#f79824",
        content=ft.Container(content=
            ft.Row
            (
                [
                    ft.Icon(ft.Icons.PLAY_ARROW),
                    ft.Text(page.trad["play_button"][page.lenguage], size=page.ancho/30,font_family='katana', text_align=ft.TextAlign.CENTER)
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
    
    page.progress_bar = ft.ProgressBar(value=0, visible=False, width=page.ancho/3, height=page.alto/30, bgcolor=ft.Colors.WHITE10, border_radius=5, color=ft.Colors.ORANGE)
    list_vers = ft.DropdownM2(
        label=page.trad['versions_dropdown_label'][page.lenguage],
        item_height=50,
        value=page.select_version,
        max_menu_height=300,
        hint_text=page.trad['versions_dropdown'][page.lenguage],
        options=[
            ft.dropdownm2.Option(key=e[0], content=
                ft.Row(controls=
                    [   
                        ft.Image(src="mc_icon.png" if not e[1] else "icono.png", width=30, height=30),
                        ft.Text(value=e[0], font_family='liberation', size=page.ancho*0.011, tooltip=ft.Tooltip(message=page.trad['installation_needed'][page.lenguage]) if not e[1] else None )
                        
                    ], alignment=ft.MainAxisAlignment.START
                ),
                on_click=select_ver
            ) for e in await all_versions
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
        f"{page.trad["sections_main"][page.lenguage]}",
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
                ft.ControlState.HOVERED: ft.BorderSide(2, color=ft.Colors.WHITE10),
                
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
    
    settings_button = ft.OutlinedButton(
        f"{page.trad["sections_settings"][page.lenguage]}",
        data="settings",
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
        f"{page.trad["sections_profile"][page.lenguage]}",
        icon="PERSON",
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
                        ft.Row(
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
                        content=ft.Row(
                            controls=[
                                list_vers,
                                page.progress_bar#Lista de versiones
                            ], alignment=ft.MainAxisAlignment.START
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
                src= page.wallpaper_launcher, 
                fit=ft.ImageFit.COVER,
                opacity= 0.8
                ),
            
            ),
        bgcolor=ft.Colors.TRANSPARENT,
        floating_action_button=boton_jugar,
        floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT,
    )
