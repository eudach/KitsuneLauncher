import flet as ft
from flet_route import Routing,path
from views.MainView import MainView
from views.LoginView import LoginView
from views.InstallationView import InstallationView
from discordrp import Presence
import time
from Utils import get_java, minecraft_dir_exists

async def Pagina(page: ft.Page):
    page.presence = Presence("1111360118680993792")
    
    
    #WINDOWS CONFIG
    page.window.title_bar_buttons_hidden = True
    page.window.title_bar_hidden = True
    page.padding = 0
    page.window.icon = "icon.ico"
    page.bgcolor = ft.Colors.TRANSPARENT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    #Client Storage
    
    #CHECK .minecraft
    page.wallpaper_launcher = await page.client_storage.get_async("wallpaper_launcher") if await page.client_storage.contains_key_async("wallpaper_launcher") else "bg.jpg"
    page._minecraft = await page.client_storage.get_async("minecraft_path") if await page.client_storage.contains_key_async("minecraft_path") else ".minecraft"
    if not await minecraft_dir_exists():
        return await page.go("/installation")
    
    page.discord_presence_allow = await page.client_storage.get_async("discord_presence_allow") if await page.client_storage.contains_key_async("discord_presence_allow") else True
    page.jvw_args = await page.client_storage.get_async("jvw_args") if await page.client_storage.contains_key_async("jvw_args") else "-Xmx3G -Xms3G --enable-native-access=ALL-UNNAMED".split(" ")
    page.java_path = await page.client_storage.get_async("java_path") if await page.client_storage.contains_key_async("java_path") else await get_java()
    page.username = await page.client_storage.get_async("username") if await page.client_storage.contains_key_async("username") else None
    page.premium_mode = await page.client_storage.get_async("premium_mode") if await page.client_storage.contains_key_async("premium_mode") else False
    page.lenguage = await page.client_storage.get_async("lenguaje") if await page.client_storage.contains_key_async("lenguaje") else 1
    page.photo_perfil_path = await page.client_storage.get_async("photo_perfil") if await page.client_storage.contains_key_async("photo_perfil") else "icon.png"
    
    page.ram_usage = await page.client_storage.get_async("ram_usage") if await page.client_storage.contains_key_async("ram_usage") else 2
    page.select_version = await page.client_storage.get_async("select_version") if await page.client_storage.contains_key_async("select_version") else None
    
    page.times = int(time.time())
    page.Text_Console = None
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
    page.trad = {
        "settings_saved":["Configuraciones guardadas", "Saved settings"],
        "setting_saved_description":["Se han guardado las siguientes configuraciones", "The following settings have been saved"],
        
        "session_closed":["Se ha cerrado tu sesion", "Your session has been closed"],
        "session_closed_description":["Has cerrado sesion como", "You have logged out as"],
        "session_close":["Cerrar Sesión", "Log out"],
        
        "select_javaw":["Seleccione", "Select"],
        "select_img_wallpaper":["Seleccione la imagen para cambiar el fondo de pantalla", "Select the Image to change the Wallpaper"],
        "discord_rich":["Mostrar el launcher en Discord", "Display on discord launcher"],
        "ram_usage":["Cambiar el uso de RAM en Minecraft", "Change usage RAM Minecraft"],
        "wallpaper_save":["Cambiar la imagen de fondo del lanzador","Change Background image launcher"],
        "save_":["Guardar", "Save"],
        "restore_":["Restaurar", "Restore"],
        "delete_all_":["Borrar Todo", "Delete All"],
        "delete_all_confirmation_":["Borrar todos los datos almacenados", "Delete all stored data"],
        "console_msg":["Esta es la consola", "This is the console"],
        "invalid_version":["Versión no válida", "Invalid Version"],
        "invalid_version_description":["es una versión válida", "it is an invalid version"],
        "installation_needed":["Necesita instalación","Need Installation"],
        "installation_sucess":["Instalando versión...", "Installing version..."],
        "installation_sucess_description":["no se ha encontrado, se instalará", "not found, will be installed"],
        
        
        "file_not_found":["No se encontró el archivo especificado", "The specified file was not found"],
        "data_question_y": ["Si", "Yes"],
        
        "data_elimination": ["Eliminación de datos en curso", "Data deletion in progress"],
        "data_elimination_sure": ["Estás seguro de eliminar todos los datos?", "Are you sure you want to delete all data?"],
        
        "user_state_discord_conect": ["Conectado", "Connected"],
        "user_state_discord_disconect":["No conectado", "Not connected"],
        "user_state_discord_mainpage":["Página de inicio", "Home page"],
        "user_state_discord_playing":["Jugando Minecraft", "Playing Minecraft"],
        
        "error_name_dialg_title":["Error en el nombre de usuario", "Error in the username"],
        "error_name_dialg_description":["El nombre de usuario proporcionado no es válido", "The username provided is not valid"],
        "error_select_dialg_title":["Error tienes que elegir una version válida", "Error you have to choose a valid version"],
        "error_select_dialg_description":["Elige una de las versiones mostradas en el apartado", "Choose one of the versions shown in the section"],
        "button_login":["Iniciar Sesión", "Sign in"],
        "name_user": ["Nombre de usuario", "Username"],
        "name_user_hint": ["Escribe tu nombre de usuario", "Write your username"],
        
        "email_user": ["Correo", "Email"],
        "email_user_hint": ["Escribe tu Correo", "Write your email"],
        "java_recommended": ["Es recomendado usar Java 1.17 para versiones recientes", "It is recommended to use Java 1.17 for recent versions"],
        
        "pass_user": ["Contraseña", "Password"],
        "pass_user_hint": ["Escribe tu Contraseña", "Write your password"],
        "versions_dropdown_label": ["Elige la versión", "Select version"],
        "versions_dropdown": ["Versiones", "Versions"],
        "sections_main": ["Consola","Console"],
        "sections_profile": ["Perfil","Profile"],
        "sections_settings": ["Ajustes","Settings"],
        "play_button": ["Jugar", "Play"],
        
        "lenguaje_dropdown": ["Idioma", "Language"],
        "lenguaje_dropdown_description": ["Selecciona el idioma", "Select the language"],
        "Resolution_perfil": ["Resolución recomendada de la imagen 256x256 or 512x512", "Recommended image resolution 256x256 or 512x512"]
    }
    
    #FONTS
    page.fonts = {
        "Katana": "KATANA.ttf",
        "Monkey": "MonkeyLand.otf",
        "lokeya": "Lokeya.otf",
        "liberation":"Roboto.ttf",
        "console": "console_windows.ttf"
    }
    
    #DISCORD RICH MAIN UPDATE
    if page.discord_presence_allow:
        page.presence.set({
            "state": page.trad["user_state_discord_mainpage"][page.lenguage],
            "details": f"{page.username} {page.trad["user_state_discord_conect"][page.lenguage]}" if page.username is not None else f"{page.trad["user_state_discord_disconect"][page.lenguage]}",
            "timestamps": {"start": int(page.times)},
        })
        
    
    async def maximi(e):
        page.window.maximized = not page.window.maximized
        page.update()
        
    async def minimi(e):
        page.window.minimized = not page.window.minimized
        page.update()
        
    #WINDOWS APPBAR
    page.appbar_x = ft.Row(
        [
            ft.WindowDragArea(
                ft.Row(controls=
                    [
                    ft.Container(content=ft.Image(src=page.window.icon, width=80, height=50, scale=1.1, opacity=0.8), margin=0, padding=0),
                    ft.Text("Kitsune Launcher", font_family="Katana", size=page.ancho/30)
                    ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER
                ), expand=True
            ),
            ft.IconButton(
                style=ft.ButtonStyle(
                    overlay_color=ft.Colors.BLACK12,
                    shape=ft.BeveledRectangleBorder(radius=5)
                ),
                icon=ft.Icons.MINIMIZE, 
                icon_color=ft.Colors.WHITE,
                on_click=minimi,
                scale=0.9
            ),
            ft.IconButton(
                style=ft.ButtonStyle(
                    overlay_color=ft.Colors.BLACK12,
                    shape=ft.BeveledRectangleBorder(radius=5)
                ),
                icon=ft.Icons.SQUARE_OUTLINED, 
                icon_color=ft.Colors.WHITE,
                on_click=maximi,
                scale=0.9
            ),
            ft.IconButton(
                style=ft.ButtonStyle(
                    overlay_color=ft.Colors.BLACK12,
                    shape=ft.BeveledRectangleBorder(radius=5)
                ),
                icon=ft.Icons.CLOSE, 
                icon_color=ft.Colors.WHITE, 
                on_click=lambda _: page.window.close(),
                scale=0.9
            )
        ]
    )
    
    #PAGES
    app_routes = [
        path(
            url="/",
            clear=True,
            view=MainView
            ),
        path(
            url="/login",
            clear=True,
            view=LoginView
            ),
        path(
            url="/installation",
            clear=True,
            view=InstallationView
            )
        #path(url="/next_view/:my_id", clear=False, view=MainView),
    ]

    Routing(
        page=page, 
        app_routes=app_routes,
        appbar=ft.Container(content=page.appbar_x, bgcolor=ft.Colors.BLACK54, border_radius=5),
        async_is=True
        )
    
    
    #MAIN
    if page.username is None:
        page.go("/login")
    else:
        page.go("/")


ft.app(target=Pagina, name="Kitsune Launcher", assets_dir="assets")