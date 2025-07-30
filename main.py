import flet as ft
from flet_route import Routing,path
from discordrp import Presence
import time
from Tools import KitsuneLauncher, TYPES_COLORS

async def Pagina(page: ft.Page):

    page.presence = Presence("1394361962212626543")
    
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
    
    page.launcher:KitsuneLauncher = KitsuneLauncher() # type: ignore
    page.launcher.set_page(page)
    
    page.discord_times = int(time.time())
    page.progress_bar = None
    
    #Windows SIZE
    page.ancho = page.window.width
    page.alto = page.window.height
    
    async def on_resize(e):
        page.ancho = e.page.window.width
        page.alto = e.page.window.height
        page.update()

    page.on_resize = on_resize
    
    #TRADUCTIONS
    # TRADUCTIONS MULTI-LANGUAGE (modern structure)
    page.trad = {
        "es": {
            "java_path_": "Ubicación de Java",
            "mc_path_": "Ubicación de Minecraft",
            "opacity": "Opacidad general",
            "need_restart": "Ciertas configuraciones realizadas necesitan de reinicio",
            "color_picker_text": "Color del tema",
            "version_not_installed": "No disponible",
            "settings_saved": "Configuraciones guardadas",
            "setting_saved_description": "Se han guardado las siguientes configuraciones",
            "session_closed": "Se ha cerrado tu sesión",
            "session_closed_description": "Has cerrado sesión como",
            "session_close": "Cerrar Sesión",
            "select_javaw": "Seleccionar",
            "select_img_wallpaper": "Seleccionar la imagen para cambiar el fondo de pantalla",
            "discord_rich": "Mostrar el launcher en Discord",
            "ram_usage": "Cambiar el uso de RAM en Minecraft",
            "wallpaper_save": "Cambiar la imagen de fondo del lanzador",
            "save_": "Guardar",
            "restore_": "Restaurar",
            "delete_all_": "Borrar Todo",
            "delete_all_confirmation_": "Borrar todos los datos almacenados",
            "console_msg": "Esta es la consola",
            "invalid_version": "Versión no válida",
            "invalid_version_description": "es una versión válida",
            "installation_needed": "Necesita instalación",
            "installation_sucess": "Instalando versión...",
            "installation_sucess_description": "no se ha encontrado, se instalará",
            "file_not_found": "No se encontró el archivo especificado",
            "data_question_y": "Si",
            "data_elimination": "Eliminación de datos en curso",
            "data_elimination_sure": "¿Estás seguro de eliminar todos los datos?",
            "user_state_discord_conect": "Conectado",
            "user_state_discord_disconect": "No conectado",
            "user_state_discord_mainpage": "Página de inicio",
            "user_state_discord_playing": "Jugando Minecraft",
            "error_name_dialg_title": "Error en el nombre de usuario",
            "error_name_dialg_description": "El nombre de usuario proporcionado no es válido",
            "error_select_dialg_title": "Error tienes que elegir una versión válida",
            "error_select_dialg_description": "Elige una de las versiones mostradas en el apartado",
            "button_login": "Iniciar Sesión",
            "name_user": "Nombre de usuario",
            "name_user_hint": "Escribe tu nombre de usuario",
            "email_user": "Correo",
            "email_user_hint": "Escribe tu Correo",
            "java_recommended": "Es recomendado usar Java 1.17 para versiones recientes",
            "pass_user": "Contraseña",
            "pass_user_hint": "Escribe tu Contraseña",
            "versions_dropdown_label": "Elige la versión",
            "versions_dropdown": "Versiones",
            "sections_main": "Consola",
            "sections_profile": "Perfil",
            "sections_settings": "Ajustes",
            "play_button": "Jugar",
            "play_button_installing": "Instalando...",
            "lenguaje_dropdown": "Idioma",
            "lenguaje_dropdown_description": "Selecciona el idioma",
            "Resolution_perfil": "Resolución recomendada de la imagen 256x256 o 512x512"
        },
        "en": {
            "java_path_": "Location of Java",
            "mc_path_": "Location of Minecraft",
            "opacity":"Overall opacity",
            "need_restart": "Certain settings made require a restart",
            "color_picker_text": "Theme color",
            "version_not_installed": "Not available",
            "settings_saved": "Saved settings",
            "setting_saved_description": "The following settings have been saved",
            "session_closed": "Your session has been closed",
            "session_closed_description": "You have logged out as",
            "session_close": "Log out",
            "select_javaw": "Select",
            "select_img_wallpaper": "Select the Image to change the Wallpaper",
            "discord_rich": "Display on discord launcher",
            "ram_usage": "Change usage RAM Minecraft",
            "wallpaper_save": "Change Background image launcher",
            "save_": "Save",
            "restore_": "Restore",
            "delete_all_": "Delete All",
            "delete_all_confirmation_": "Delete all stored data",
            "console_msg": "This is the console",
            "invalid_version": "Invalid Version",
            "invalid_version_description": "it is an invalid version",
            "installation_needed": "Need Installation",
            "installation_sucess": "Installing version...",
            "installation_sucess_description": "not found, will be installed",
            "file_not_found": "The specified file was not found",
            "data_question_y": "Yes",
            "data_elimination": "Data deletion in progress",
            "data_elimination_sure": "Are you sure you want to delete all data?",
            "user_state_discord_conect": "Connected",
            "user_state_discord_disconect": "Not connected",
            "user_state_discord_mainpage": "Home page",
            "user_state_discord_playing": "Playing Minecraft",
            "error_name_dialg_title": "Error in the username",
            "error_name_dialg_description": "The username provided is not valid",
            "error_select_dialg_title": "Error you have to choose a valid version",
            "error_select_dialg_description": "Choose one of the versions shown in the section",
            "button_login": "Sign in",
            "name_user": "Username",
            "name_user_hint": "Write your username",
            "email_user": "Email",
            "email_user_hint": "Write your email",
            "java_recommended": "It is recommended to use Java 1.17 for recent versions",
            "pass_user": "Password",
            "pass_user_hint": "Write your password",
            "versions_dropdown_label": "Select version",
            "versions_dropdown": "Versions",
            "sections_main": "Console",
            "sections_profile": "Profile",
            "sections_settings": "Settings",
            "play_button": "Play",
            "play_button_installing": "Installing...",
            "lenguaje_dropdown": "Language",
            "lenguaje_dropdown_description": "Select the language",
            "Resolution_perfil": "Recommended image resolution 256x256 or 512x512"
        }
    }

    # idioma desde storage
    # función de traducción
    page.t = lambda k: page.trad[page.launcher.config.get("language")].get(k, f"[{k}]")
    page.Text_Console = ft.ListView(controls=
        [
            ft.Text(font_family="console", value="", size=page.ancho/65, selectable=True, expand=True)
        ],
        spacing=5,
        padding=3,
        expand=True,
        auto_scroll=True
    )
    page.color_init = page.launcher.config.get("primary_color_schema")
    
    #FONTS
    page.fonts = {
        "Katana": "KATANA.ttf",
        "Monkey": "MonkeyLand.otf",
        "lokeya": "Lokeya.otf",
        "liberation":"Roboto.ttf",
        "console": "console_windows.ttf"
    }
    
    #DISCORD RICH MAIN UPDATE
    if page.launcher.config.get("discord_presence"):
        page.presence.set({
            "state": page.t("user_state_discord_mainpage"),
            "details": f"{page.launcher.config.get("username")} {page.t("user_state_discord_conect")}" if page.launcher.config.get("username") is not None else f"{page.t("user_state_discord_disconect")}",
            "timestamps": {"start": int(page.discord_times)},
            "assets": {
                "large_image": "icon",
            },
            "buttons": [
                {
                    "label": "Info",
                    "url": "https://github.com/eudach/KitsuneLauncher",
                }
            ],
        })
        
    
    async def maximi(e):
        page.window.maximized = not page.window.maximized
        page.update()
        
    async def minimi(e):
        page.window.minimized = not page.window.minimized
        page.update()
    
    async def close_windows(e):
        page.launcher.config.save()
        page.window.close()
    
    #WINDOWS APPBAR
    page.appbar_x = ft.Row(
        controls=[
            ft.WindowDragArea(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Image(src=page.window.icon, width=80, height=50, scale=1.1, opacity=0.8),
                            margin=0,
                            padding=0
                        ),
                        ft.Text("Kitsune Launcher", font_family="Katana", size=page.ancho / 30)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                expand=True
            ),
            ft.IconButton(
                icon=ft.Icons.MINIMIZE,
                icon_color=ft.Colors.WHITE,
                on_click=minimi,
                scale=0.9
            ),
            ft.IconButton(
                icon=ft.Icons.SQUARE_OUTLINED,
                icon_color=ft.Colors.WHITE,
                on_click=maximi,
                scale=0.9
            ),
            ft.IconButton(
                icon=ft.Icons.CLOSE,
                icon_color=ft.Colors.WHITE,
                on_click=close_windows,
                scale=0.9
            )
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    async def lazy_main_view(page, params, basket):
        from views.MainView import MainView
        # si MainView es async:
        return await MainView(page=page, params=params, basket=basket)

    async def lazy_login_view(page, params, basket):
        from views.LoginView import LoginView
        return await LoginView(page=page, params=params, basket=basket)

    #PAGES
    app_routes = [
        path(url="/", clear=True, view=lazy_main_view),
        path(url="/login", clear=True, view=lazy_login_view)
    ]


    Routing(
        page=page, 
        app_routes=app_routes,
        appbar=ft.Container(content=page.appbar_x, bgcolor=TYPES_COLORS[page.launcher.config.get("opacity")][1], border_radius=5),
        async_is=True
        )
    
    
    #MAIN
    if page.launcher.config.get("username") is None:
        page.go("/login")
    else:
        page.go("/")


ft.app(target=Pagina, name="Kitsune Launcher", assets_dir="assets")