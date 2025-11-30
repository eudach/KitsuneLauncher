import flet as ft


class IconButtonFilterSearch:
    
    def __init__(self, page, on_click):
        self.page = page
        
        self.iconbutton_filter = ft.IconButton(
            icon=ft.Icons.FILTER_ALT,
            icon_color='white',
            padding=0,
            hover_color=ft.Colors.BLACK12,
            on_click=on_click
        )
        
    def get(self):
        return self.iconbutton_filter
    
class IconButtonWallpaper:
    
    def __init__(self, page, bttn_img_wallpaper):
        self.page = page
        
        self.iconbutton_wallpaper = ft.IconButton(
            icon=ft.Icons.EDIT,
            on_click=bttn_img_wallpaper,
            bgcolor=ft.Colors.TRANSPARENT,
            icon_color=page.global_vars["primary_color"]
        )
        
    def get(self):
        return self.iconbutton_wallpaper
    
class IconButtonJavaPath:
    
    def __init__(self, page, bttn_select_java_bin):
        self.page = page
        
        self.iconbutton_java_path = ft.IconButton(
            icon=ft.Icons.FOLDER,
            icon_color=page.global_vars["primary_color"],
            padding=0,
            hover_color=ft.Colors.BLACK12,
            on_click=bttn_select_java_bin
        )
        
    def get(self):
        return self.iconbutton_java_path
    
class IconButtonMcPath:
    
    def __init__(self, page, bttn_check_minecraft_path):
        self.page = page
        
        self.iconbutton_mc_path = ft.IconButton(icon=ft.Icons.FOLDER, 
            icon_color=page.global_vars["primary_color"], 
            padding=0, 
            hover_color=ft.Colors.BLACK12, 
            on_click=bttn_check_minecraft_path
        )
        
    def get(self):
        return self.iconbutton_mc_path

class IconButtonSearchMod:
    """IconButton para disparar búsqueda de mods en Modrinth.

    Usado por `ui/sections/Modrinth.py`.
    """
    def __init__(self, page, on_click):
        self.page = page
        self.iconbutton_search_mod = ft.IconButton(
            icon=ft.Icons.SEARCH,
            icon_color=page.global_vars.get("primary_color", ft.Colors.WHITE),
            padding=0,
            hover_color=ft.Colors.BLACK12,
            on_click=on_click
        )

    def get(self):
        return self.iconbutton_search_mod