import flet as ft
import asyncio
import platform
import subprocess
import socket
import urllib.request

from ui.components import toast
from ui.resources.Fonts import BaseFonts

class Internet:
    def __init__(self, page: ft.Page):
        self._page = page
        self._connected = True
        self._page.run_task(self._setup)

    @property
    def connected(self) -> bool:
        """Devuelve True si hay conexión a internet, False si no."""
        return self._connected

    async def _setup(self):
        """Hace la comprobación inicial y lanza el ciclo de verificación."""
        self._connected = await self._check_connection()
        self._page.logger.debug(f"🌐 Estado inicial: {'online ✅' if self._connected else 'offline ❌'}")
        await self._background_task()

    async def _check_connection(self) -> bool:
        """Verifica conexión de manera multiplataforma sin depender de ping.

        Estrategia:
        1) Intentar conexión TCP a DNS público (1.1.1.1:53)
        2) Fallback: solicitar URL ligera (HTTP 204) con timeout corto
        """

        def check():
            # 1) Probar socket a DNS (rápido, sin HTTP)
            try:
                with socket.create_connection(("1.1.1.1", 53), timeout=1.5):
                    return True
            except Exception:
                pass

            # 2) Fallback HTTP a una URL que responde 204 sin contenido
            try:
                req = urllib.request.Request(
                    "https://www.google.com/generate_204",
                    headers={"User-Agent": "KitsuneLauncher/1.0"},
                    method="GET",
                )
                with urllib.request.urlopen(req, timeout=2) as resp:
                    return 200 <= resp.status < 400
            except Exception:
                return False

        # Ejecutar sin bloquear la UI
        return await asyncio.to_thread(check)

    async def _background_task(self):
        """Tarea que se ejecuta durante toda la vida de la app."""
        while True:
            new_status = await self._check_connection()
            if new_status != self._connected:
                self._connected = new_status
                
                if self._connected is False:
                    # Confirmar una vez más rápidamente para evitar falsos negativos puntuales
                    if await self._check_connection() is False:
                        try:
                            self._page.toaster.show_toast(
                                toast= toast.Toast(
                                    content=ft.Text(
                                        value=self._page.t("internet_no_found"),
                                        expand=True,
                                        size=self._page.window.width / 80,
                                        max_lines=2,
                                        text_align=ft.TextAlign.LEFT,
                                        font_family=BaseFonts.texts,
                                    ),
                                    toast_type=toast.ToastType.ERROR,
                                ),
                                duration=3,
                            )
                        except Exception:
                            pass
                        self._page.logger.debug(f"🌐 Conexión: {'online ✅' if self._connected else 'offline ❌'}")
                        if hasattr(self._page, "modrinth_button") and self._page.modrinth_button is not None:
                            self._page.modrinth_button.disabled = True
                            self._page.modrinth_button.update()
                    else:
                        if hasattr(self._page, "modrinth_button") and self._page.modrinth_button is not None:
                            self._page.modrinth_button.disabled = False
                            self._page.modrinth_button.update()
                else:
                    if hasattr(self._page, "modrinth_button") and self._page.modrinth_button is not None:
                        self._page.modrinth_button.disabled = False
                        self._page.modrinth_button.update()
            
            await asyncio.sleep(3)
