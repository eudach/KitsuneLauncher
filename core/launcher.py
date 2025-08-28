
import re
from core.settings import ConfigManager
from pathlib import Path
import flet as ft
import subprocess
import minecraft_launcher_lib
import threading
from minecraft_launcher_lib import utils
import json
import os
import time
import uuid
from core.utils import alerta

def check_username(username:str) -> bool:
    return re.fullmatch(r'[a-zA-Z0-9_]{3,16}', username)

def get_offline_uuid(username: str) -> str:
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, "OfflinePlayer:" + username))

class KitsuneLauncher:
    def __init__(self):
        self.config = ConfigManager()
        self._minecraft_path = None
        self._java_path = None
        self._username = None
        self._version = None
        self.page = None  # Se conecta luego con .set_page()

    def set_page(self, page):
        self.page = page

    @property
    def minecraft_path(self):
        if self._minecraft_path is None:
            self._minecraft_path = self.config.get("minecraft_path")
        return self._minecraft_path

    @property
    def java_path(self):
        if self._java_path is None:
            self._java_path = self.config.get("java_path")
        return self._java_path

    @property
    def username(self):
        if self._username is None:
            self._username = self.config.get("username")
        return self._username

    @property
    def last_played_version(self):
        if self._version is None:
            self._version = self.config.get("last_version_played")
        return self._version  # Tuple: (version, installed)
    
    @property
    def versions(self) -> list[tuple[str, bool]]:
        """
        Retorna una lista de versiones de Minecraft disponibles y/o instaladas.
        Cada tupla es: (version_id: str, instalada: bool)
        """
        try:
            disponibles = {
                e['id']: False for e in utils.get_version_list()
                if e['type'] == 'release'
            }
        except Exception:
            disponibles = {}

        instaladas = {
            e['id']: True for e in utils.get_installed_versions(self.minecraft_path)
            if e['type'] == 'release'
        }

        # Fusionar: lo instalado sobrescribe lo disponible
        versiones_combinadas = {**disponibles, **instaladas}

        return [(version, instalada) for version, instalada in versiones_combinadas.items()]

    def minecraft_is_installed(self) -> bool:
        return Path(self.minecraft_path).exists() and utils.is_minecraft_installed(self.minecraft_path)

    def set_java(self, new_path, save: bool = True) -> bool:
        if Path(new_path).exists():
            if save:
                self.config.set("java_path", new_path)
                self._java_path = new_path  # cache update
            return True
        return False

    def set_minecraft_path(self, new_value) -> bool:
        if Path(new_value).exists():
            self.config.set("minecraft_path", new_value)
            self._minecraft_path = new_value  # cache update
            return True
        return False

    def set_username(self, username: str):
        self.config.set("username", username)
        self._username = username  # cache update
        
    def get_list_mods(self) -> list:
        pathh = Path(self.minecraft_path) / "mods"
        if pathh.is_dir():
            return [(entry.name, Path(entry.path)) 
                    for entry in os.scandir(pathh) if ".jar" in entry.name]
        else:
            return []
    
    def set_version(self, version: tuple) -> bool:
        version = tuple(version)
        if (Path(self.minecraft_path) / "versions" / version[0]).is_dir():
            self.config.set("last_version_played", version)
            self._version = version
            return True
        return False
    
    def init(self):
        launcher_mc_path = Path(self.minecraft_path)
        
        if not launcher_mc_path.is_dir():
            launcher_mc_path.mkdir(parents=True, exist_ok=True)
            self.mostrar_linea_en_consola(f"✅ .minecraft {self.page.t('mc_path_create')}")
            
        launcher_file = Path(self.minecraft_path) / "launcher_profiles.json"
        
        """
        CHECK IF LAUNCHER PROFILES FILE EXISTS
        """
        if not launcher_file.exists():
            with launcher_file.open("w", encoding="utf-8") as f:
                json.dump(
                    {
                    "profiles": {},
                    "selectedProfile": "default"
                    }, f, indent=4
                )
                self.mostrar_linea_en_consola(f"✅ launcher_profiles.json {self.page.t('profile_path_created')}")
    
    def return_appdata(self) -> str:
        """
        RETURNS APPDATA
        """
        return os.getenv('APPDATA')
    
    def __actualizar_progress_bar(self, iteration, total):
        progreso = iteration / total
            
        self.page.progress_bar.value = progreso
        self.page.progress_bar.update()
        
        if iteration >= total:
            self.page.progress_bar.value = None
            self.page.progress_bar.update()
            
    def calcular_tiempo_restante_suavizado(self, progreso):
        elapsed = time.perf_counter() - self.install_start_time
        total_est = elapsed / progreso
        remaining = max(0, total_est - elapsed)

        mins_total, secs_total = divmod(int(total_est), 60)
        mins_remain, secs_remain = divmod(int(remaining), 60)

        return f"⏱ {mins_total:02d}:{secs_total:02d} total - ⏳ {mins_remain:02d}:{secs_remain:02d} restante"
    
    def __set_progress(self, value):
        progreso = value / self.max_value[0] if self.max_value[0] > 0 else 0
        tiempo_restante = self.calcular_tiempo_restante_suavizado(progreso)
        self.page.progress_time_remain.value = tiempo_restante
        self.page.progress_time_remain.visible=True
        self.page.progress_time_remain.update()

        self.__actualizar_progress_bar(value, self.max_value[0])
    
    def instalar_minecraft_en_hilo(self, page:ft.Page, version):
        self.page = page
        self.max_value = [0]
        minecraft_path = self.minecraft_path
        self.install_start_time = time.perf_counter()
        done_event = threading.Event()
        
        callback = {
            "setStatus": self.mostrar_linea_en_consola,
            "setProgress": self.__set_progress,
            "setMax": lambda value: self.__maximum(self.max_value, value)
        }
        
        self.page.progress_bar.visible=True
        self.page.progress_bar.update()
        
        def __run_installation():
            try:
                minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_path, callback)
            except:
                page.open(
                    alerta(
                        titulo="Error",
                        descripcion=page.t("error_installation")
                    )
                )

            done_event.set()
            if done_event:
                page.option_change_installed.content.controls[0].src = "icono.png"
                page.option_change_installed.update()
                self.set_version((version, True))
                self.page.button_play.disabled = False
                self.page.button_play.content.content.controls[1].value = page.t("play_button")
                self.page.progress_time_remain.visible = False
                self.page.progress_bar.visible = False
                self.page.button_play.update()
                self.page.progress_time_remain.update()
                self.page.progress_bar.update()

        page.run_thread(__run_installation)

    def mostrar_linea_en_consola(self, linea):
        controls = self.page.Text_Console.controls
        # Solo recorta si se pasa el límite
        exceso = len(controls) - 200
        if exceso > 0:
            del controls[:exceso]

        color = ft.Colors.RED_300 if "ERROR" in linea.upper() else ft.Colors.WHITE

        controls.append(
            ft.Text(
                font_family="console",
                value=linea,
                size=self.page.ancho / 65,
                selectable=True,
                expand=True,
                color=color
            )
        )

        if self.page.current_section is None:
            return
        if self.page.current_section == 'console':
            self.page.Text_Console.update()
        
    def __maximum(self, max_value, value):
        self.max_value[0] = value
        
    def __limpiar_comando(self, cmd: list) -> list:
        filtros = {
            '-XstartOnFirstThread',
            '--demo',
            '--accessToken',
            'msa',
            '',
            '--userType'
        }
        return [x for x in cmd if x not in filtros]
    
    
    def start_minecraft(self, page:ft.Page):
        username = self.username
        uuid = self.config.get("uuid")
        if uuid is None:
            uuid = get_offline_uuid(username)
            page.launcher.config.set("uuid", uuid)
            page.launcher.config.save()
            
        minecraft_path = self.minecraft_path
        version = self.last_played_version[0]
        jvm_args = self.config.get("jvm_args")
            
        def __ejecutar_minecraft(comando):
            try:
                flags = subprocess.CREATE_NO_WINDOW | subprocess.HIGH_PRIORITY_CLASS
                proceso = subprocess.Popen(
                    comando,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    creationflags=flags,
                    cwd=minecraft_path
                )
            except Exception as e:
                with open(f"{self.minecraft_path}/error.log", "w", encoding="utf-8") as f:
                    f.write(str(e))
            
            page.presence.update()
            page.button_play.content.content.controls[1].value = page.t("init_mc")
            page.button_play.disabled = True
            page.button_play.update()
            page.temp_config_modrinth["minecraft_started"] = True
                
            for linea in proceso.stdout:
                self.mostrar_linea_en_consola(linea.strip())

            #MINECRAFT CLOSED
            proceso.wait()
            page.presence.update()
            page.button_play.bgcolor=page.color_init
            page.button_play.content.content.controls[1].value = page.t("play_button")
            page.button_play.disabled = False
            page.temp_config_modrinth["minecraft_started"] = False
            page.button_play.update()
            
        # Preparar opciones
        options:minecraft_launcher_lib.types.MinecraftOptions = {
            'username': username,
            'uuid': uuid,
            'demo': False,
            'token': '',
            "executablePath": self.java_path,
            "jvmArguments": jvm_args,
            "launcherName": "Kitsune",
            "launcherVersion": "0.1",
            "gameDirectory": str(minecraft_path),
            "nativesDirectory": str(minecraft_path)
        }

        # Generar comando
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_path, options)
        minecraft_command = self.__limpiar_comando(minecraft_command)
        minecraft_command += ['--accessToken', '0', '--userType', 'legacy']
        
        # Lanzar Minecraft en un hilo para capturar la salida sin bloquear la app
        threading.Thread(target=__ejecutar_minecraft, args=(minecraft_command,), daemon=True).start()
        
