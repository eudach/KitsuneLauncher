import os
import threading
import flet as ft
from flet_route import Params,Basket
from Utils import alerta, alerta_good

async def InstallationView(page:ft.Page, params:Params, basket:Basket):
    
    
    
    return ft.View(
        "/installation",
        controls=[
            ft.Container(expand=True, bgcolor=ft.Colors.BLACK38, border_radius=5)
            
        ],
        decoration=ft.BoxDecoration(
            image=ft.DecorationImage( 
                src= page.wallpaper_launcher, 
                fit=ft.ImageFit.COVER,
                opacity= 0.8
                ),
            
            ),
        bgcolor=ft.Colors.TRANSPARENT,
    )