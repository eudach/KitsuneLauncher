import flet as ft
from ui.resources.Fonts import BaseFonts
from ui.components.toast import Toast, ToastType


def show_error_toast(page, value: str):
    page.toaster.show_toast(
        toast=Toast(
            content=ft.Text(
                value=value,
                expand=True,
                size=page.window.width / 80,
                max_lines=2,
                text_align=ft.TextAlign.LEFT,
                font_family=BaseFonts.texts,
            ),
            toast_type=ToastType.ERROR,
        ),
        duration=5,
    )

SIZES = {
    "title": lambda w: w / 40,
    "subtitle": lambda w: w / 80,
    "category": lambda w: w / 90,
    "chip": lambda w: w / 110,
}


def build_text(value: str, size: int, page, bold=False, expand=True):
    return ft.Text(
        value=value,
        size=size,
        font_family=BaseFonts.texts,
        text_align=ft.TextAlign.LEFT,
        weight=ft.FontWeight.BOLD if bold else None,
        expand=expand,
    )


def build_image(src: str, w: int, h: int, fit=ft.ImageFit.COVER, on_click=None, data=None, bgcolor=None):
    return ft.Container(
        padding=1,
        bgcolor=bgcolor or ft.Colors.BLACK12,
        border_radius=10,
        ink=bool(on_click),
        on_click=on_click,
        data=data,
        content=ft.Image(
            src=src,
            width=w,
            height=h,
            fit=fit,
            anti_alias=True,
            repeat=ft.ImageRepeat.NO_REPEAT,
            border_radius=ft.border_radius.all(10),
        ),
    )