import flet as ft 
from core.utils import TYPES_COLORS

class SliderOpacity:
    
    def __init__(self, page):
        self.slider_opacity = ft.Slider(
            min=0,
            max=6,
            value=page.launcher.config.get("opacity"),
            label="{value}°",
            divisions=6,
            inactive_color=TYPES_COLORS[page.launcher.config.get("opacity")][0],
            active_color=page.color_init
        )
    
    def get(self):
        return self.slider_opacity
    
class SliderRam:
    
    def __init__(self, page, ram_change_function):
        self.slider_ram = ft.Slider(
            on_change=ram_change_function,
            min=2,
            max=16,
            round=0,
            value=page.launcher.config.get("ram"),
            divisions=14,
            label="{value}GB",
            inactive_color=TYPES_COLORS[page.launcher.config.get("opacity")][0],
            active_color=page.color_init
        )
    
    def get(self):
        return self.slider_ram