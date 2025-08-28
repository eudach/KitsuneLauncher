import flet as ft

from ui.components.button import ButtonCloseSession
from core.utils import alerta

class Perfil:
    def __init__(self, page:ft.Page):
        self.page = page
        
    async def close_session(self, e):
        page = self.page
        page.open(
            alerta(
                titulo= page.t("session_closed"),
                descripcion= f"{page.t('session_closed_description')} {page.launcher.config.get("username")}",
                success=True
            )
        )
        
        page.launcher.config.set("username", None)
        page.launcher.config.save()
        page.go("/login")
        
    async def load(self):
        page = self.page
        page.current_section = 'perfil'
        page.content_menu.alignment= ft.alignment.center
        page.content_menu.content= ft.Column(
            controls=[
                ft.Container(
                    content=ft.Image(
                        filter_quality=ft.FilterQuality.MEDIUM,
                        anti_alias=True,
                        fit=ft.ImageFit.CONTAIN,
                        src=page.launcher.config.get("photo_perfil"),
                        border_radius=(page.ancho*0.35)/2,
                        width=page.ancho*0.25, height=page.alto*0.25
                    ),
                    padding=0,
                    alignment=ft.alignment.center,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    width=page.ancho*0.35, height=page.alto*0.35,
                    bgcolor=ft.Colors.TRANSPARENT,
                    border=ft.border.all(2, ft.Colors.TRANSPARENT),
                    shape=ft.BoxShape.CIRCLE,
                    
                )
                ,
                ft.Container(
                    content=ft.Text(
                        selectable=True,
                        value=page.launcher.config.get("username") ,
                        font_family="liberation", 
                        size=page.ancho/30,
                    ), 
                    bgcolor=ft.Colors.BLACK12,
                    border_radius=10,
                    ink=True, 
                    padding=5
                ),
                ButtonCloseSession(page, self.close_session).get() 
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )