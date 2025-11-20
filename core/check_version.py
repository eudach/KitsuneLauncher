import requests
from packaging import version
from pathlib import Path
import os

class CheckVersion:
    VERSION_FILE = Path(f"{os.path.dirname(__file__)}\\VERSION.txt")
    REPO = "eudach/KitsuneLauncher"

    def __init__(self, page):
        self.page = page
        self._local_version = None
        self._latest_version = None
        self.page.logger.debug(f"Inicio de chequeo de versiones...")

    def load_current_version(self):
        if self._local_version is None:
            try:
                with self.VERSION_FILE.open("r", encoding="utf-8") as f:
                    v = f.read().strip()
                    self._local_version = v
            except FileNotFoundError:
                self._local_version = "0.0.0"
        self.page.logger.debug(f"Versión actual: {self._local_version}")
        return self._local_version

    def get_latest_version(self):
        if self._latest_version is None:
            try:
                url = f"https://api.github.com/repos/{self.REPO}/tags"
                res = requests.get(url, timeout=5)
                res.raise_for_status()
                tags = res.json()
                if tags:
                    self._latest_version = tags[0]["name"]
                else:
                    self._latest_version = "0.0.0"
            except requests.RequestException:
                self._latest_version = "0.0.0"
                
        self.page.logger.debug(f"Versión encontrada en el repositorio: {self._latest_version}")
        return self._latest_version

    def have_new_version(self):
        return version.parse(self.load_current_version()) < version.parse(self.get_latest_version())

    def latest_version_link(self):
        return f"https://github.com/{self.REPO}/releases/latest"
