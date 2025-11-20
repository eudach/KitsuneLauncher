import os
import flet as ft

from ui.components.BaseButton import BaseButtonMaker
from ui.resources.Fonts import BaseFonts

from core.utils import alerta

class ButtonNavigationSearch:
    def __init__(self, page):
        self.page = page
    
    def get_next(self, on_click_next) -> ft.FloatingActionButton:
        page = self.page
        return ft.FloatingActionButton(
            on_click=on_click_next,
            icon=ft.Icons.NAVIGATE_NEXT,
            bgcolor=self.page.launcher.config.get("dark_color_schema"),
            mini=True,
            shape=ft.RoundedRectangleBorder(radius=5),
        )
    
    def get_home(self, on_click_home) -> ft.FloatingActionButton:
        page = self.page
        return ft.FloatingActionButton(
            on_click=on_click_home,
            icon=ft.Icons.HOME,
            mini=True,
            bgcolor=self.page.launcher.config.get("light_color_schema"),
            shape=ft.RoundedRectangleBorder(radius=5),
        )
    
    def get_back(self, on_click_back) -> ft.FloatingActionButton:
        page = self.page
        return ft.FloatingActionButton(
            on_click=on_click_back,
            icon=ft.Icons.NAVIGATE_BEFORE,
            bgcolor=self.page.launcher.config.get("dark_color_schema"),
            mini=True,
            shape=ft.RoundedRectangleBorder(radius=5),
        )

class ButtonSave:
    
    def __init__(self, page, save_settings):
        self.page = page
        
        self.button_save = BaseButtonMaker(page).create_button(
            text=page.t('save_'),
            on_click=save_settings,
            width=page.window.width *0.12,
            height=page.window.height*0.07,
            icon_src="iconos/save.png",
            icon_width = 20, icon_height = 20,
            style=ft.ButtonStyle(
                overlay_color=ft.Colors.BLACK12,
                color={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                    ft.ControlState.HOVERED: ft.Colors.GREEN,
                    },
                side=ft.BorderSide(1, color=ft.Colors.WHITE10),
                shape=ft.RoundedRectangleBorder(10),
                bgcolor=ft.Colors.WHITE10,
            ),
            text_style=ft.TextStyle(
                size=page.window.width/60,
                font_family=BaseFonts.buttons
                
            )
        )
        
    def get(self):
        return self.button_save
    
class ButtonReport:
    
    def __init__(self, page):
        self.page = page
        
        self.button_report = BaseButtonMaker(page).create_button(
            text=page.t('report'),
            width=page.window.width *0.15,
            height=page.window.height*0.07,
            icon_src="iconos/report.png",
            icon_width = 50, icon_height = 50,
            on_click=self.send_report,
            style=ft.ButtonStyle(
                overlay_color=ft.Colors.BLACK12,
                color={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                    ft.ControlState.HOVERED: ft.Colors.YELLOW,
                    },
                side=ft.BorderSide(1, color=ft.Colors.WHITE10),
                shape=ft.RoundedRectangleBorder(10),
                bgcolor=ft.Colors.WHITE10
            ),
            text_style=ft.TextStyle(
                size=page.window.width/60,
                font_family=BaseFonts.buttons
                
            )
        )
    
    async def send_report(self, e):
        self.page.launch_url("https://github.com/eudach/KitsuneLauncher/issues")
        
    def get(self):
        return self.button_report
    
class ButtonDeleteAll:
    
    def __init__(self, page):
        self.page = page
        
        self.button_delete_all = BaseButtonMaker(page).create_button(
            text=page.t('delete_all_'),
            width=page.window.width *0.15,
            height=page.window.height*0.07,
            icon_src="iconos/trash.png",
            icon_width = 30, icon_height = 30,
            on_click=self.delte_all_data,
            style=ft.ButtonStyle(
                overlay_color=ft.Colors.BLACK12,
                color={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                    ft.ControlState.HOVERED: ft.Colors.RED,
                },
                side=ft.BorderSide(1, color=ft.Colors.WHITE10),
                shape=ft.RoundedRectangleBorder(10),
                bgcolor=ft.Colors.WHITE10,
            ),
            text_style=ft.TextStyle(
                size=page.window.width/60,
                font_family=BaseFonts.buttons
            )
        )
    
    async def clr_data_modal(self, e):
        try:
            
            self.page.logger.warning("Reseteando todas las configuraciones del usuario")
            self.page.launcher.config.reset()
            self.page.launcher.config.save()
            
            self.page.presence.update()
            self.page.stray.start()
            
            self.page.logger.info("Configuraciones reseteadas, redirigiendo al login")
            self.page.go("/login")
        except Exception as ex:
            self.page.logger.error(f"Error reseteando configuraciones: {ex}")
    
    async def delte_all_data(self, e):
        page = self.page
        
        if page.global_vars["installing_minecraft_version"]:
            page.open(
                alerta(titulo="Error", descripcion=page.t("error_installing"))
            )
            return 
        
        alrt = ft.AlertDialog(
            icon=ft.Icon(name=ft.Icons.WARNING_AMBER),
            title=ft.Text(value=page.t("data_elimination"), text_align=ft.TextAlign.CENTER),
            content=ft.Text(value=page.t("data_elimination_sure"), text_align=ft.TextAlign.CENTER),
            actions=[
                ft.TextButton(
                    text=page.t("data_question_y"),
                    on_click=self.clr_data_modal,
                    style=ft.ButtonStyle(
                        color=page.global_vars["primary_color"]
                    )
                ),
                ft.TextButton(
                    text="No",
                    style=ft.ButtonStyle(
                        color=page.global_vars["primary_color"]
                    ),
                    on_click=lambda e: page.close(alrt)
                ),
            ],
            bgcolor=ft.Colors.BLACK,
            shape=ft.BeveledRectangleBorder(3),
            icon_color=page.global_vars["primary_color"],
            alignment=ft.alignment.center,
        )
        page.open(
            alrt
        )
    
    def get(self):
        return self.button_delete_all


class ButtonPlay:
    
    def __init__(self, page, jugar_func):
        self.page = page
        
        
        self.button_play = ft.ElevatedButton(
            col=3.5,
            on_click=jugar_func,
            
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5),
                bgcolor= {
                    ft.ControlState.DEFAULT: page.global_vars["primary_color"],
                    ft.ControlState.DISABLED: ft.Colors.GREY,
                }
            ),
            content=ft.ResponsiveRow(
                spacing=0,
                run_spacing=0,
                expand=True,
                controls=[
                    ft.Image(
                        col=3,
                        src="iconos/gamepad.png",
                        width=40, height=40
                    ),
                    ft.Container(
                        col=8,
                        content=ft.Text(
                            expand=True,
                            no_wrap=True,
                            overflow="ellipsis",
                            value=page.t("play_button"),
                            style=ft.TextStyle(
                                size=page.window.width/25,
                                font_family=BaseFonts.titles,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE
                            )
                        ),
                        alignment=ft.alignment.center
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
        )
        
    def get(self):
        return self.button_play
    


class ButtonsSections:
    
    def __init__(self, page, function_content):
        self.page = page
        self.function_content = function_content
        self.icon_colour = ft.Colors.WHITE
        self.base_width=page.window.width/4
        self.base_height=page.window.height/10
        self.col_base = 4
    
    async def get_perfil(self):
        page = self.page
        return BaseButtonMaker(page).create_button(
            text=page.t("sections_profile"),
            on_click=self.function_content,
            icon_src="iconos/perfil.png",
            col=self.col_base,
            data="perfil",
            width=self.base_width,
            height=self.base_height,
            style=ft.ButtonStyle(
                shape=ft.ContinuousRectangleBorder(3),
                color=ft.Colors.WHITE,
                side={
                    ft.ControlState.DEFAULT: ft.BorderSide(0, color=ft.Colors.TRANSPARENT),
                    ft.ControlState.HOVERED: ft.BorderSide(2, color=ft.Colors.WHITE10)
                    },
                overlay_color=ft.Colors.BLACK12,
                icon_size=page.window.width /50,
            ),
            text_style=ft.TextStyle(
                size=page.window.width /40,
                font_family=BaseFonts.titles,
                weight=ft.FontWeight.BOLD,
                word_spacing=100
            )
        )
    
    async def get_settings(self):
        page = self.page
        return BaseButtonMaker(page).create_button(
            text=page.t("sections_settings"),
            data="settings",
            col=self.col_base,
            icon_src="iconos/settings.png",
            on_click=self.function_content,
            width=self.base_width,
            height=self.base_height,
            style=ft.ButtonStyle(
                shape=ft.ContinuousRectangleBorder(3),
                color=ft.Colors.WHITE,
                side={
                    ft.ControlState.DEFAULT: ft.BorderSide(0, color=ft.Colors.TRANSPARENT),
                    ft.ControlState.HOVERED: ft.BorderSide(2, color=ft.Colors.WHITE10)
                    },
                overlay_color=ft.Colors.BLACK12,
                icon_size=page.window.width /50,
            ),
            text_style=ft.TextStyle(
                size=page.window.width /40,
                font_family=BaseFonts.titles,
                weight=ft.FontWeight.BOLD,
            )
        )
    
    async def get_modrinth(self):
        page = self.page
        
        return BaseButtonMaker(page).create_button(
            text="MORINTH",
            col=self.col_base,
            data='modrinth',
            disabled=not page.internet_check.connected,
            on_click=self.function_content,
            icon_src="iconos/modrinth.png",
            icon_width = 35, icon_height = 35,
            width=self.base_width,
            height=self.base_height,
            style=ft.ButtonStyle(
                shape=ft.ContinuousRectangleBorder(3),
                color=ft.Colors.WHITE,
                side={
                    ft.ControlState.DEFAULT: ft.BorderSide(0, color=ft.Colors.TRANSPARENT),
                    ft.ControlState.HOVERED: ft.BorderSide(2, color=ft.Colors.WHITE10)
                    },
                overlay_color=ft.Colors.BLACK12,
                icon_size=page.window.width /50
            ),
            text_style=ft.TextStyle(
                size=page.window.width /40,
                font_family=BaseFonts.titles,
                weight=ft.FontWeight.BOLD,
            )
        )

class ButtonOpenFolder:
    
    def __init__(self, page, type:str="mod"):
        self.page = page
        
        type_path_map = {
            "mod": "mods",
            "resourcepack": "resourcepacks",
            "shader": "shaderpacks"
        }
        last_path = type_path_map[type]
        
        self.button_open_folder = BaseButtonMaker(page).create_button(
            icon=ft.Icons.FOLDER_OPEN,
            text=page.t('open_folder'),
            icon_src="iconos/folder.png",
            icon_width = 15, icon_height = 15,
            on_click=lambda a: os.startfile(f"{page.launcher.minecraft_path}\\{last_path}"),
            expand=False
        )
        
    def get(self):
        return self.button_open_folder
    
class ButtonNewVersion:
    
    def __init__(self, page, on_click):
        self.page = page
        
        self.button_new_version = BaseButtonMaker(page).create_button(
            icon=ft.Icons.FOLDER_OPEN,
            text=page.t('new_update_button'),
            on_click=on_click,
            expand=True,
            width=170
        )
        
    def get(self):
        return self.button_new_version
    

class ButtonRefreshModsLocal:
    
    def __init__(self, page, on_click):
        self.page = page
        
        self.button_refresh_mods_local = BaseButtonMaker(page).create_button(
            icon=ft.Icons.REFRESH,
            text=page.t('refresh'),
            icon_src="iconos/rocket.png",
            icon_width = 20, icon_height = 20,
            on_click=on_click,
            expand=False
        )
        
    def get(self):
        return self.button_refresh_mods_local

class ButtonNavigationDescription:
    def __init__(self, page):
        self.page = page
    
    def get_next(self, on_click, have_next:bool=True, slug_next_mod:str=None) -> ft.FloatingActionButton:
        return ft.FloatingActionButton(
            icon=ft.Icons.NAVIGATE_NEXT,
            disabled=have_next,
            on_click=on_click,
            bgcolor=self.page.launcher.config.get("dark_color_schema"),
            shape=ft.RoundedRectangleBorder(radius=5),
            mini=True,
            data=slug_next_mod
        )
    
    def get_home(self, function_search_mod) -> ft.FloatingActionButton:
        return ft.FloatingActionButton(
            icon=ft.Icons.HOME,
            shape=ft.RoundedRectangleBorder(radius=5),
            data='description',
            bgcolor=self.page.global_vars["primary_color"],
            mini=True,
            on_click=function_search_mod,
        )
        
    def get_before(self, on_click, have_before:bool=True, slug_before_mod:str=None) -> ft.FloatingActionButton:
        return ft.FloatingActionButton(
            
            icon=ft.Icons.NAVIGATE_BEFORE,
            disabled=have_before,
            on_click=on_click,
            bgcolor=self.page.launcher.config.get("dark_color_schema"),
            shape=ft.RoundedRectangleBorder(radius=5),
            mini=True,
            data=slug_before_mod
        )
    
class ButtonOpenBrowser:
    
    def __init__(self, page, open_mod_in_browser, data):
        self.page = page
        
        
        self.button_open_browser = ft.FloatingActionButton(
            text=page.t("open_browser"),
            icon=ft.Icons.TOUCH_APP,
            on_click=open_mod_in_browser,
            data=data,
            bgcolor=page.global_vars["primary_color"],
            shape=ft.RoundedRectangleBorder(radius=5),
            mini=True,
        )
        
    def get(self):
        return self.button_open_browser
    
class ButtonCloseSession:
    
    def __init__(self, page, close_session):
        self.page = page
        
        
        self.button_close_session = BaseButtonMaker(page).create_button(
            text=page.t('session_close'),
            disabled=page.temp_config_modrinth["minecraft_started"],
            width=page.window.width*0.25,
            height=page.window.height*0.10,
            on_click=close_session,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(10),
                overlay_color=ft.Colors.WHITE10,
                color={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                    ft.ControlState.HOVERED: page.global_vars["primary_color"],
                    },
                bgcolor=ft.Colors.WHITE10,
                side=ft.BorderSide(1, color=ft.Colors.WHITE10),
            ),
            text_style=ft.TextStyle(
                font_family=BaseFonts.buttons,
                size=page.window.width/35,
            )
        )
        
    def get(self):
        return self.button_close_session
    

class ButtonOpenLatestLog:
    
    def __init__(self, page):
        self.page = page
        
        
        self.button_open_latest_log = BaseButtonMaker(page).create_button(
            text=page.t('open_app') + " latest.log",
            on_click=self.__open_latest_log
        )
        
    def __open_latest_log(self, e):
        if not self.page.launcher.open_minecraft_logs("latest.log"):
            self.page.logger.error("( latest.log ) File Not Found")
            self.page.update()
    
    def get(self):
        return self.button_open_latest_log
    

class ButtonOpenDebugLog:
    
    def __init__(self, page):
        self.page = page
        
        
        self.button_open_debug_log = BaseButtonMaker(page).create_button(
            text=page.t('open_app') + " debug.log",
            on_click=self.__open_debug_log
        )
        
    def __open_debug_log(self, e):
        if not self.page.launcher.open_minecraft_logs("debug.log"):
            self.page.logger.error("( debug.log ) File Not Found")
            self.page.update()
    
    def get(self):
        return self.button_open_debug_log