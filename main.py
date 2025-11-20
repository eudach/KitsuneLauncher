import os
import flet as ft
from flet_route import Routing, path
import time

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

async def Pagina(page: ft.Page):
    # WINDOWS CONFIG
    page.window.title_bar_hidden = True
    page.title = "Kitsune Launcher"
    page.window.frameless = True
    page.window.prevent_close = True
    page.window.title_bar_buttons_hidden = True
    page.window.transparent = True
    page.window.min_width = 1200
    page.window.min_height = 700
    page.window_resizable = True
    page.window.icon = "icon.ico"
    page.padding = 0
    page.bgcolor = ft.Colors.TRANSPARENT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    page.dragging_enabled = False
    page.progress_bar = None
    page.close_alert = close_alert
    page.icon_path = f"{os.path.dirname(__file__)}\\assets\\icon.ico"
    
    # LOADING SCREEN (rápido)
    page.loading_animation = ft.Container(
        alignment=ft.alignment.center,
        content=ft.Column(
        controls=[
                ft.Image(src="loading.gif", width=page.window.width/2, scale=1.5, height=page.window.height/2),
                ft.ProgressRing(color='white', scale=2)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.add(page.loading_animation)
    page.update()

    # ------- Load all Widgets and Modules --------
    async def init_launcher():
        
        
        # LOGGER
        page.logger = Logger(page)
        
        # TRADUCTIONS
        page.trad = LenguageSyS(page).get()
        
        # Fuction TRADUCTIONS
        page.t = lambda k: page.trad[page.launcher.config.get("language")].get(k, f"[{k}]")
        
        #TOASTS
        page.toaster = Toaster(page, expand=False, position=ToastPosition.TOP_CENTER)
        
        #Internet
        page.internet_check : Internet = Internet(page=page)  # type: ignore
        
        # KITSUNE CONFIG
        page.launcher:KitsuneLauncher = KitsuneLauncher(page) # type: ignore
        page.launcher.init()
        
        #Version
        page.version = CheckVersion(page)
        
        #Windows manager
        page.win = WindowsManager(page)
        
        def on_window_event(e: ft.WindowEvent):
            if e.data == "minimize" or e.data == "hide" or e.data == "blur":
                page.dragging_enabled =  False
            elif e.data == "restore" or e.data == "show" or e.data == "focus":
                page.dragging_enabled = True

            if e.data == "close":
                page.win.close_windows()
            
            
        page.window.on_event = on_window_event
        
        #Modrinth Api
        page.api = ModrinthAPI(page)
        await page.api.start()

        page.window.start_dragging()
        
        # STRAY
        page.stray = StraySystem(page)

        # GLOBAL CONFIG
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
        
        # TEMP CONFIG
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
    
        # FONTS
        page.fonts = {
            "ShareTech": "fonts/ShareTech-Regular.ttf",
            "Inter": "fonts/Inter-Reegular.ttf",
            "Poppins": "fonts/Poppins-SemiBold.ttf",
            "console": "fonts/console_windows.ttf"
        }
        
        # PRESENCE
        page.presence = DiscordReachPresence(page=page, started=page.launcher.config.get("discord_presence"))
        page.logger.debug("Discord pasa")
        
        async def lazy_main_view(page, params, basket):
            from ui.views.MainView import MainView
            page.logger.debug(f"Inicio de MainView")
            return await MainView(page=page, params=params, basket=basket)

        async def lazy_login_view(page, params, basket):
            from ui.views.LoginView import LoginView
            page.logger.debug(f"Inicio de LoginView")
            return await LoginView(page=page, params=params, basket=basket)
        
        # PAGES
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
        
        # NAV
        if page.launcher.config.get("username") is None:
            page.logger.debug(f"Redirigiendo a LoginView")
            page.go("/login")
        else:
            page.logger.debug(f"Redirigiendo a MainView")
            page.go("/")

    # Task loading
    try:
        page.run_task(init_launcher)
    except:
        return exit()


ft.app(target=Pagina, name="Kitsune Launcher", assets_dir="assets")
