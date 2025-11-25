from pathlib import Path
import json
import os
from typing import Any
from core.utils import random_hex_color, return_appdata
import shutil

def find_java() -> str | None:
    """Intenta localizar un ejecutable de Java de forma robusta.

    Estrategia:
    1. Variables de entorno (JAVA_HOME/JDK_HOME) con soporte para macOS "Contents/Home".
    2. Búsqueda en rutas conocidas según el sistema operativo.
    3. Detección rápida vía PATH (shutil.which).
    4. Escaneo recursivo superficial (hasta 3 niveles) en rutas conocidas buscando bin/java*.
    """

    java_execs = ["java", "java.exe", "javaw.exe"]

    def _candidate_from_home(home: str) -> str | None:
        home_p = Path(home)
        # Añadir variante macOS si el usuario exportó JAVA_HOME apuntando a la raíz del bundle
        mac_variants = [home_p, home_p / "Contents" / "Home"] if "darwin" in os.sys.platform else [home_p]
        for base in mac_variants:
            bin_dir = base / "bin"
            if not bin_dir.exists():
                continue
            for exe in java_execs:
                exe_path = bin_dir / exe
                if exe_path.exists():
                    return str(exe_path)
        return None

    # 1. Variables de entorno
    for var in ("JAVA_HOME", "JDK_HOME"):
        env_val = os.environ.get(var)
        if env_val:
            found = _candidate_from_home(env_val)
            if found:
                return found

    # 2. PATH rápida (si ya está accesible)
    for exe in ("javaw.exe" if os.name == "nt" else "java", "java.exe", "javaw.exe"):
        path_found = shutil.which(exe)
        if path_found:
            return path_found

    # 3. Rutas conocidas según SO
    search_roots: list[Path] = []
    if os.name == "nt":
        search_roots += [
            Path("C:/Program Files/Java"),
            Path("C:/Program Files (x86)/Java"),
        ]
    else:  # POSIX
        if "darwin" in os.sys.platform:  # macOS
            search_roots += [Path("/Library/Java/JavaVirtualMachines")]
        else:  # Linux / otros Unix
            search_roots += [
                Path("/usr/lib/jvm"),
                Path("/usr/java"),
                Path("/opt/java"),
            ]

    patterns = ["jdk*", "zulu*", "temurin*", "openjdk*", "java*"]
    for root in search_roots:
        if not root.exists():
            continue
        for pattern in patterns:
            for candidate in sorted(root.glob(pattern)):
                # Intentar variantes estándar y macOS
                found = _candidate_from_home(str(candidate))
                if found:
                    return found

    # 4. Escaneo recursivo superficial (hasta 3 niveles) buscando bin/java*
    for root in search_roots:
        if not root.exists():
            continue
        depth_limit = 3
        try:
            for path in root.rglob('bin'):
                # limitar profundidad para evitar explorar demasiado
                if len(path.relative_to(root).parts) > depth_limit:
                    continue
                for exe in java_execs:
                    exe_path = path / exe
                    if exe_path.exists():
                        return str(exe_path)
        except Exception:
            pass

    return None

class ConfigManager:
    def __init__(self, page, path: str = "KitsuneLauncher/config.json", default_config: dict = None):
        self.page = page
        self.config_path = Path(return_appdata()) / path
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        mc_path = str(self.check_minecraft_path(Path(return_appdata()) / ".minecraft"))
        
        self.default_config = default_config or {
            "username": None,
            "uuid": None,
            "java_path": find_java(),
            "last_version_played": [None, None],
            "ram": "4",
            "premium_mode": False,
            # Dejar vacío por defecto; se generará en runtime en función de la versión de Java
            "jvm_args": [],
            "minecraft_path": mc_path,
            "app_background": True,
            "language": "en",
            "photo_perfil": "iconos/photo.png",
            "discord_presence": True,
            "wallpaper_launcher": "imgs/wallpaper.png",
            "primary_color_schema": "#e85d04",
            "light_color_schema": "#f48c06",
            "dark_color_schema": "#ff7b00",
            "last_colors": [
                random_hex_color(), random_hex_color(),
                random_hex_color(), random_hex_color(),
                random_hex_color(), random_hex_color(),
            ],
            "opacity": 5
        }

        self.config = self.load()
        
    def check_minecraft_path(self, path):
        launcher_mc_path = Path(path)
        
        if not launcher_mc_path.is_dir():
            launcher_mc_path.mkdir(parents=True, exist_ok=True)
            
            return launcher_mc_path
        return launcher_mc_path

    def _java_major(self) -> int:
        """Detecta la versión mayor de Java desde la ruta configurada."""
        try:
            jp = self.config.get("java_path")
            if not jp or not Path(jp).exists():
                return -1
            import subprocess, re
            completed = subprocess.run([jp, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out = (completed.stdout or "") + (completed.stderr or "")
            # version "1.8.0_382" -> 8 ; version "21.0.2" -> 21
            m = re.search(r'version\s+"(?:(?:1\.)?(?P<maj1>\d+))', out)
            if m and m.group("maj1"):
                maj = int(m.group("maj1"))
                return 8 if maj == 1 else maj
        except Exception:
            pass
        return -1

    def set_jvm_args(self):
        """Actualiza los JVM args según la RAM y capacidades de la versión de Java."""
        ram_val = str(self.config.get('ram') or "4")
        args = [
            f"-Xmx{ram_val}G",
            f"-Xms{ram_val}G",
        ]
        try:
            if self._java_major() >= 21:
                args.append("--enable-native-access=ALL-UNNAMED")
        except Exception:
            # Si falla la detección, simplemente no añadimos el flag opcional
            pass
        self.config["jvm_args"] = args

    def load(self) -> dict:
        if self.config_path.exists():
            self.page.logger.info(f"✅ Se han cargado todas las configuraciones")
            try:
                with self.config_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Asegurarse de que todos los valores faltantes se agreguen
                    for key, value in self.default_config.items():
                        data.setdefault(key, value)
                    return data
            except Exception as e:
                return self.page.logger.error(f"⚠️ Error al cargar la configuración, usando valores predeterminados: {e}")
        
        self.page.logger.info(f"♻ Se han cargado todas las configuraciones predeterminadas") 
        return self.default_config.copy()

    def save(self):
        with self.config_path.open("w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)
            self.page.logger.info(f"✅ Se han guardado las configuraciones")
        

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        self.config[key] = value
        if key == "ram":
            self.set_jvm_args()
        self.page.logger.info(f"🔧 Configuración actualizada: {key} = {value}")

    def reset(self):
        """Restablece a la configuración predeterminada."""
        self.config = self.default_config.copy()
        self.page.logger.warning("♻️ Configuración restablecida a valores predeterminados.")
        self.save()