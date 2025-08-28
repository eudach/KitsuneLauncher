import flet as ft
from flet_route import Routing,path

import time

from core.launcher import KitsuneLauncher
from core.discord import DiscordReachPresence
from core.lenguage import LenguageSyS

from ui.components.appbar import AppBarWindows

async def Pagina(page: ft.Page):
    #WINDOWS CONFIG
    page.window.title_bar_hidden = True
    page.window.frameless = True 
    page.window.title_bar_buttons_hidden = True
    page.window.transparent = False  
    page.window_min_width = 400
    page.window_min_height = 300
    page.window_resizable = True
    page.window.icon = "icon.ico"
    page.padding = 0
    page.bgcolor = ft.Colors.TRANSPARENT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    #KITSUNE CONFIG
    page.launcher:KitsuneLauncher = KitsuneLauncher() # type: ignore
    page.launcher.set_page(page)
    
    #Windows SIZE
    page.ancho = page.window.width
    page.alto = page.window.height
    
    async def on_resize(e):
        page.ancho = e.page.window.width
        page.alto = e.page.window.height
        page.update()

    page.on_resize = on_resize
    
    #TRADUCTIONS
    page.trad = LenguageSyS().get()

    # función de traducción
    page.t = lambda k: page.trad[page.launcher.config.get("language")].get(k, f"[{k}]")
    
    page.temp_config_modrinth = {
        "offset": 0,
        "limit_search_mods": 10,
        "total_mods_result": 0,
        "minecraft_started": False,
        
        "current_section_modrinth": None,
        "list_mods_cache": [],
        "page_modslist_return": None,
        
    }
    
    page.current_section = None
    page.default_wallpaper = "bg.png"
    page.option_change_installed = None
    page.discord_times = int(time.time())
    page.progress_bar = None
    page.color_init = page.launcher.config.get("primary_color_schema")
    
    page.Text_Console = ft.ListView(
        controls=[
            ft.Text(font_family="console", value="Console", size=page.ancho/65, selectable=True, expand=True)
        ],
        spacing=5,
        padding=3,
        expand=True,
        auto_scroll=True
    )
    page.launcher.init()
    
    #FONTS
    page.fonts = {
        "Katana": "KATANA.ttf",
        "Monkey": "MonkeyLand.otf",
        "lokeya": "Lokeya.otf",
        "liberation":"Roboto.ttf",
        "console": "console_windows.ttf"
    }
    
    #PRESENCE
    page.presence = DiscordReachPresence(page=page, started=page.launcher.config.get("discord_presence"))
    
    async def maximize(e):
        page.window.maximized = not page.window.maximized
        page.update()
        
    async def minimize(e):
        page.window.minimized = not page.window.minimized
        page.update()
    
    async def close_windows(e):
        page.launcher.config.save()
        page.window.close()
    
    async def lazy_main_view(page, params, basket):
        from ui.views.MainView import MainView
        return await MainView(page=page, params=params, basket=basket)

    async def lazy_login_view(page, params, basket):
        from ui.views.LoginView import LoginView
        return await LoginView(page=page, params=params, basket=basket)
    
    #PAGES
    app_routes = [
        path(url="/", clear=True, view=lazy_main_view),
        path(url="/login", clear=True, view=lazy_login_view)
    ]

    Routing(
        page=page, 
        app_routes=app_routes,
        appbar=AppBarWindows(page, minimize, maximize, close_windows).get(),
        async_is=True
        )
    
    #MAIN
    if page.launcher.config.get("username") is None:
        page.go("/login")
    else:
        page.go("/")


ft.app(target=Pagina, name="Kitsune Launcher", assets_dir="assets")