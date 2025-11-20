

class LenguageSyS:
    def __init__(self, page):
        self.page = page
        self.page.logger.debug(f"Inicio de carga de traducciones")
        self.list_traductions = {
            "es": {
                "local_downloaded": "Contenido descargado localmente",
                "new_update_button": "Actualizar",
                "new_update_description": "Se ha encontrado una nueva actualización, haga clic en el botón para actualizar.",
                "new_update":"Actualización disponible",
                "internet_no_found": "No tiene conexión a internet",
                "error_search_mod_name":"No se pudo buscar, intente escribir manualmente",
                "markdown_news":"""
## 🆕 Novedades en la versión 0.1.6

- 🎨 **Interfaz gráfica renovada**: ahora todo el diseño se ve más atractivo y moderno.
- 🌐 **Sección de Modrinth mejorada**: exploración y vista rediseñadas, con más contenido y una experiencia más completa.
- 🧩 **Código optimizado y mejor estructurado** para facilitar el mantenimiento y futuras mejoras.
- 🖱️ **Sistema de Stray añadido**: permite dejar el launcher en segundo plano sin necesidad de abrirlo y cerrarlo constantemente (recomendado).  
- 🐞 **Corrección de varios bugs**: ahora se muestra el nombre de la ventana correctamente y se evita el cierre accidental desde la barra de tareas.  
- 🎨 **Historial de colores de tema**: se guardan los últimos 6 colores seleccionados.  
- ☕ **Panel de información de Java**: incluye detalles útiles junto con las últimas novedades.  
- 🔔 **Botón de actualización automática**: aparece solo cuando hay una nueva versión del launcher disponible.  
- 🧭 **Botones de navegación mejorados**: tanto en mods internos como en mods de Modrinth, ofreciendo mayor fluidez.  
- 🚧 **Próximamente en Modrinth**: descarga directa de mods desde el launcher. 
                """,
                "open_app":"Abrir",
                "exit_app":"Cerrar",
                "report": "Reportar",
                "no_close_app": "Mantener ejecutándose",
                "error_installing": "Error hay una instalación en curso",
                "error_installation": "Ha habido un error",
                "open_browser": "Abrir navegador",
                "refresh": "Actualizar",
                "open_folder": "Abrir Folder",
                "total_mods_loaded": "Total mods cargados",
                "limit_search": "Límite",
                'loaders': "Cargadores",
                "imgs": "Imagenes",
                'categories':'Categorias: ',
                "search": "Buscar",
                "next_pag": "Siguiente",
                "back_pag": "Atras",
                "init_mc": "Iniciando",
                "mc_path_create": "Directorio creado",
                "profile_path_created": "Archivo creado",
                "java_path_": "Ubicación de java",
                "mc_path_": "Ubicación de Minecraft",
                "opacity": "Opacidad general",
                "need_restart": "Ciertas configuraciones realizadas necesitan de reinicio",
                "version_not_installed": "No disponible",
                "settings_saved": "Configuraciones guardadas",
                "setting_saved_description": "Se han guardado las siguientes configuraciones",
                "session_closed": "Se ha cerrado tu sesión",
                "session_closed_description": "Has cerrado sesión como",
                "session_close": "Cerrar sesión",
                "select_javaw": "Seleccionar",
                "select_img_wallpaper": "Seleccionar la imagen para cambiar el fondo de pantalla",
                "discord_rich": "Mostrar el launcher en discord",
                "ram_usage": "Cambiar el uso de RAM en Minecraft",
                "wallpaper_save": "Cambiar la imagen de fondo del lanzador",
                "save_": "Guardar",
                "restore_": "Restaurar",
                "delete_all_": "Borrar todo",
                "delete_all_confirmation_": "Borrar todos los datos almacenados",
                "invalid_version": "Versión no válida",
                "invalid_version_description": "Es una versión válida",
                "installation_needed": "Necesita instalación",
                "installation_sucess": "Instalando versión...",
                "installation_sucess_description": "No se ha encontrado, se instalará",
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
                "error_java_path":"No tienes java instalado",
                "error_select_dialg_description": "Elige una de las versiones mostradas en el apartado",
                "button_login": "Iniciar Sesión",
                "name_user": "Nombre de usuario",
                "name_user_hint": "Escribe tu nombre de usuario",
                "email_user": "Correo",
                "email_user_hint": "Escribe tu Correo",
                "pass_user": "Contraseña",
                "pass_user_hint": "Escribe tu contraseña",
                "versions_dropdown_label": "Elige la versión",
                "versions_dropdown": "Versiones",
                "sections_main": "Consola",
                "sections_profile": "PERFIL",
                "sections_settings": "AJUSTES",
                "play_button": "JUGAR",
                "play_button_started": "JUGANDO",
                "play_button_installing": "Instalando...",
                "lenguaje_dropdown": "Idioma",
                "lenguaje_dropdown_description": "Selecciona el idioma",
                "Resolution_perfil": "Resolución recomendada de la imagen 256x256 o 512x512"
            },
            "en": {
                "local_downloaded": "Locally downloaded content",
                "new_update_button": "Update",
                "new_update_description": "A new update has been found, click the button to update.",
                "new_update":"Update available",
                "internet_no_found": "Does not have internet connection",
                "error_search_mod_name":"Could not search, please try typing manually",
                "markdown_news":"""
## 🆕 What's new in version 0.1.6

- 🎨 **Revamped graphical interface**: the entire design now looks more attractive and modern.  
- 🌐 **Improved Modrinth section**: redesigned exploration and view, with more content and a richer experience.  
- 🧩 **Optimized and better structured code** for easier maintenance and future improvements.  
- 🖱️ **Added Stray system**: allows keeping the launcher in the background without constantly opening and closing it (recommended).  
- 🐞 **Fixed several bugs**: the window name is now displayed correctly and accidental closing from the taskbar is prevented.  
- 🎨 **Theme color history**: the last 6 selected colors are saved.  
- ☕ **Java information panel**: includes useful details along with the latest updates.  
- 🔔 **Auto-update button**: appears only when a new launcher version is available.  
- 🧭 **Improved navigation buttons**: both for internal mods and Modrinth mods, offering smoother navigation.  
- 🚧 **Coming soon in Modrinth**: direct mod downloading from the launcher.  
                """,
                "open_app":"Open",
                "exit_app":"Close",
                "report": "Report",
                "no_close_app": "Keep running",
                "error_installing": "Error an installation is in progress",
                "error_installation": "There has been an error",
                "open_browser": "Open browser",
                "refresh": "Update",
                "open_folder": "Open folder",
                "total_mods_loaded": "Total mods loaded",
                "limit_search": "Limit",
                'loaders': "Loader",
                "imgs": "Images",
                'categories':'Categories: ',
                "search": "Search",
                "next_pag": "Next",
                "back_pag": "Back",
                "init_mc": "Starting",
                "mc_path_create": "created directory",
                "profile_path_created": "file created",
                "java_path_": "Location of Java",
                "mc_path_": "Location of Minecraft",
                "opacity":"Overall opacity",
                "need_restart": "Certain settings made require a restart",
                "version_not_installed": "Not available",
                "settings_saved": "Saved settings",
                "setting_saved_description": "The following settings have been saved",
                "session_closed": "Your session has been closed",
                "session_closed_description": "You have logged out as",
                "session_close": "Log out",
                "select_javaw": "Select",
                "select_img_wallpaper": "Select the image to change the wallpaper",
                "discord_rich": "Display on discord launcher",
                "ram_usage": "Change usage RAM minecraft",
                "wallpaper_save": "Change background image launcher",
                "save_": "Save",
                "restore_": "Restore",
                "delete_all_": "Delete all",
                "delete_all_confirmation_": "Delete all stored data",
                "console_msg": "This is the console",
                "invalid_version": "Invalid Version",
                "invalid_version_description": "it is an invalid version",
                "installation_needed": "Need installation",
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
                "error_java_path":"You don't have java installed",
                "error_select_dialg_description": "Choose one of the versions shown in the section",
                "button_login": "Sign in",
                "name_user": "Username",
                "name_user_hint": "Write your username",
                "email_user": "Email",
                "email_user_hint": "Write your email",
                "pass_user": "Password",
                "pass_user_hint": "Write your password",
                "versions_dropdown_label": "Select version",
                "versions_dropdown": "Versions",
                "sections_main": "Console",
                "sections_profile": "PROFILE",
                "sections_settings": "SETTINGS",
                "play_button": "PLAY",
                "play_button_started": "PLAYING",
                "play_button_installing": "Installing...",
                "lenguaje_dropdown": "Language",
                "lenguaje_dropdown_description": "Select the language",
                "Resolution_perfil": "Recommended image resolution 256x256 or 512x512"
            }
        }
    
    def get(self):
        return self.list_traductions