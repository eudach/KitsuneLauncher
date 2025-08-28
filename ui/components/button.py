import os
import flet as ft

class ButtonListSearchModrinth:
    def __init__(self, page):
        self.page = page
    
    async def get_next(self, on_click_next):
        page = self.page
        return ft.OutlinedButton(
            text=page.t("next_pag"),
            on_click=on_click_next,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(10),
                overlay_color=ft.Colors.WHITE10,
                color={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                    ft.ControlState.HOVERED: page.color_init,
                    },
                bgcolor=ft.Colors.WHITE10,
                side=ft.BorderSide(1, color=ft.Colors.WHITE10),
            )
        )
    
    async def get_home(self, on_click_home):
        page = self.page
        return ft.OutlinedButton(
            text=page.t("home_pag"),
            on_click=on_click_home,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(5),
                overlay_color=ft.Colors.WHITE10,
                color={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                    ft.ControlState.HOVERED: page.color_init,
                    },
                bgcolor=ft.Colors.WHITE10,
                side=ft.BorderSide(1, color=ft.Colors.WHITE10),
                
            )
        )
    
    async def get_back(self, on_click_back):
        page = self.page
        return ft.OutlinedButton(
            text=page.t("back_pag"),
            on_click=on_click_back,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(10),
                overlay_color=ft.Colors.WHITE10,
                color={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                    ft.ControlState.HOVERED: page.color_init,
                    },
                bgcolor=ft.Colors.WHITE10,
                side=ft.BorderSide(1, color=ft.Colors.WHITE10),
                
            )
        )

class ButtonSave:
    
    def __init__(self, page, text_save, save_settings):
        self.page = page
        
        
        self.button_save = ft.OutlinedButton(                    
            content=text_save,
            width=page.ancho*0.10,
            height=page.alto*0.07,
            on_click=save_settings,
            style=ft.ButtonStyle(
                overlay_color=ft.Colors.WHITE10 ,
                color={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                    ft.ControlState.HOVERED: ft.Colors.GREEN,
                    },
                side=ft.BorderSide(1, color=ft.Colors.WHITE10),
                shape=ft.RoundedRectangleBorder(10),
                bgcolor=ft.Colors.WHITE10
            ),
        )
        
    def get(self):
        return self.button_save
    
class ButtonDeleteAll:
    
    def __init__(self, page, text_delete_all, delte_all_data):
        self.page = page
        
        
        self.button_delete_all = ft.OutlinedButton(           
            content=text_delete_all,
            width=page.ancho*0.10,
            height=page.alto*0.07,
            style=ft.ButtonStyle(
                overlay_color=ft.Colors.WHITE10,
                color={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                    ft.ControlState.HOVERED: ft.Colors.RED,
                    ft.ControlState.FOCUSED: ft.Colors.RED_ACCENT_100
                },
                side=ft.BorderSide(1, color=ft.Colors.WHITE10),
                shape=ft.RoundedRectangleBorder(10),
                bgcolor=ft.Colors.WHITE10
            ),
            on_click=delte_all_data
        )
        
    def get(self):
        return self.button_delete_all


class ButtonPlay:
    
    async def hover_bttn_play(self, e):
        page = self.page
        color_ = self.page.launcher.config.get("primary_color_schema")
        page.button_play.bgcolor =self.page.launcher.config.get("dark_color_schema") if page.button_play.bgcolor == color_ else color_
        page.button_play.update()
    
    def __init__(self, page, text_play, jugar_func):
        self.page = page
        
        
        self.button_play = ft.FloatingActionButton(
            width=300,
            height=60,
            bgcolor=page.color_init,
            
            content=ft.Container(content=
                ft.Row
                (
                    [
                        ft.Icon(ft.Icons.PLAY_ARROW),
                        text_play
                    ], 
                    alignment="center",
                    spacing=5
                ),
                on_click=jugar_func,
                on_hover=self.hover_bttn_play
            , expand=True, padding=0),
            shape=ft.RoundedRectangleBorder(radius=5),
            mini=True,
        )
        
    def get(self):
        return self.button_play

class ButtonsSections:
    
    def __init__(self, page, function_content):
        self.page = page
        self.function_content = function_content
    
    async def get_perfil(self):
        page = self.page
        return ft.OutlinedButton(
            text=page.t("sections_profile"),
            icon="PERSON",
            on_click=self.function_content,
            col=4,
            data="perfil",
            icon_color=ft.Colors.WHITE,
            width=page.ancho/4,
            height=page.alto/10,
            
            style=ft.ButtonStyle(
                shape=ft.ContinuousRectangleBorder(3),
                color=ft.Colors.WHITE,
                side={
                    ft.ControlState.DEFAULT: ft.BorderSide(0, color=ft.Colors.TRANSPARENT),
                    ft.ControlState.HOVERED: ft.BorderSide(2, color=ft.Colors.WHITE10)
                    },
                overlay_color=ft.Colors.BLACK12,
                icon_size=page.ancho/50,
                text_style=ft.TextStyle(
                    size=page.ancho/50,
                    font_family="Monkey",
                    weight=ft.FontWeight.W_100,
                )
                
            )
        )
    
    async def get_settings(self):
        page = self.page
        return ft.OutlinedButton(
            text=page.t("sections_settings"),
            data="settings",
            col=4,
            on_click=self.function_content,
            icon="SETTINGS", 
            icon_color=ft.Colors.WHITE,
            width=page.ancho/4,
            height=page.alto/10,
            
            style=ft.ButtonStyle(
                shape=ft.ContinuousRectangleBorder(3),
                color=ft.Colors.WHITE,
                side={
                        ft.ControlState.DEFAULT: ft.BorderSide(0, color=ft.Colors.TRANSPARENT),
                        ft.ControlState.HOVERED: ft.BorderSide(2, color=ft.Colors.WHITE10)
                    },
                overlay_color=ft.Colors.BLACK26,
                icon_size=page.ancho/50,
                text_style=ft.TextStyle(
                    size=page.ancho/50,
                    font_family="Monkey",
                    weight=ft.FontWeight.W_100,
                ),
                
                
            )
        )
    
    async def get_modrinth(self):
        page = self.page
        return ft.OutlinedButton(
            text="Modrinth",
            col=4,
            data='modrinth',
            on_click=self.function_content,
            icon="AUTO_AWESOME_OUTLINED",
            icon_color=ft.Colors.WHITE,
            width=page.ancho/4,
            height=page.alto/10,
            
            
            style=ft.ButtonStyle(
                shape=ft.ContinuousRectangleBorder(3),
                color=ft.Colors.WHITE,
                side={
                        ft.ControlState.DEFAULT: ft.BorderSide(0, color=ft.Colors.TRANSPARENT),
                        ft.ControlState.HOVERED: ft.BorderSide(2, color=ft.Colors.WHITE10)
                    },
                overlay_color=ft.Colors.BLACK12,
                icon_size=page.ancho/50,
                text_style=ft.TextStyle(
                    size=page.ancho/50,
                    font_family="Monkey",
                    weight=ft.FontWeight.W_100,
                ),
            )   
        )

class ButtonOpenFolder:
    
    def __init__(self, page,):
        self.page = page
        
        
        self.button_open_folder = ft.OutlinedButton(
            icon=ft.Icons.FOLDER_OPEN,
            text=page.t('open_folder'),
            on_click=lambda a: os.startfile(f"{page.launcher.minecraft_path}/mods"),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(10),
                overlay_color=ft.Colors.WHITE10,
                color={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                    ft.ControlState.HOVERED: page.color_init,
                },
                bgcolor=ft.Colors.WHITE10,
                side=ft.BorderSide(1, color=ft.Colors.WHITE10),
                
            )
        )
        
    def get(self):
        return self.button_open_folder
    
    
class ButtonRefreshModsLocal:
    
    def __init__(self, page, refresh_list_mods_local):
        self.page = page
        
        
        self.button_refresh_mods_local = ft.OutlinedButton(
            icon=ft.Icons.REFRESH,
            text=page.t('refresh'),
            on_click=refresh_list_mods_local,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(10),
                overlay_color=ft.Colors.WHITE10,
                color={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                    ft.ControlState.HOVERED: page.color_init,
                    },
                bgcolor=ft.Colors.WHITE10,
                side=ft.BorderSide(1, color=ft.Colors.WHITE10),
                
            )
        )
        
    def get(self):
        return self.button_refresh_mods_local
    

class ButtonNextPagMod:
    
    def __init__(self, page, have_next_mod, next_mod, go_mod_description):
        self.page = page
        
        
        self.button_next_pag_mod = ft.OutlinedButton(
            text=page.t("next_pag"),
            icon=ft.Icons.ARROW_FORWARD_IOS,
            disabled=have_next_mod,
            expand=True, data=next_mod,
            on_click=go_mod_description,
            
            style=ft.ButtonStyle(
                color={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                    ft.ControlState.HOVERED: page.launcher.config.get("primary_color_schema"),
                    },
                shape=ft.RoundedRectangleBorder(10),
                side={
                    ft.ControlState.DEFAULT: ft.BorderSide(1, color=ft.Colors.WHITE10),
                    ft.ControlState.HOVERED: ft.BorderSide(1, color=page.launcher.config.get("primary_color_schema")),
                    },
                text_style=ft.TextStyle(
                    size=page.ancho/70,
                    font_family="liberation"
                ),
                overlay_color=ft.Colors.TRANSPARENT
            ),
        )
        
    def get(self):
        return self.button_next_pag_mod
    
class ButtonBackPagMod:
    
    def __init__(self, page, have_back_mod, back_mod, go_mod_description):
        self.page = page
        
        
        self.button_back_pag_mod = ft.OutlinedButton(
            text=page.t("back_pag"),
            icon=ft.Icons.ARROW_BACK_IOS,
            disabled=have_back_mod,
            expand=True,
            data=back_mod, on_click=go_mod_description,
            
            style=ft.ButtonStyle(
                color={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                    ft.ControlState.HOVERED: page.launcher.config.get("primary_color_schema"),
                    },
                shape=ft.RoundedRectangleBorder(10),
                side={
                    ft.ControlState.DEFAULT: ft.BorderSide(1, color=ft.Colors.WHITE10),
                    ft.ControlState.HOVERED: ft.BorderSide(1, color=page.launcher.config.get("primary_color_schema")),
                    },
                text_style=ft.TextStyle(
                    size=page.ancho/70,
                    font_family="liberation"
                ),
                overlay_color=ft.Colors.TRANSPARENT
            ),
        )
        
    def get(self):
        return self.button_back_pag_mod
    
class ButtonHomePagMod:
    
    def __init__(self, page, search_mods):
        self.page = page
        
        
        self.button_back_pag_mod = ft.OutlinedButton(
            text=page.t("home_pag"),
            icon=ft.Icons.HOME_FILLED,
            expand=True,
            on_click=search_mods,
            data='description',
            
            style=ft.ButtonStyle(
                color={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                    ft.ControlState.HOVERED: page.launcher.config.get("primary_color_schema"),
                    },
                shape=ft.RoundedRectangleBorder(10),
                side={
                    ft.ControlState.DEFAULT: ft.BorderSide(1, color=ft.Colors.WHITE10),
                    ft.ControlState.HOVERED: ft.BorderSide(1, color=page.launcher.config.get("primary_color_schema")),
                    },
                text_style=ft.TextStyle(
                    size=page.ancho/70,
                    font_family="liberation"
                ),
                overlay_color=ft.Colors.TRANSPARENT
            ),
            
        )
        
    def get(self):
        return self.button_back_pag_mod
    
    

class ButtonOpenBrowser:
    
    def __init__(self, page, open_mod_in_browser, data):
        self.page = page
        
        
        self.button_open_browser = ft.OutlinedButton(
            text=page.t("open_browser"),
            icon=ft.Icons.TOUCH_APP,
            expand=True,
            on_click=open_mod_in_browser,
            data=data,
            style=ft.ButtonStyle(
                color={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                    ft.ControlState.HOVERED: page.launcher.config.get("primary_color_schema"),
                    },
                shape=ft.RoundedRectangleBorder(10),
                side={
                    ft.ControlState.DEFAULT: ft.BorderSide(1, color=ft.Colors.WHITE10),
                    ft.ControlState.HOVERED: ft.BorderSide(1, color=page.launcher.config.get("primary_color_schema")),
                    },
                text_style=ft.TextStyle(
                    size=page.ancho/70,
                    font_family="liberation"
                ),
                overlay_color=ft.Colors.TRANSPARENT
            ),
            
        )
        
    def get(self):
        return self.button_open_browser
    
    

class ButtonCloseSession:
    
    def __init__(self, page, close_session):
        self.page = page
        
        
        self.button_close_session = ft.OutlinedButton(                           
            content=ft.Text(
                value=page.t('session_close'),
                font_family="liberation",
                size=page.ancho/35,
                text_align=ft.TextAlign.CENTER
            ),
            width=page.ancho*0.20,
            height=page.alto*0.10,
            on_click=close_session,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(10),
                overlay_color=ft.Colors.WHITE10,
                color={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                    ft.ControlState.HOVERED: page.color_init,
                    },
                bgcolor=ft.Colors.WHITE10,
                side=ft.BorderSide(1, color=ft.Colors.WHITE10),
                
                ),
        )
        
        
    def get(self):
        return self.button_close_session