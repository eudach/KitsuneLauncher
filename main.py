import os
import time
import flet as ft
from flet_route import Routing, path

from core.launcher import KitsuneLauncher
from core.discord import DiscordReachPresence
from core.lenguage import LenguageSyS
from core.modrinthApi import ModrinthAPI
from core.stray import StraySystem
from core.internet import Internet
from core.loggerKL import Logger
from core.windows import WindowsManager
from core.check_version import CheckVersion
from core.utils import close_alert
from ui.components.toast import Toaster, ToastPosition
from ui.components.appbar import AppBarWindows

# ---------------------------------------------------------------------------
# Window configuration helpers
# ---------------------------------------------------------------------------
def configure_window(page: ft.Page) -> None:
    # Mostrar barra de título estándar para que se vea icono y nombre.
    page.window.title_bar_hidden = False
    page.title = "Kitsune Launcher"
    page.window.frameless = False
    page.window.prevent_close = True
    page.window.title_bar_buttons_hidden = False
    page.window.transparent = False
    # Tamaños mínimos y tamaño inicial (forzar si arranca más pequeño)
    MIN_W, MIN_H = 1200, 700
    page.window.min_width = MIN_W
    page.window.min_height = MIN_H
    # Si la ventana inicial es menor, ajustar inmediatamente
    if page.window.width < MIN_W:
        page.window.width = MIN_W
    if page.window.height < MIN_H:
        page.window.height = MIN_H
    # Propiedad correcta: resizable (el código anterior usaba window_resizable)
    page.window.resizable = True
    # Icono (debe existir en assets_dir)
    page.window.icon = "icon.ico"
    page.padding = 0
    page.bgcolor = ft.Colors.TRANSPARENT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.dragging_enabled = False
    page.progress_bar = None
    page.close_alert = close_alert
    page.icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.ico')
    # Compatibilidad con secciones que usan ancho/alto
    page.ancho = page.window.width
    page.alto = page.window.height
    # Handler temprano para mantener mínimos antes de init async
    def _early_window_event(e: ft.WindowEvent):
        if e.data.startswith("resize") or e.data.startswith("resized"):
            changed = False
            if page.window.width < MIN_W:
                page.window.width = MIN_W; changed = True
            if page.window.height < MIN_H:
                page.window.height = MIN_H; changed = True
            if changed:
                page.update()
    page.window.on_event = _early_window_event




async def Pagina(page: ft.Page):
    # Configuración de ventana y pantalla de carga rápida
    configure_window(page)
    page.loading_animation = ft.Container(
        alignment=ft.alignment.center,
        content=ft.Column(
            controls=[
                ft.Image(src="loading.gif", width=page.window.width / 2, scale=1.5, height=page.window.height / 2),
                ft.ProgressRing(color='white', scale=2)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.add(page.loading_animation)
    page.update()

    async def init_page():
        page.logger = Logger(page)
        page.logger.debug("Iniciando inicialización asíncrona")
        page.trad = LenguageSyS(page).get()
        page.launcher = KitsuneLauncher(page)  # type: ignore
        page.launcher.init()
        # Color base inicial para secciones que lo requieren (Settings, Modrinth)
        page.color_init = page.launcher.config.get("primary_color_schema")
        page.t = lambda k: page.trad[page.launcher.config.get("language")].get(k, f"[{k}]")
        page.toaster = Toaster(page, expand=False, position=ToastPosition.TOP_CENTER)
        page.internet_check = Internet(page=page)  # type: ignore
        page.temp_config_modrinth = {
            "offset": 0,
            "list_changes": [],
            "limit_search_mods": 10,
            "total_mods_result": 0,
            "minecraft_started": False,
            "current_section_modrinth": None,
            "last_search": None,
            "page_modslist_return": None,
            "list_mods_cache_installed": [],
            "mods_index_installed": {},
            "list_mods_cache": [],
            "mods_index": {}
        }
        page.fonts = {
            "ShareTech": "fonts/ShareTech-Regular.ttf",
            "Inter": "fonts/Inter-Reegular.ttf",
            "Poppins": "fonts/Poppins-SemiBold.ttf",
            "console": "fonts/console_windows.ttf"
        }
        page.global_vars = {
            "primary_color": page.launcher.config.get("primary_color_schema"),
            "project_type": "mod",
            "installing_minecraft_version": False,
            "discord_time_instance": int(time.time()),
            "option_change_installed": None,
            "current_section": None,
            "default_wallpaper": "img/wallpaper.png",
            "current_loader_task": None,
            "loading": False
        }
        # Añadir atributo directo para compatibilidad con código que usa page.default_wallpaper
        page.default_wallpaper = page.global_vars["default_wallpaper"]
        page.version = CheckVersion(page)
        page.win = WindowsManager(page)
        MIN_W, MIN_H = 1200, 700
        def on_window_event(e: ft.WindowEvent):
            # Enforce min size if resize event occurs (Flet may emit 'resized')
            if e.data in {"minimize", "hide", "blur"}:
                page.dragging_enabled = False
            elif e.data in {"restore", "show", "focus", "maximize"}:
                page.dragging_enabled = True
            elif e.data.startswith("resize") or e.data.startswith("resized"):
                # Ajustar si ventana por debajo del mínimo
                w, h = page.window.width, page.window.height
                changed = False
                if w < MIN_W:
                    page.window.width = MIN_W; changed = True
                if h < MIN_H:
                    page.window.height = MIN_H; changed = True
                if changed:
                    page.update()
            if e.data == "close":
                page.win.close_windows()
        page.window.on_event = on_window_event
        page.api = ModrinthAPI(page)
        await page.api.start()
        page.stray = StraySystem(page)
        page.presence = DiscordReachPresence(page=page, started=page.launcher.config.get("discord_presence"))
        page.logger.debug("Discord iniciado")
        async def lazy_main_view(page, params, basket):
            from ui.views.MainView import MainView
            page.logger.debug("Cargando MainView")
            return await MainView(page=page, params=params, basket=basket)
        async def lazy_login_view(page, params, basket):
            from ui.views.LoginView import LoginView
            page.logger.debug("Cargando LoginView")
            return await LoginView(page=page, params=params, basket=basket)
        app_routes = [
            path(url="/", clear=True, view=lazy_main_view),
            path(url="/login", clear=True, view=lazy_login_view)
        ]
        Routing(
            page=page,
            app_routes=app_routes,
            appbar=AppBarWindows(page, page.win.minimize, page.win.maximize, page.win.close_windows).get(),
            async_is=True
        )
        if page.launcher.config.get("app_background"):
            page.stray.start()
        if page.launcher.config.get("username") is None:
            page.logger.debug("Redirigiendo a LoginView")
            page.go("/login")
        else:
            page.logger.debug("Redirigiendo a MainView")
            page.go("/")

    # Inicio asíncrono
    try:
        page.run_task(init_page)  # Corre la corrutina sin bloquear la UI
    except Exception as e:
        print(f"Error iniciando la aplicación: {e}")
        return
def main():
    ft.app(target=Pagina, name="Kitsune Launcher", assets_dir="assets")


if __name__ == "__main__":
    main()
