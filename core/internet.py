import flet as ft
import asyncio
import platform
import subprocess

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
        """Verifica conexión mediante ping (sin dependencias externas)."""
        def ping():
            host = "1.1.1.1"  # Cloudflare DNS (siempre disponible)
            param = "-n" if platform.system().lower() == "windows" else "-c"
            cmd = ["ping", param, "1", host]
            try:
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

                result = subprocess.run(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    startupinfo=si,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    shell=False
                )
                
                return result == 0
            except Exception:
                return False

        # ejecuta el ping sin bloquear la UI
        return await asyncio.to_thread(ping)

    async def _background_task(self):
        """Tarea que se ejecuta durante toda la vida de la app."""
        while True:
            new_status = await self._check_connection()
            if new_status != self._connected:
                self._connected = new_status
                
                if self._connected == False:
                    if await self._check_connection() == False:
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
                        self._page.logger.debug(f"🌐 Conexión: {'online ✅' if self._connected else 'offline ❌'}")
                        self._page.modrinth_button.disabled = True
                        self._page.modrinth_button.update()
                    else:
                        self._page.modrinth_button.disabled = False
                        self._page.modrinth_button.update()
                else:
                    self._page.modrinth_button.disabled = False
                    self._page.modrinth_button.update()
            
            await asyncio.sleep(3)
