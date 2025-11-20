import flet as ft
import os

import logging
from core.utils import alerta
import psutil


class WindowsManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.logger = getattr(page, "logger", logging.getLogger(__name__))

    def maximize(self, e=None):
        """Alternar ventana maximizada"""
        self.page.window.maximized = not self.page.window.maximized
        self.page.update()

    def minimize(self, e=None):
        """Alternar ventana minimizada"""
        self.page.window.minimized = not self.page.window.minimized
        self.page.update()

    def close_windows(self, e=None):
        """
        Cerrar la ventana respetando configuración.
        Si app_background está activo, solo oculta la ventana.
        """
        if self.page.global_vars["installing_minecraft_version"]:
            self.page.open(alerta(titulo="Error", descripcion=self.page.t("error_installing")))
            return
        try:
            self.page.launcher.config.save()
        except Exception as ex:
            self.logger.error(f"Error guardando config: {ex}")

        if self.page.launcher.config.get("app_background"):
            self.page.window.skip_task_bar = True
            self.page.window.visible = False
            self.page.dragging_enabled = False
            self.page.update()
            return

        self._shutdown()
        
    def kill_process(self):
        # PID
        parent = psutil.Process(os.getpid())

        exclude_names = ["java.exe", "javaw.exe"]  # Minecraft java
        exclude_paths = []

        for child in parent.children(recursive=True):
            try:
                
                name = child.name().lower()
                exe_path = child.exe() if child.exe() else ""

                if name not in [n.lower() for n in exclude_names] and not any(p in exe_path for p in exclude_paths):
                    child.kill()
            except Exception:
                pass
            
        parent.kill()

    def _shutdown(self):
        """Cierra presencia, stray y termina el proceso"""
        # Intentar cerrar presencia si existe
        try:
            if hasattr(self.page, "presence"):
                self.page.presence.close()
        except Exception as ex:
            self.logger.warning(f"No se pudo cerrar presence: {ex}")

        # Intentar detener stray si existe
        try:
            if hasattr(self.page, "stray"):
                self.page.stray.stop()
        except Exception as ex:
            self.logger.warning(f"No se pudo detener stray: {ex}")

        # Terminar proceso
        self.kill_process()
