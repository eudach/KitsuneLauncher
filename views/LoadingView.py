import flet as ft
from flet_route import Params,Basket

def LoadingView(page:ft.Page, params:Params, basket:Basket):
    return ft.View(
        route="/loading",
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                    controls=[
                        ft.Image(src="icon.png", width=150, height=150),  # tu logo
                        ft.Text("Cargando Kitsune Launcher...", size=20, font_family="liberation", color=ft.Colors.WHITE),
                        ft.ProgressRing(color=ft.Colors.ORANGE)
                    ]
                )
            )
        ],
        bgcolor=ft.Colors.BLACK
    )