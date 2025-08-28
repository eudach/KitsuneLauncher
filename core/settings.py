from pathlib import Path
import json
import os
from typing import Any

def default_java_path():
    base = Path("C:/Program Files/Java")
    if not base.exists():
        return None
    
    paths = sorted(base.glob("jdk-24*"))
    for path in reversed(paths):  # Priorizar versiones más recientes
        exe = path / "bin" / "javaw.exe"
        if exe.exists():
            return str(exe)
    return None

class ConfigManager:
    def __init__(self, path: str = "KitsuneLauncher/config.json", default_config: dict = None):
        self.config_path = Path(os.getenv('APPDATA')) / path
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        self.default_config = default_config or {
            "username": None,
            "uuid": None,
            "java_path": default_java_path(),
            "last_version_played": [None, None],
            "ram": "3",
            "premium_mode": False,
            "jvm_args": ["-Xmx4G", "-Xms4G", "--enable-native-access=ALL-UNNAMED"],
            "minecraft_path": str(Path(os.getenv('APPDATA')) / ".minecraft"),
            
            "language": "en",
            "photo_perfil": "icon.png",
            "discord_presence": True,
            "wallpaper_launcher": "bg.png",
            "primary_color_schema": "#ff8f00",
            "light_color_schema": "#f1b362",
            "dark_color_schema": "#c57813",
            "opacity": 5
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