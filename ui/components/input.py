import flet as ft

class InputMinecraftPath:
    
    def __init__(self, page, iconbutton_mc_path):
        self.page = page
    
        self.input_minecraft_path = ft.TextField(
            cursor_color=page.color_init,
            label=page.t('mc_path_'),
            bgcolor=ft.Colors.TRANSPARENT,
            border=ft.InputBorder.NONE,
            filled=True,
            value=page.launcher.minecraft_path,
            fill_color=ft.Colors.TRANSPARENT,
            max_lines=1,
            border_radius=3,
            focused_border_color=ft.Colors.WHITE,
            label_style=ft.TextStyle(color=ft.Colors.WHITE, font_family='liberation', size=page.ancho*0.018),
            multiline=True,
            suffix= iconbutton_mc_path,
            expand=True,
            read_only=True
        )
        
    def get(self):
        return self.input_minecraft_path
    

class InputModModrinth:
    
    def __init__(self, page, iconbutton_search_mod, search_mods):
        self.page = page
        self.input_mod_modrinth = ft.TextField(
            cursor_color=page.color_init,
            label=page.t("search"),
            bgcolor=ft.Colors.TRANSPARENT,
            border=ft.InputBorder.NONE,
            filled=True,
            fill_color=ft.Colors.TRANSPARENT,
            max_lines=1,
            border_radius=3,
            focused_border_color=ft.Colors.WHITE,
            label_style=ft.TextStyle(color=ft.Colors.WHITE,font_family='liberation', size=page.ancho*0.018),
            multiline=True,
            suffix= iconbutton_search_mod,
            expand=True,
            on_change=search_mods,
            hint_text="Sodium", 
        )
        
    def get(self):
        return self.input_mod_modrinth
    
class InputJavaPath:
    
    def __init__(self, page, iconbutton_java_path):
        self.page = page
        self.input_java_path = ft.TextField(
            cursor_color=page.color_init,
            label=page.t('java_path_'),
            bgcolor=ft.Colors.TRANSPARENT,
            border=ft.InputBorder.NONE,
            filled=True,
            value=page.launcher.java_path,
            fill_color=ft.Colors.TRANSPARENT,
            max_lines=1,
            border_radius=3,
            focused_border_color=ft.Colors.WHITE,
            label_style=ft.TextStyle(color=ft.Colors.WHITE,font_family='liberation', size=page.ancho*0.018),
            multiline=True,
            suffix= iconbutton_java_path,
            expand=True,
            read_only=True
        )
        
    def get(self):
        return self.input_java_path