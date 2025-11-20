import logging

import flet as ft 
from core.utils import return_appdata
from ui.resources.Fonts import BaseFonts

def before_execute(before_func_name):
    """
    Decorador que ejecuta self.<before_func_name>(*args, **kwargs)
    antes del método real.
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            # Llama al método "before_func_name" de la instancia
            getattr(self, before_func_name)(*args, **kwargs)
            # Luego ejecuta el método real
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

class Logger:
    
    def __init__(self, page):
        self.console_open = False
        self.page = page
        self.page.Text_Console:ft.ListView = ft.ListView(  # type: ignore
            controls=[
                self.text("Console")
            ],
            spacing=5,
            padding=3,
            expand=True,
            auto_scroll=True
        )
        
        self.logger = logging.getLogger("Kitsune-Logger")
        self.logger.setLevel(logging.DEBUG)
        
        file_handler = logging.FileHandler(f"{return_appdata()}/KitsuneLauncher/app.log", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("[%(asctime)s]   [%(levelname)s] -> %(message)s"))
        
        self.logger.addHandler(file_handler)
        self.logger.info("Iniciando...")
    
    
        
    def text(self, txt:str, color:str='green'):
        return ft.Text(font_family=BaseFonts.console, value=txt, size=self.page.window.width/65, selectable=True, color=color, expand=True)
        
    def print_console_warn(self, message):
        self.page.Text_Console.controls.append(
            self.text(txt=f"[Logs System] -> {message}", color='red')
        )
    
    def print_console_info(self, message):
        self.page.Text_Console.controls.append(
            self.text(txt=f"[Logs System] -> {message}", color='green')
        )
    
    @before_execute("print_console_warn")
    def warning(self, message):
        self.logger.warning(message)
    
    @before_execute("print_console_warn")
    def error(self, message):
        self.logger.error(message)
        
    @before_execute("print_console_info")
    def info(self, message):
        self.logger.info(message)
    
    @before_execute("print_console_info")
    def debug(self, message):
        self.logger.debug(message)