import flet as ft

class Tooltip_installation:
    def __init__(self, page):
        
        self.tooltip_installation_needed = ft.Tooltip(
            message=page.t('installation_needed')
        )
        
    def get(self):
        return self.tooltip_installation_needed