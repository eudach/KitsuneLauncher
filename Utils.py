import asyncio
import threading
import flet as ft
from minecraft_launcher_lib import utils
import os
import minecraft_launcher_lib
import subprocess
from flet import AlertDialog, Text, Colors, BeveledRectangleBorder, alignment, Icons, Icon, TextAlign
import uuid


async def get_minecraft_dir(page):
    #RETURN .minecraft PATH
    minecraft_path = os.path.join(os.getenv('APPDATA'), page._minecraft)
    
    return str(minecraft_path)


async def minecraft_dir_exists(page):
    """ True If .minecraft exists False if not """
    path = get_minecraft_dir(page)
    if os.path.exists(path):
        if minecraft_launcher_lib.utils.is_minecraft_installed(path):
            return True
    
    return False

def minecraft_install():
    minecraft_launcher_lib.install()

async def get_java():
    pathhh = utils.get_java_executable()
    
    return str(pathhh)

async def alerta(titulo, descripcion):
    alrt = AlertDialog(
        icon=Icon(name=Icons.WARNING_AMBER),
        title=Text(value=titulo, text_align=TextAlign.CENTER),
        content=Text(value=descripcion, text_align=TextAlign.CENTER),
        bgcolor=Colors.BLACK,
        shape=BeveledRectangleBorder(3),
        icon_color=Colors.ORANGE,
        alignment=alignment.center,
    )
    return alrt

async def alerta_good(titulo, descripcion):
    alrt = AlertDialog(
        icon=Icon(name=Icons.CHECK_OUTLINED),
        title=Text(value=titulo, text_align=TextAlign.CENTER),
        content=Text(value=descripcion, text_align=TextAlign.CENTER),
        bgcolor=Colors.BLACK87,
        shape=BeveledRectangleBorder(3),
        icon_color=Colors.GREEN,
        alignment=alignment.center,
    )
    return alrt

async def valid_version(version:str) -> bool:
    mc_path = await get_minecraft_dir()
    if minecraft_launcher_lib.utils.is_version_valid(version, mc_path):
        return True
    else:
        return False

async def versiones() -> list:
    #GET ALL MINECRAFT VERSION (INSTALLED + DISPO)
    # TRUE = INSTALLED FLASE = NOT INSTALLED
    mc_path = await get_minecraft_dir()
    try:
        list_ver = [(e['id'], False) for e in utils.get_version_list() if e['type'] == 'release']
    except:
        list_ver = []
    list_ver_inst = [(e['id'], True) for e in utils.get_installed_versions(mc_path) if e['type'] == 'release']
    
    return list(list_ver_inst+list_ver)

def maximum(max_value, value):
    max_value[0] = value

def actualizar_progress_bar(page, iteration, total):
    progreso = iteration / total
    porcentaje = int(progreso * 100)

    page.progress_bar.value = progreso  # Flet espera un valor entre 0.0 y 1.0
    page.progress_bar.tooltip = ft.Tooltip(message=f"{porcentaje}%")
    page.progress_bar.update()
    
    if iteration >= total:
        page.progress_bar.value = None
        page.progress_bar.tooltip = ft.Tooltip(message=f"{porcentaje}% DONE")
        page.progress_bar.update()

async def iniciar_minecraft_no_premium(name, version, page):
    def mostrar_linea_en_consola(linea):
        if page.Text_Console is not None:
            if len(page.Text_Console.controls) > 200:
                page.Text_Console.controls.pop(0)
                
            page.Text_Console.controls.append(
                ft.Text(font_family="console", value=f'{linea}', size=page.ancho/65, selectable=True, expand=True)
            )
            page.Text_Console.update()
        else:
            pass

    def ejecutar_minecraft(comando):
        flags = 0
        if os.name == "nt":
            flags = subprocess.CREATE_NO_WINDOW

        proceso = subprocess.Popen(
            comando,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            creationflags=flags
        )

        for linea in proceso.stdout:
            mostrar_linea_en_consola(linea.strip())

        proceso.wait()
        page.presence.set(
            {
                "state": page.trad["user_state_discord_mainpage"][page.lenguage],
                "details": f"{page.username} {page.trad["user_state_discord_conect"][page.lenguage]}",
                "timestamps": {"start": page.times},
            }
        )
        

    # Directorio .minecraft
    minecraft_directori = await get_minecraft_dir()

    # Verifica si la versión está instalada
    versiones_instaladas = [
        e['id'] for e in utils.get_installed_versions(minecraft_directori)
        if e['type'] == 'release'
    ]

    if version not in versiones_instaladas:
        page.open(
            await alerta_good(
                titulo=page.trad['installation_sucess'][page.lenguage],
                descripcion=f"{version} {page.trad['installation_sucess_description'][page.lenguage]}"
            )
        )

        max_value = [0]
        callback = {
            "setStatus": mostrar_linea_en_consola,
            "setProgress": lambda value: actualizar_progress_bar(page, value, max_value[0]),
            "setMax": lambda value: maximum(max_value, value)
        }
        
        page.progress_bar.visible=True
        page.progress_bar.update()

        await asyncio.to_thread(
            minecraft_launcher_lib.install.install_minecraft_version,
            version,
            minecraft_directori,
            callback
        )

    # Preparar opciones
    options = {
        'username': name,
        'uuid': str(uuid.uuid4()),
        'demo': False,
        'token': '',
        "executablePath": page.java_path.replace('/', '//'),
        "jvmArguments": page.jvw_args,
        "launcherName": "Kitsune",
        "launcherVersion": "0.1",
    }

    # Generar comando
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directori, options)

    # Limpieza
    if '-XstartOnFirstThread' in minecraft_command:
        minecraft_command.remove('-XstartOnFirstThread')

    if '--demo' in minecraft_command:
        minecraft_command.remove('--demo')
    
    if '--accessToken' in minecraft_command:
        minecraft_command.remove('--accessToken')
    
    if '' in minecraft_command:
        minecraft_command.remove('')
    
    minecraft_command.append('--accessToken')
    minecraft_command.append('0')
    
    if '--userType' in minecraft_command:
        minecraft_command.remove('--userType')
    
    if 'msa' in minecraft_command:
        minecraft_command.remove('msa')
    
    minecraft_command.append('--userType')
    minecraft_command.append('legacy')
    

    print("Iniciando Minecraft...")

    # Lanzar Minecraft en un hilo para capturar la salida sin bloquear la app
    threading.Thread(target=ejecutar_minecraft, args=(minecraft_command,), daemon=True).start()
