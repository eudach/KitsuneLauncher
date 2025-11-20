
import pystray
from PIL import Image
import base64, io, os
import flet as ft


class StraySystem:
    def __init__(self, page: ft.Page):
        self.page: ft.Page = page
        self.page.logger.debug("Inicio de StraySystem")
        self.icon_img = Image.open(page.icon_path)

        self.tray_icon: pystray.Icon | None = None # type: ignore
        
        
    def _build_menu(self):
        """Construye el menú dinámicamente según traducciones."""
        return pystray.Menu(
            pystray.MenuItem(f'{self.page.t("open_app")} launcher', self.default_item_clicked, default=True),
            pystray.MenuItem(f'{self.page.t("exit_app")} launcher', self.exit_app)
        )
        
    def _create_icon(self):
        menu = self._build_menu()
        return pystray.Icon(
            name=f"StraySys-{self.page.title}",
            title=self.page.title,
            icon=self.icon_img,
            menu=menu
        )
    
    def update(self):
        menu = self._build_menu()
        self.tray_icon.menu = menu
        self.tray_icon.update_menu()

    def start(self):
        # Si ya había uno corriendo, lo paramos primero
        if self.tray_icon:
            try:
                self.tray_icon.stop()
            except Exception:
                pass

        self.tray_icon:pystray.Icon = self._create_icon()  # type: ignore
        self.tray_icon.run_detached()
        self.page.logger.debug("System Tray iniciado")

    def stop(self):
        if self.tray_icon:
            self.tray_icon.stop()
            self.tray_icon = None
            self.page.logger.debug("System Tray detenido")
        
    def exit_app(self, icon, item):
        self.page.win._shutdown()

    def default_item_clicked(self, icon, item):
        if self.page.window.visible:
            self.page.window.to_front()
        else:
            self.page.window.visible = True
            self.page.window.skip_task_bar = False
            self.page.update()
