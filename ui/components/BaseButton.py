import flet as ft

from ui.resources.Fonts import BaseFonts

class BaseButtonMaker:
    def __init__(self, page):
        self.page = page
        self.default_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            overlay_color=ft.Colors.WHITE10,
            color={
                ft.ControlState.DEFAULT: ft.Colors.WHITE,
                ft.ControlState.HOVERED: page.global_vars["primary_color"],
            },
            bgcolor=ft.Colors.WHITE10
        )

    def create_button(self, text:str | None =None, col=None, data=None, on_click=None, width=None, height=None,
            disabled=False, style=None, text_style=None, tooltip=None,
            icon_src:str=None, icon=None, icon_color=None, icon_width:int = 30, icon_height:int = 30, expand:int|bool = None):
        
        controls = []
        if icon_src is not None:
            controls.append(
                ft.Image(src=icon_src, width=icon_width, height=icon_height)
            )
        if text is not None:
            controls.append(
                ft.Text(value=text, style=text_style, expand=expand)
            )

        if len(controls) == 1:
            content = controls[0]
        else:
            content = ft.Row(
                controls=controls,
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=expand,
                tight=True
            )
        return ft.OutlinedButton(
            expand=expand,
            tooltip=tooltip,
            data=data,
            content=content,
            col=col,
            icon_color=icon_color,
            width=width,
            height=height,
            disabled=disabled,
            on_click=on_click,
            style=style or self.default_style,
        )