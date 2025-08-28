from flet import AlertDialog, Text, Colors, BeveledRectangleBorder, alignment, Icons, Icon, TextAlign
import flet as ft
import colorsys

DEFAULT_SIDE = {
    ft.ControlState.DEFAULT: ft.BorderSide(0, color=ft.Colors.TRANSPARENT),
    ft.ControlState.HOVERED: ft.BorderSide(2, color=ft.Colors.WHITE10),
}

TYPES_COLORS = {
    0 : ["transparent","transparent","transparent",],
    1: ["black12", "black12", "black26"],
    2: ["black12", "black26", "black38",],
    3: ["black26", "black38", "black45"],
    4: ["black38", "black45", "black54"],
    5: ["black45", "black54", "black87"],
    6: ["black54", "black87", "black87"],
}

def alerta(titulo, descripcion, success:bool=False) -> AlertDialog:
    """
    SUCESS si es true significa good
    false significa error
    """
    return AlertDialog(
        icon=Icon(name=Icons.CHECK_OUTLINED if success else Icons.WARNING_AMBER),
        title=Text(value=titulo, text_align=TextAlign.CENTER),
        content=Text(value=descripcion, text_align=TextAlign.CENTER),
        bgcolor=Colors.BLACK87 if success else Colors.BLACK,
        shape=BeveledRectangleBorder(3),
        icon_color=Colors.GREEN if success else Colors.ORANGE,
        alignment=alignment.center,
    )


def rgb2hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(
        int(rgb[0] * 255.0), int(rgb[1] * 255.0), int(rgb[2] * 255.0)
    )


def hex2rgb(value):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


def hex2hsv(value):
    rgb_color = hex2rgb(value)
    return colorsys.rgb_to_hsv(
        rgb_color[0] / 255, rgb_color[1] / 255, rgb_color[2] / 255
    )

def generar_degradado(color:str, diferencia=0.1)->tuple:
    """
    Devuelve los colores más oscuro y más claro a partir del color actual.
    `diferencia` define cuánto se aclara u oscurece (0.1 recomendado).
    """
    r, g, b = hex2rgb(color)
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

    # Más oscuro
    l_oscuro = max(l - diferencia, 0)
    r_o, g_o, b_o = colorsys.hls_to_rgb(h, l_oscuro, s)
    oscuro = rgb2hex((r_o, g_o, b_o))

    # Más claro
    l_claro = min(l + diferencia, 1)
    r_c, g_c, b_c = colorsys.hls_to_rgb(h, l_claro, s)
    claro = rgb2hex((r_c, g_c, b_c))

    return oscuro, claro