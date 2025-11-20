
import flet as ft
from typing import Any, List, Literal, Union

from core.launcher import ResourcePack, Mod, ShaderPack
from ui.resources.Fonts import BaseFonts


class ContainerLocal:
    def __init__(
        self,
        page: ft.Page,
        on_click,
        data_list: Union[List[ResourcePack], List[Mod], List[ShaderPack]],
        tipo: Literal["mod", "resource", "shader"]
    ):
        self.page = page
        self.on_click = on_click
        self.data_list = data_list
        self.tipo = tipo.lower()
        self._build()

    # ------------------------------------------
    def _build(self):
        self.container_items = [
            ft.Row(
                key=i,
                controls=[
                    ft.Container(
                        expand=True,
                        padding=10,
                        border_radius=5,
                        bgcolor=ft.Colors.WHITE10,
                        alignment=ft.alignment.center,
                        content=self._get_content(file),
                    ),
                    ft.IconButton(
                        width=35,
                        height=35,
                        data=file.path,
                        content=ft.Image(
                            src="iconos/modrinth.png",
                            width=35,
                            height=35,
                        ),
                        on_click=self.on_click,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
            for i, file in enumerate(self.data_list)
        ]

    # ------------------------------------------
    def _get_content(self, file: ResourcePack):
        """Genera el contenido del contenedor según el tipo"""
        controls = []

        if self.tipo == "resource":
            try:
                img_b64 = file.get_icon()
                controls.append(
                    ft.Image(src_base64=img_b64, width=30, height=30, border_radius=5)
                )
            except Exception:
                # fallback si no existe el pack.png
                controls.append(
                    ft.Icon(name=ft.Icons.IMAGE_NOT_SUPPORTED, size=30, opacity=0.5)
                )

        # Agrega el nombre del archivo
        controls.append(
            ft.Text(
                value=file.name,
                size=self.page.window.width / 80,
                text_align=ft.TextAlign.LEFT,
                font_family=BaseFonts.texts,
                max_lines=1,
                expand=True,
            )
        )

        return ft.Row(
            controls=controls,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # ------------------------------------------
    def reload(self, data_list: list | None = None):
        """Recarga la lista (sin bloquear la UI si se llama desde un hilo)"""
        if data_list is not None:
            self.data_list = data_list
        self._build()

    # ------------------------------------------
    def get(self) -> list[ft.Control]:
        """Devuelve la lista de contenedores"""
        return self.container_items
