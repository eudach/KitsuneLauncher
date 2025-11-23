import asyncio
import flet as ft
from flet_route import Params, Basket

from core.utils import TYPES_COLORS, alerta

from ui.components.dropdown import DropdownVersions
from ui.components.tooltip import Tooltip_installation
from ui.components.button import (
    ButtonPlay, ButtonsSections, ButtonNewVersion,
    ButtonOpenLatestLog, ButtonOpenDebugLog)

from ui.sections.Modrinth import Modrinth
from ui.sections.Settings import Settings
from ui.sections.Perfil import Perfil

from ui.resources.Fonts import BaseFonts

class MainViewConstants:
    """Constantes de la vista principal."""
    CONSOLE_ICON = ft.Icons.MONITOR_HEART_OUTLINED
    CONSOLE_BUTTON_ICON = ft.Icons.MONITOR_OUTLINED
    WARNING_ICON = ft.Icons.WARNING_AMBER
    WARNING_OUTLINED_ICON = ft.Icons.WARNING_AMBER_OUTLINED
    SECTIONS = ["perfil", "settings", "modrinth"]
    DIALOG_BORDER_RADIUS = 3
    BUTTON_BORDER_RADIUS = 5


async def MainView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    page.logger.info("Inicializando vista principal del launcher")

    # --- Funciones de eventos ---
    async def jugar_func(e: ft.ControlEvent) -> None:
        version_ = page.launcher.last_played_version
        if version_ == [None, None]:
            page.open(
                alerta(page.t("error_select_dialg_title"), page.t("error_select_dialg_description"))
            )
            return

        if page.launcher.config.get("java_path") is None:
            page.open(
                alerta(page.t("error_select_dialg_title"), page.t("error_java_path"))
            )
            return

        if not page.launcher.set_version(version_):
            page.open(
                alerta(page.t("invalid_version"), f"{version_[0]} {page.t('invalid_version_description')}")
            )
            return

        page.logger.info(f"Iniciando Minecraft con versión: {version_[0]}")
        page.run_thread(page.launcher.start_minecraft)
        
    async def install_minecraft_ver(e):
        version = e.control.data
        page.dialog_installation.open = False
        page.update()
        page.launcher.instalar_minecraft_en_hilo(version)

    async def select_ver(e: ft.ControlEvent) -> None:
        version_data = e.control.data
        
        if page.global_vars["installing_minecraft_version"]:
            page.open(
                alerta(titulo="Error", descripcion=page.t("error_installing"))
            )
            return
        
        if not version_data:
            return

        version = version_data[0]
        installed = page.launcher.set_version(version_data)
        page.dialog_installation = ft.AlertDialog(
            icon=ft.Icon(name=MainViewConstants.WARNING_ICON, color=page.global_vars["primary_color"]),
            title=ft.Text(page.t("installation_sucess"), text_align=ft.TextAlign.CENTER, font_family=BaseFonts.texts),
            content=ft.Text(
                f"{version} {page.t('installation_sucess_description')}",
                text_align=ft.TextAlign.CENTER,
            ),
            actions=[
                ft.TextButton(
                    text=page.t("data_question_y"),
                    data=version,
                    on_click=install_minecraft_ver,
                    style=ft.ButtonStyle(color=page.global_vars["primary_color"]),
                ),
                ft.TextButton(
                    text="No",
                    on_click=lambda e: page.close(page.overlay[-1]),
                    style=ft.ButtonStyle(color=page.global_vars["primary_color"]),
                ),
            ],
            bgcolor=ft.Colors.BLACK,
            shape=ft.BeveledRectangleBorder(MainViewConstants.DIALOG_BORDER_RADIUS),
            alignment=ft.alignment.center,
        )
        if not installed:
            page.global_vars["option_change_installed"] = e.control
            page.open(
                page.dialog_installation
            )
    
    def reset_button_style(btn):
        btn.style = ft.ButtonStyle(
            shape=ft.ContinuousRectangleBorder(3),
            color=ft.Colors.WHITE,
            side={
                ft.ControlState.DEFAULT: ft.BorderSide(0, color=ft.Colors.TRANSPARENT),
                ft.ControlState.HOVERED: ft.BorderSide(2, color=ft.Colors.WHITE10)
            },
            overlay_color=ft.Colors.BLACK12,
            icon_size=page.window.width /50,
            text_style=ft.TextStyle(
                size=page.window.width /50,
                font_family=BaseFonts.titles,
                weight=ft.FontWeight.W_100,
            )
        )
        btn.update()
    

    async def function_content(e: ft.ControlEvent) -> None:
        new_section = e.control.data
        old_section = page.global_vars["current_section"]

        # --- 1. Evitar recargar la misma sección ---
        if new_section == old_section:
            return
        
        page.views[0].floating_action_button = None

        # --- 2. Sistema de botones ---
        button_map = {
            "perfil": page.perfil_button,
            "settings": page.settings_button,
            "modrinth": page.modrinth_button,
        }

        # Resetear estilo del botón anterior
        if old_section in button_map:
            reset_button_style(button_map[old_section])

        # Activar botón nuevo
        page.selected_button = button_map.get(new_section)
        if page.selected_button:
            page.selected_button.style.bgcolor = TYPES_COLORS[page.launcher.config.get("opacity")][0]
            page.selected_button.style.side = page.borderside_sections
            page.selected_button.update()

        # --- 3. Cancelar carga previa si está activa ---
        old_task = page.global_vars.get("current_loader_task")
        if old_task and not old_task.done():
            old_task.cancel()

        # --- 4. Poner animación de carga inmediatamente ---
        page.content_menu.content = page.loading_animation
        page.update()

        # Guardar sección actual
        page.global_vars["current_section"] = new_section
        page.global_vars["loading"] = True

        # --- 5. Diccionario de loaders ---
        sections = {
            "settings": lambda: Settings(page, select_ver).load(),
            "modrinth": lambda: Modrinth(page).load(),
            "perfil":   lambda: Perfil(page).load(),
        }

        # --- 6. Crear tarea de carga ---
        async def load_section():
            try:
                # cargar sección correcta
                if new_section in sections:
                    await sections[new_section]()

            except asyncio.CancelledError:
                page.logger.log("Carga cancelada por cambio rápido de sección")
                return

            except Exception as err:
                page.logger.error(f"Error al cargar sección: {err}")

            finally:
                page.global_vars["loading"] = False
                page.update()

        # Ejecutar task sin bloquear UI
        task = page.run_task(load_section)
        page.global_vars["current_loader_task"] = task


    # --- Widgets principales ---
    page.tooltip_installation_needed = Tooltip_installation(page).get()
    page.borderside_sections = ft.BorderSide(1, color=page.global_vars["primary_color"], stroke_align=ft.BorderSideStrokeAlign.INSIDE)

    page.button_play = ButtonPlay(page, jugar_func).get()
    page.progress_time_remain = ft.Text(visible=False, text_align=ft.TextAlign.CENTER, font_family=BaseFonts.texts)
    page.progress_bar = ft.ProgressBar(
        value=0,
        visible=False,
        width=page.window.width / 3,
        height=page.window.height / 30,
        bgcolor=ft.Colors.WHITE10,
        border_radius=MainViewConstants.BUTTON_BORDER_RADIUS,
        color=page.global_vars["primary_color"],
    )
    
    page.markdown_control = ft.Markdown(
        value=page.t("markdown_news"),
        selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        code_theme=ft.MarkdownCodeTheme.DARCULA,
        expand=True,
        fit_content=True,
        md_style_sheet=ft.MarkdownStyleSheet(block_spacing=20, blockquote_alignment=ft.MainAxisAlignment.CENTER)
    )

    # botones secciones
    sections_list_cls = ButtonsSections(page, function_content)
    page.modrinth_button = await sections_list_cls.get_modrinth()
    page.settings_button = await sections_list_cls.get_settings()
    page.perfil_button = await sections_list_cls.get_perfil()

    
    
    # botón consola
    async def open_console(e: ft.ControlEvent) -> None:
        page.global_vars["current_section"] = "console"
        page.open(
            ft.AlertDialog(
                content_padding=10,
                actions_padding=10,
                title_padding=0,
                icon_padding=ft.Padding(left=5, right=5, top=5, bottom=0),
                content=ft.Container(
                    content=page.Text_Console,
                    bgcolor=ft.Colors.WHITE10,
                    border_radius=MainViewConstants.BUTTON_BORDER_RADIUS,
                    expand=True,
                    width=page.window.width,
                    height=page.window.height/1.3,
                ),
                icon=ft.Row(controls=[
                        ft.Row(expand=True),
                        ft.Icon(name=MainViewConstants.CONSOLE_ICON, color=page.global_vars["primary_color"]),
                        ft.Row(expand=True),
                        ft.IconButton(icon=ft.Icons.CLOSE, icon_color=page.global_vars["primary_color"], on_click=page.close_alert)
                    ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
                ,
                bgcolor=ft.Colors.BLACK,
                shape=ft.BeveledRectangleBorder(MainViewConstants.DIALOG_BORDER_RADIUS),
                actions=[
                    ButtonOpenLatestLog(page=page).get(),
                    ButtonOpenDebugLog(page=page).get()
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER,
                actions_overflow_button_spacing=5
            )
        )

    page.iconbutton_console = ft.IconButton(
        col=0.7,
        tooltip=ft.Tooltip(message=page.t("sections_main")),
        on_click=open_console,
        bgcolor=ft.Colors.TRANSPARENT,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=MainViewConstants.BUTTON_BORDER_RADIUS)),
        content=ft.Image(
            src="iconos/console.png", width=40, height=40
        )
    )

    # contenedores
    page.content_sections = ft.Container(
        expand=1,
        border_radius=ft.BorderRadius(
            MainViewConstants.BUTTON_BORDER_RADIUS,
            MainViewConstants.BUTTON_BORDER_RADIUS,
            0,
            0,
        ),
        bgcolor=TYPES_COLORS[page.launcher.config.get("opacity")][1],
        content=ft.ResponsiveRow(
            controls=[page.perfil_button, page.modrinth_button, page.settings_button],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        alignment=ft.alignment.center,
    )

    page.content_menu = ft.Container(
        border=ft.border.all(1, page.global_vars["primary_color"]),
        expand=10,
        bgcolor=TYPES_COLORS[page.launcher.config.get("opacity")][2],
        content=page.markdown_control,
        margin=0,
        padding=5,
        alignment=ft.alignment.top_left,
    )

    page.dropdown_versions = DropdownVersions(page, select_ver, page.tooltip_installation_needed).get()
    
    page.bottom_bar = ft.BottomAppBar(
        padding=5,
        bgcolor=TYPES_COLORS[page.launcher.config.get("opacity")][2],
        content= ft.ResponsiveRow(
            expand=True,
            columns=14,
                controls=[
                    page.dropdown_versions,
                    page.iconbutton_console,
                    ft.Row(
                        col=0.7),
                    ft.Column(
                        col=4,
                        controls=[page.progress_bar, page.progress_time_remain],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    page.button_play
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
    
    if page.version.have_new_version():
        page.open(
            ft.AlertDialog(
                content_padding=10,
                actions_padding=10,
                title_padding=0,
                icon_padding=ft.Padding(left=5, right=5, top=5, bottom=0),
                title=ft.Text(value=page.t("new_update"), font_family=BaseFonts.titles, text_align=ft.TextAlign.CENTER),
                content=ft.Text(value=page.t("new_update_description"), font_family=BaseFonts.texts, text_align=ft.TextAlign.CENTER),
                icon=ft.Row(controls=[
                        ft.Row(expand=True),
                        ft.Icon(name=MainViewConstants.WARNING_ICON, color=page.global_vars["primary_color"]),
                        ft.Row(expand=True),
                        ft.IconButton(icon=ft.Icons.CLOSE, icon_color=page.global_vars["primary_color"], on_click=page.close_alert)
                    ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                bgcolor=ft.Colors.BLACK87,
                shape=ft.BeveledRectangleBorder(MainViewConstants.DIALOG_BORDER_RADIUS),
                actions=[
                    ButtonNewVersion(page, on_click=lambda a: page.launch_url(page.version.latest_version_link())).get()
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER
            
            )
        )
    # vista final
    return ft.View(
        "/",
        controls=[
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.TRANSPARENT,
                margin=0,
                padding=0,
                content=ft.Column(
                    controls=[page.content_sections, page.content_menu],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                ),
            )
        ],
        decoration=ft.BoxDecoration(
            image=ft.DecorationImage(
                src=page.launcher.config.get("wallpaper_launcher"),
                fit=ft.ImageFit.COVER,
                opacity=0.8,
            ),
        ),
        bgcolor=ft.Colors.TRANSPARENT,
        bottom_appbar=page.bottom_bar
    )
