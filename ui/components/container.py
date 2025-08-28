import flet as ft

class ContainerModLocal:
    def __init__(self, page, mod, search_mod_installed_modrinth):
        self.container_mod_local = ft.Container(
            padding=5,
            border_radius=5,
            bgcolor=ft.Colors.WHITE10,
            alignment=ft.alignment.center,
            ink=True,
            on_click=search_mod_installed_modrinth,
            data=f"{mod[0]}",
            content=ft.Row(
                controls=[
                    ft.Text(
                        value=f"{mod[0]}",
                        size=page.ancho/80,
                        text_align=ft.TextAlign.LEFT,
                        font_family="liberation",
                        max_lines=1,
                        expand=True,
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
        )
        
    def get(self):
        return self.container_mod_local