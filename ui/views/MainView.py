import flet as ft
from flet_route import Params,Basket

from core.utils import TYPES_COLORS, alerta, DEFAULT_SIDE

from ui.components.dropdown import DropdownVersions
from ui.components.tooltip import Tooltip_installation
from ui.components.button import ButtonPlay, ButtonsSections

from ui.sections.Modrinth import Modrinth
from ui.sections.Settings import Settings
from ui.sections.Perfil import Perfil

async def MainView(page:ft.Page, params:Params, basket:Basket):
        
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
                    descripcion= f"{version_[0]} {page.t('invalid_version_description')}"
                    )
                )
            return
        
        
        page.run_thread(page.launcher.start_minecraft, page)
    
    #FILEPICKER WIDGET
            
    async def __dismiss_installation(e):
        page.close(page.overlay[-1]) 
        page.button_play.disabled = True
        page.button_play.content.content.controls[1].value = page.t("version_not_installed")
        page.button_play.update()

    async def __install_minecraft_version(e):
        page.close(page.overlay[-1])
        page.button_play.disabled = True
        page.button_play.content.content.controls[1].value = page.t("play_button_installing")
        page.button_play.update()
        page.launcher.instalar_minecraft_en_hilo(page, e.control.data)

    async def select_ver(e:ft.ControlEvent):
        installed = page.launcher.set_version(e.control.data)
        version = e.control.data[0]
        
        if not installed:
            page.option_change_installed = e.control
            alrt = ft.AlertDialog(
                icon=ft.Icon(
                    name=ft.Icons.WARNING_AMBER
                ),
                title=ft.Text(
                    value=page.t('installation_sucess'),
                    text_align=ft.TextAlign.CENTER
                ),
                content=ft.Text(
                    value=f"{version} {page.t('installation_sucess_description')}",
                    text_align=ft.TextAlign.CENTER
                ),
                actions=[
                    ft.TextButton(
                        text=page.t("data_question_y"),
                        data=version,
                        on_click=__install_minecraft_version,
                        style=ft.ButtonStyle(
                            color=page.color_init
                        )
                    ),
                    ft.TextButton(
                        text="No",
                        on_click=__dismiss_installation,
                        style=ft.ButtonStyle(
                            color=page.color_init
                        )
                    )
                ],
                bgcolor=ft.Colors.BLACK,
                shape=ft.BeveledRectangleBorder(3),
                icon_color=page.color_init,
                alignment=ft.alignment.center,
            )
            page.open(alrt)
        
    #WIDGETS
    page.tooltip_installation_needed = Tooltip_installation(page).get()
    page.text_play = ft.Text(
        value=page.t("play_button"),
        size=page.ancho/30,
        font_family='katana',
        text_align=ft.TextAlign.CENTER
    )
    page.borderside_sections = ft.BorderSide(1, color=page.color_init, stroke_align=ft.BorderSideStrokeAlign.INSIDE)
    
    #END WIDGETS
    
    def reset_button_style(btn):
        btn.style.bgcolor = None
        btn.style.side = DEFAULT_SIDE
        btn.update()
        
    async def open_console(e):
        page.current_section = 'console'
        page.open(
            ft.AlertDialog(
                content=ft.Container(
                    content=page.Text_Console,
                    bgcolor=ft.Colors.WHITE10,
                    border_radius=5,
                    expand=True,
                    width=page.ancho,
                    height=page.alto
                ),
                icon=ft.Icon(name=ft.Icons.MONITOR_HEART_OUTLINED, color=page.color_init),
                bgcolor=ft.Colors.BLACK87,
                shape=ft.BeveledRectangleBorder(3)
            )
        )
    
    async def function_content(e):
        if e.control.data == page.current_section:
            return

        # Mapa de botones (guardar fuera si quieres aún más rápido)
        button_map = {
            'perfil': page.perfil_button,
            'settings': page.settings_button,
            'modrinth': page.modrinth_button
        }

        # Resetear solo el botón anterior
        if page.current_section in button_map:
            reset_button_style(button_map[page.current_section])

        # Activar el nuevo
        selected_button = button_map.get(e.control.data)
        if selected_button:
            selected_button.style.bgcolor = TYPES_COLORS[page.launcher.config.get("opacity")][0]
            selected_button.style.side = page.borderside_sections
            selected_button.update()

        # Guardar como sección actual
        page.current_section = e.control.data
        
        if selected_button.data == 'settings':
            await Settings(page, select_ver).load()
    
        if selected_button.data == 'modrinth':
            try:
                await Modrinth(page).load()
            except:
                pass
             
        if selected_button.data == 'perfil':
            await Perfil(page).load()
            
        page.update()

    page.content_menu = ft.Container(
        border=ft.border.all(1, page.color_init),
        expand=10,
        bgcolor=TYPES_COLORS[page.launcher.config.get("opacity")][2],
        margin=0,
        padding=5,
        alignment=ft.alignment.top_left
    )
        
    page.button_play = ButtonPlay(page, page.text_play, jugar_func).get()
    
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
    
    sections_list_cls = ButtonsSections(page, function_content)
    
    page.modrinth_button = await sections_list_cls.get_modrinth()
    page.settings_button = await sections_list_cls.get_settings()
    page.perfil_button = await sections_list_cls.get_perfil()
    page.iconbutton_console = ft.IconButton(
        col=1,
        icon=ft.Icons.MONITOR_OUTLINED,
        on_click=open_console,
        icon_color=page.color_init,
        bgcolor=ft.Colors.TRANSPARENT,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5)
        )
    )
    page.content_sections = ft.Container(
        expand=1,
        border_radius=ft.BorderRadius(5, 5, 0, 0),
        bgcolor=TYPES_COLORS[page.launcher.config.get("opacity")][1],
        content=
        ft.ResponsiveRow(
            controls=[
                page.perfil_button,
                page.modrinth_button,
                page.settings_button     
            ], 
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            spacing=0,
            run_spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ), alignment=ft.alignment.center
        
    )
    
    page.dropdown_versions = DropdownVersions(page, select_ver, page.tooltip_installation_needed).get()
    page.content_sidebar = ft.Container(
        margin=ft.Margin(0, 5, 0, 0),
        border_radius=5,
        expand=1.5,
        content=ft.ResponsiveRow(
            columns=14,
            controls=[
                page.dropdown_versions,#Lista de versiones
                page.iconbutton_console,
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
                margin=0,
                padding=0,
                content=ft.Column(
                    controls=[
                        page.content_sections,
                        page.content_menu,
                        page.content_sidebar
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
        floating_action_button=page.button_play,
        floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT,
    )
