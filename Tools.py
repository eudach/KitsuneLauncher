import json
import os
import threading
import time
import flet as ft
from minecraft_launcher_lib import utils
import minecraft_launcher_lib
import subprocess
from flet import AlertDialog, Text, Colors, BeveledRectangleBorder, alignment, Icons, Icon, TextAlign
import uuid
from pathlib import Path
from typing import Any
import colorsys

def default_java_path():
    base = Path("C:/Program Files/Java")
    if not base.exists():
        return None

    paths = sorted(base.glob("jdk*")) + sorted(base.glob("jre*"))
    for path in reversed(paths):
        exe = path / "bin" / "javaw.exe"
        if exe.exists():
            return str(exe)
    return None

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

class ConfigManager:
    def __init__(self, path: str = "KitsuneLauncher/config.json", default_config: dict = None):
        self.config_path = Path(os.getenv('APPDATA')) / path
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        self.default_config = default_config or {
            "language": "es",
            "username": None,
            "java_path": default_java_path(),
            "photo_perfil": "icon.png",
            "last_version_played": [None, None],
            "ram": "3",
            "premium_mode": False,
            "discord_presence": True,
            "wallpaper_launcher": "bg.png",
            "jvm_args": ["-Xmx3G", "-Xms3G", "--enable-native-access=ALL-UNNAMED"],
            "minecraft_path": str(Path(os.getenv('APPDATA')) / ".minecraft"),

            "primary_color_schema": "#ff8f00",
            "light_color_schema": "#f1b362",
            "dark_color_schema": "#c57813",
        }

        self.config = self.load()

    def set_jvm_args(self):
        self.config["jvm_args"] = [
            f"-Xmx{self.config['ram']}G",
            f"-Xms{self.config['ram']}G",
            "--enable-native-access=ALL-UNNAMED"
        ]

    def load(self) -> dict:
        if self.config_path.exists():
            try:
                with self.config_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Asegurarse de que todos los valores faltantes se agreguen
                    for key, value in self.default_config.items():
                        data.setdefault(key, value)
                    return data
            except Exception as e:
                pass
                #print(f"⚠️ Error al cargar la configuración, usando valores predeterminados: {e}")
        return self.default_config.copy()

    def save(self):
        with self.config_path.open("w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)
        

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        self.config[key] = value
        if key == "ram":
            self.set_jvm_args()
        #print(f"🔧 Configuración actualizada: {key} = {value}")

    def reset(self):
        """Restablece a la configuración predeterminada."""
        self.config = self.default_config.copy()
        #print("♻️ Configuración restablecida a valores predeterminados.")
        self.save()

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
    
    def set_version(self, version: tuple) -> bool:
        version = tuple(version)
        if (Path(self.minecraft_path) / "versions" / version[0]).is_dir():
            self.config.set("last_version_played", version)
            self._version = version
            return True
        return False
    
    def init(self):
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
                #print("✅ Archivo launcher_profiles.json creado.")
        else:
            pass
            #print("❕ Archivo launcher_profiles.json ya existe.")
    
    def return_appdata(self) -> str:
        """
        RETURNS APPDATA
        """
        return os.getenv('APPDATA')
    
    def __actualizar_progress_bar(self, iteration, total):
        progreso = iteration / total
        porcentaje = int(progreso * 100)

        self.page.progress_bar.value = progreso  # Flet espera un valor entre 0.0 y 1.0
        self.page.progress_bar.tooltip = ft.Tooltip(message=f"{porcentaje}%")
        self.page.progress_bar.update()
        
        if iteration >= total:
            self.page.progress_bar.value = None
            self.page.progress_bar.update()
    
    def __set_progress(self, value):
        now = time.time()
        elapsed = now - self.install_start_time
        progreso = value / self.max_value[0] if self.max_value[0] else 0
        
        if progreso > 0:
            total_est = elapsed / progreso
            remaining = max(0, total_est - elapsed)
            mins, secs = divmod(int(remaining), 60)
            self.estimated_time_remaining = f"{mins:02d}:{secs:02d}"
        else:
            self.estimated_time_remaining = "..."

        self.page.progress_time_remain.value = f"⏳ {self.estimated_time_remaining} restante"
        self.page.progress_time_remain.visible=True
        self.page.progress_time_remain.update()

        self.__actualizar_progress_bar(value, self.max_value[0])
    
    def instalar_minecraft_en_hilo(self, page, version):
        self.page = page
        self.max_value = [0]
        minecraft_path = self.minecraft_path
        self.install_start_time = time.time()
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
                        descripcion="No hay conexion a internet"
                    )
                )
            done_event.set()
            if done_event:
                self.set_version((version, True))
                self.page.boton_jugar.disabled = False
                self.page.boton_jugar.content.content.controls[1].value = page.t("play_button")
                self.page.progress_bar.tooltip = None
                self.page.progress_time_remain.visible = False
                self.page.progress_bar.visible = False
                self.page.boton_jugar.update()
                self.page.progress_time_remain.update()
                self.page.progress_bar.update()
            # Si el callback no soporta onFinish, puedes poner aquí: done_event.set()

        threading.Thread(target=__run_installation, daemon=True).start()
    
    def mostrar_linea_en_consola(self, linea):
        while len(self.page.Text_Console.controls) > 200:
            self.page.Text_Console.controls.pop(0)
            
        color = Colors.RED_300 if "ERROR" in linea.upper() else Colors.WHITE
        
        self.page.Text_Console.controls.append(
            ft.Text(font_family="console", value=f'{linea}', size=self.page.ancho/65, selectable=True, expand=True, color=color)
        )
        try:
            self.page.Text_Console.update()
        except:
            pass
        
    def __maximum(self, max_value, value):
        self.max_value[0] = value
        
    def __limpiar_comando(self, cmd: list) -> list:
        filtros = [
            '-XstartOnFirstThread',
            '--demo',
            '--accessToken',
            'msa',
            '',
            '--userType'
        ]
        return [x for x in cmd if x not in filtros]
    
    def start_minecraft(self, page):
        username = self.username
        minecraft_path = self.minecraft_path
        version = self.last_played_version[0]
        jvm_args = self.config.get("jvm_args")
        self.init()
            
        def __ejecutar_minecraft(comando):
            try:
                if not Path(minecraft_path).exists():
                    Path(minecraft_path).mkdir(parents=True, exist_ok=True)
                proceso = subprocess.Popen(
                    comando,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    cwd=minecraft_path
                )
            except Exception as e:
                with open("error.log", "w", encoding="utf-8") as f:
                    f.write(str(e))
            #print("Iniciando Minecraft...")
            self.mostrar_linea_en_consola("Iniciando Minecraft...")
            version_nombre = version
            version_details = ""
            if len(version.split("-"))>1:
                version_nombre = version.split("-")[0]
                version_details = version.split("-")[1]
                
                
            page.presence.set(
                {
                "state": f"{page.t("user_state_discord_playing")} {version_nombre} {version_details}",
                "details": f"{username} {page.t("user_state_discord_conect")}",
                "timestamps": {"start": page.discord_times},
                "buttons": [
                        {
                            "label": "Info",
                            "url": "https://github.com/eudach/KitsuneLauncher",
                        }
                    ],
                }
            )

            for linea in proceso.stdout:
                self.mostrar_linea_en_consola(linea.strip())

            proceso.wait()
            page.presence.set(
                {
                    "state": page.t("user_state_discord_mainpage"),
                    "details": f"{username} {page.t("user_state_discord_conect")}",
                    "timestamps": {"start": page.discord_times},
                    "buttons": [
                        {
                            "label": "Info",
                            "url": "https://github.com/eudach/KitsuneLauncher",
                        }
                    ],
                }
            )
            
        # Preparar opciones
        options:minecraft_launcher_lib.types.MinecraftOptions = {
            'username': username,
            'uuid': str(uuid.uuid4()),
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
        self.mostrar_linea_en_consola("todo correcto")
        # Lanzar Minecraft en un hilo para capturar la salida sin bloquear la app
        threading.Thread(target=__ejecutar_minecraft, args=(minecraft_command,), daemon=True).start()
        self.mostrar_linea_en_consola("yaaaaaaa")


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