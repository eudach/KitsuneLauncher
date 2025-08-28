import flet as ft 
from core.utils import TYPES_COLORS

class AppBarWindows:
    
    def __init__(self, page, minimize, maximize, close_windows):
        self.appbar = ft.Container(
            height=50,
            content=ft.Row(
                controls=[
                    ft.WindowDragArea(
                        maximizable=True,
                        content=ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Image(src=page.window.icon, width=70, height=40, scale=1, opacity=0.8),
                                    margin=0,
                                    padding=0
                                ),
                                ft.Text("Kitsune Launcher", font_family="Katana", size=page.ancho / 40, text_align=ft.TextAlign.CENTER)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        expand=True
                    ),
                    ft.IconButton(
                        icon=ft.Icons.MINIMIZE,
                        icon_color=ft.Colors.WHITE,
                        on_click=minimize,
                        scale=0.9
                    ),
                    ft.IconButton(
                        icon=ft.Icons.SQUARE_OUTLINED,
                        icon_color=ft.Colors.WHITE,
                        on_click=maximize,
                        scale=0.9
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_color=ft.Colors.WHITE,
                        on_click=close_windows,
                        scale=0.9
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            bgcolor=TYPES_COLORS[page.launcher.config.get("opacity")][1],
            border_radius=5
        )
        
    def get(self):
        return self.appbar