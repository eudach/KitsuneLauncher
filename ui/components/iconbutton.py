import flet as ft


class IconButtonSearchMod:
    
    def __init__(self, page, search_mods):
        self.page = page
        
        self.iconbutton_search_mod = ft.IconButton(
            icon=ft.Icons.SEARCH,
            icon_color=page.color_init,
            padding=0,
            hover_color=ft.Colors.BLACK12,
            on_click=search_mods
        )
        
    def get(self):
        return self.iconbutton_search_mod
    
class IconButtonWallpaper:
    
    def __init__(self, page, bttn_img_wallpaper):
        self.page = page
        
        self.iconbutton_wallpaper = ft.IconButton(
            icon=ft.Icons.REPLAY,
            on_click=bttn_img_wallpaper,
            bgcolor=ft.Colors.TRANSPARENT,
            icon_color=page.color_init
        )
        
    def get(self):
        return self.iconbutton_wallpaper
    
class IconButtonJavaPath:
    
    def __init__(self, page, bttn_select_java_bin):
        self.page = page
        
        self.iconbutton_java_path = ft.IconButton(
            icon=ft.Icons.FOLDER,
            icon_color=page.color_init,
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
            icon_color=page.color_init, 
            padding=0, 
            hover_color=ft.Colors.BLACK12, 
            on_click=bttn_check_minecraft_path
        )
        
    def get(self):
        return self.iconbutton_mc_path