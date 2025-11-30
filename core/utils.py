import random
from flet import AlertDialog, Text, Colors, BeveledRectangleBorder, alignment, Icons, Icon, TextAlign
import flet as ft
import colorsys
import os
import hashlib
import asyncio
import sys

def close_alert(e:ft.ControlEvent):
    control = e.page.overlay[-1]
    if type(control) == ft.AlertDialog:
        e.page.close(control)
        e.page.update()

async def sha1_of_file_with_progress(path, on_progress=None, chunk_size=8192):
    """
    Calcula el SHA-1 de un archivo reportando progreso.

    Args:
        path (str): Ruta del archivo
        on_progress (callable): Callback (progress: float) entre 0.0 y 1.0
        chunk_size (int): Tamaño de cada bloque leído

    Returns:
        str: Hash SHA-1 en hexadecimal
    """
    file_size = os.path.getsize(path)
    read_size = 0
    hasher = hashlib.sha1()
    if path.is_dir():
        return None
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
            read_size += len(chunk)

            # calcular progreso
            progress = read_size / file_size

            # reportar a la UI
            if on_progress:
                on_progress(progress)

            # ceder el control al event loop (no bloquear la UI)
            await asyncio.sleep(0)

    return hasher.hexdigest()


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

def return_appdata(app_name: str = "KitsuneLauncher") -> str:
    """Devuelve la ruta base de datos de aplicación según el sistema operativo.

    Sistemas:
    - Windows: %APPDATA% (Roaming) si existe, fallback ~/AppData/Roaming
    - macOS: ~/Library/Application Support
    - Linux/Unix: $XDG_DATA_HOME si existe, fallback ~/.local/share

    Se añade el nombre de la aplicación como subdirectorio y se crea si no existe.
    """
    home = os.path.expanduser("~")

    if sys.platform.startswith("win"):
        # Preferir APPDATA (Roaming). LOCALAPPDATA suele usarse para datos locales, pero se pidió APPDATA.
        base = os.getenv("APPDATA") or os.path.join(home, "AppData", "Roaming")
    elif sys.platform == "darwin":
        base = os.path.join(home, "Library", "Application Support")
    else:
        # Linux / Unix (XDG). Si XDG_DATA_HOME no está definido, usar ~/.local/share
        base = os.getenv("XDG_DATA_HOME") or os.path.join(home, ".local", "share")

    path_final = os.path.join(base, app_name) if app_name else base
    os.makedirs(path_final, exist_ok=True)
    return path_final

def random_hex_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

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