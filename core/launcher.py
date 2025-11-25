import asyncio
import re

from pathlib import Path
from typing import Any, List
import flet as ft
import subprocess
import minecraft_launcher_lib
import threading
from minecraft_launcher_lib import utils
import json
import os
import time
import uuid

from ui.resources.Fonts import BaseFonts

from core.settings import ConfigManager
from core.utils import alerta

from dataclasses import dataclass
import base64
import zipfile

def check_username(username:str) -> bool:
    return re.fullmatch(r'[a-zA-Z0-9_]{3,16}', username)

def get_offline_uuid(username: str) -> str:
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, "OfflinePlayer:" + username))

@dataclass
class ResourcePack:
    name: str
    path: Path
    
    def get_icon(self) -> str:
        
        ruta = self.path
        try:
            if ruta.is_dir():
                pack_path = ruta / "pack.png"
                if pack_path.exists():
                    return base64.b64encode(pack_path.read_bytes()).decode("utf-8")

            elif ruta.suffix == ".zip":
                with zipfile.ZipFile(ruta) as zf:
                    if "pack.png" in zf.namelist():
                        return base64.b64encode(zf.read("pack.png")).decode("utf-8")

        except Exception:
            return None
        
        return None

@dataclass
class ShaderPack:
    name: str
    path: Path


@dataclass
class Mod:
    name: str
    path: Path

class KitsuneLauncher:
    def __init__(self, page):
        self.page = page
        self.config = ConfigManager(page)
        self._minecraft_path = None
        self._java_path = None
        self._username = None
        self._version = None
        
    def open_minecraft_logs(self, type:str):
        # arg type: latest.log [ latest.log or debug.log]
        from sys import platform as _plat
        log_path = Path(self.minecraft_path) / "logs" / type
        try:
            if not log_path.exists():
                return False
            if _plat.startswith("win"):
                os.startfile(str(log_path))
            elif _plat == "darwin" or _plat.startswith("mac"):
                subprocess.run(["open", str(log_path)], check=False)
            else:
                subprocess.run(["xdg-open", str(log_path)], check=False)
            return True
        except Exception:
            return False

    @property
    def minecraft_path(self):
        if self._minecraft_path is None:
            self._minecraft_path = self.config.get("minecraft_path")
        return self._minecraft_path
    
    def check_vanilla_ver(self):
        #minecraft_launcher_lib.utils.is_vanilla_version(e[0])
        
        ...

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

        disponibles = {
            "1.7.10": False,
            "1.8.9": False,
            "1.12.2": False,
            "1.16.5": False,
            "1.19.2": False,
            "1.20.1": False,
            "1.21.1": False,
            "1.21.5": False,
            "1.21.8": False,
            "1.21.9": False
        }
        

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
        from pathlib import Path
        p = Path(new_path)
        # If a directory is provided, try to locate a java executable inside common subpaths.
        if p.is_dir():
            candidates = [
                p / "bin" / "java",
                p / "bin" / "java.exe",
                p / "Contents" / "Home" / "bin" / "java",  # macOS JDK bundle structure
            ]
            for c in candidates:
                if c.exists():
                    new_path = str(c)
                    p = c
                    break
        if p.exists():
            if save:
                self.config.set("java_path", str(p))
                self._java_path = str(p)  # cache update
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
            return [
                    Mod(
                        name=entry.name,
                        path=Path(entry)
                    )
                    for entry in os.scandir(pathh) if ".jar" in entry.name]
        else:
            return []
        
    def get_list_resourcepacks(self) -> List[ResourcePack]:
        pathh = Path(self.minecraft_path) / "resourcepacks"
        if pathh.is_dir():
            return [
                ResourcePack(
                    name=entry.name,
                    path=Path(entry)
                )
                for entry in pathh.iterdir()
            ]
        else:
            return []
        
    def get_list_shaderpacks(self) -> list:
        pathh = Path(self.minecraft_path) / "shaderpacks"
        if pathh.is_dir():
            return [
                ShaderPack(
                    name=entry.name,
                    path=Path(entry)
                )
                for entry in pathh.iterdir() if Path(entry).suffix != ".txt"
            ]
        else:
            return []
    
    def set_version(self, version: tuple) -> bool:
        version = tuple(version)
        if (Path(self.minecraft_path) / "versions" / version[0]).is_dir():
            self.config.set("last_version_played", version)
            self._version = version
            return True
        return False
    
    def check_launcher_profiles(self):
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
            return True
    
    
    def init(self):
        self.check_launcher_profiles()
        
        installed = utils.get_installed_versions(self.minecraft_path)
        if not any(v["id"] == self.last_played_version[0] for v in installed):
            self.config.set("last_version_played", [None, None])
            self._version = None
    
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
        
    def __finalizar_instalacion(self, version):
        page = self.page
        page.global_vars["option_change_installed"].content.controls[0].src = "iconos/icono.png"
        page.global_vars["option_change_installed"].update()

        self.set_version((version, True))
        
        page.button_play.disabled = False
        page.button_play.content.controls[1].content.value = page.t("play_button")
        page.progress_time_remain.visible = False
        page.progress_bar.visible = False
        page.global_vars["installing_minecraft_version"] = False
        page.update()

    def instalar_minecraft_en_hilo(self, version):
        page = self.page
        minecraft_path = self.minecraft_path
        
        if not page.internet_check.connected:
            page.open(alerta(titulo="Error", descripcion=page.t("error_installation")))
            return
        
        self.max_value = [0]
        self.install_start_time = time.perf_counter()

        callback = {
            "setStatus": self.mostrar_linea_en_consola,
            "setProgress": self.__set_progress,
            "setMax": lambda value: self.__maximum(self.max_value, value)
        }

        page.progress_bar.visible = True
        page.progress_bar.update()

        async def _install_task():
            try:
                # Ejecuta la función bloqueante en un thread separado
                await asyncio.to_thread(
                    minecraft_launcher_lib.install.install_minecraft_version,
                    version, minecraft_path, callback
                )
                page.global_vars["installing_minecraft_version"] = True
            except Exception as e:
                # ESTO se ejecuta en el event loop principal: seguro para UI
                page.open(alerta(titulo="Error", descripcion=page.t("error_installation")))
                return

            # Aquí también estamos en el event loop principal: actualizar UI es seguro
            self.__finalizar_instalacion(version)

        # Lanza la tarea en background (no bloquea la UI)
        page.run_task(_install_task)

    def mostrar_linea_en_consola(self, linea):
        controls = self.page.Text_Console.controls
        # Solo recorta si se pasa el límite
        exceso = len(controls) - 200
        if exceso > 0:
            del controls[:exceso]

        if "Sound engine started" in linea:
            self.page.button_play.content.controls[1].content.value = self.page.t("play_button_started")
            self.page.button_play.update()
        if "error" in linea:
            self.page.logger.print_console_warn(linea)
        else:
            self.page.logger.print_console_info(linea)

        if self.page.global_vars["current_section"] is None or self.page.global_vars["current_section"] != "console":
            return
        if self.page.global_vars["current_section"] == 'console':
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

    def __detectar_version_java(self, java_path: str) -> int:
        """Ejecuta '<java> -version' y devuelve la versión mayor (8, 11, 17, 21...)."""
        try:
            if not java_path or not Path(java_path).exists():
                return -1
            import re
            p = subprocess.run([java_path, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out = (p.stdout or "") + (p.stderr or "")
            m = re.search(r'version\s+"(?:(?:1\.)?(?P<maj1>\d+))', out)
            if m and m.group("maj1"):
                maj = int(m.group("maj1"))
                return 8 if maj == 1 else maj
        except Exception:
            pass
        return -1

    def __sanear_jvm_args(self, args, java_major: int, ram_gb: str) -> list:
        """Limpia o construye JVM args compatibles con la versión de Java y la RAM configurada."""
        safe = []
        seen = set()

        def add(a: str):
            if not a:
                return
            a = a.strip()
            if not a or a in seen:
                return
            seen.add(a)
            safe.append(a)

        base = args or []

        # Si no hay args, añadir memoria base según config
        if not base:
            add(f"-Xmx{ram_gb}G")
            add(f"-Xms{ram_gb}G")

        for a in base:
            if not a:
                continue
            # Quitar flag no soportado en Java < 21
            if a.startswith("--enable-native-access") and (java_major < 21):
                continue
            add(a)

        # Asegurar flags de memoria si faltan
        if not any(x.startswith("-Xmx") for x in safe):
            add(f"-Xmx{ram_gb}G")
        if not any(x.startswith("-Xms") for x in safe):
            add(f"-Xms{ram_gb}G")

        return safe
    
    
    def start_minecraft(self):
        page = self.page
        username = self.username
        uuid = self.config.get("uuid")
        if uuid is None:
            uuid = get_offline_uuid(username)
            page.launcher.config.set("uuid", uuid)
            page.launcher.config.save()
            
        minecraft_path = self.minecraft_path
        version = self.last_played_version[0]
        jvm_args = self.config.get("jvm_args")
        ram = str(self.config.get("ram") or "4")

        # Detectar versión de Java y sanear args para evitar errores de VM
        java_path = self.java_path
        java_major = self.__detectar_version_java(java_path)
        safe_jvm_args = self.__sanear_jvm_args(jvm_args, java_major, ram)

        try:
            page.logger.info(f"Java path: {java_path}")
            page.logger.info(f"Java major: {java_major}")
            page.logger.info(f"JVM args: {safe_jvm_args}")
        except Exception:
            pass
                    
        def __ejecutar_minecraft(comando):
            try:
                import sys
                popen_kwargs = {
                    "stdout": subprocess.PIPE,
                    "stderr": subprocess.STDOUT,
                    "text": True,
                    "bufsize": 1,
                    "cwd": minecraft_path,
                    "encoding": "utf-8",  # Fuerza UTF-8
                    "errors": "replace"
                }
                # Solo usar flags especiales en Windows; en macOS/Linux causarían AttributeError
                if sys.platform.startswith("win"):
                    popen_kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW | subprocess.HIGH_PRIORITY_CLASS
                proceso = subprocess.Popen(comando, **popen_kwargs)
            except Exception as e:
                with open(f"{self.minecraft_path}/error.log", "w", encoding="utf-8") as f:
                    f.write(str(e))
            
            page.temp_config_modrinth["minecraft_started"] = True
            page.presence.update()
            page.button_play.content.controls[1].content.value = page.t("init_mc")
            page.button_play.disabled = True
            page.button_play.update()
            
                
            for linea in proceso.stdout:
                self.mostrar_linea_en_consola(linea.strip())

            #MINECRAFT CLOSED
            proceso.wait()
            page.temp_config_modrinth["minecraft_started"] = False
            page.presence.update()
            page.button_play.bgcolor=page.global_vars["primary_color"]
            page.button_play.content.controls[1].content.value = page.t("play_button")
            page.button_play.disabled = False
            page.button_play.update()
            
            
        # Preparar opciones
        options:minecraft_launcher_lib.types.MinecraftOptions = {
            'username': username,
            'uuid': uuid,
            'demo': False,
            'token': '',
            "executablePath": java_path,
            "jvmArguments": safe_jvm_args,
            "launcherName": "Kitsune",
            "launcherVersion": "0.1",
            "gameDirectory": str(minecraft_path),
            # Deja que minecraft_launcher_lib gestione el directorio de natives
            # no forces "nativesDirectory" here
        }

        # Generar comando
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_path, options)
        minecraft_command = self.__limpiar_comando(minecraft_command)
        minecraft_command += ['--accessToken', '0', '--userType', 'legacy']
        
        # Lanzar Minecraft en un hilo para capturar la salida sin bloquear la app
        threading.Thread(target=__ejecutar_minecraft, args=(minecraft_command,), daemon=True).start()

