from pathlib import Path
import json
import os
from typing import Any
from core.utils import random_hex_color, return_appdata

def default_java_path():
    """Intenta encontrar una instalación predeterminada de Java 17 en el sistema."""
    if os.name == "darwin":  # macOS
        base = Path("/Library/Java/JavaVirtualMachines/")
    elif os.name == "nt":  # Windows
        base = Path("C:/Program Files/Java/")
    elif os.name == "posix":  # Linux
        base = Path("/usr/lib/jvm/")
    else:
        return None


    
    paths = sorted(base.glob("jdk-17*"))
    for path in reversed(paths):  # Priorizar versiones más recientes
        exe = path / "bin" / "javaw.exe"
        if exe.exists():
            return str(exe)
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
            "java_path": default_java_path(),
            "last_version_played": [None, None],
            "ram": "4",
            "premium_mode": False,
            "jvm_args": ["-Xmx4G", "-Xms4G", "--enable-native-access=ALL-UNNAMED"],
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

    def set_jvm_args(self):
        self.config["jvm_args"] = [
            f"-Xmx{self.config['ram']}G",
            f"-Xms{self.config['ram']}G",
            "--enable-native-access=ALL-UNNAMED"
        ]

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