
import flet as ft
from flet_route import Params, Basket
from Tools import alerta, get_offline_uuid, TYPES_COLORS
import re

async def LoginView(page:ft.Page, params:Params, basket:Basket):
    
    async def goto_MainView(e):
        nombre = name_user.value
        #page.launcher:KitsuneLauncher # type: ignore
        
        if page.launcher.config.get("premium_mode"):
            page.open(
                alerta(
                    titulo= "Error",
                    descripcion= "En desarrollo"
                    )
                )
            return
        
        if not re.fullmatch(r'[a-zA-Z0-9_]{3,16}', nombre):
            page.open(
                alerta(
                    titulo= page.t("error_name_dialg_title"),
                    descripcion= page.t("error_name_dialg_description")
                    )
                )
            return
        
        uuidd = get_offline_uuid(nombre)
        page.launcher.config.set("uuid", uuidd)

        basket.nombre = nombre
        page.launcher.set_username(nombre)
        page.launcher.config.save()
        page.go("/")
    
    
    async def change_perfil(e):
        e.control.bgcolor=ft.Colors.WHITE10 if e.control.bgcolor==ft.Colors.TRANSPARENT else ft.Colors.TRANSPARENT
        e.control.border = ft.border.all(2, ft.Colors.TRANSPARENT) if e.control.border == ft.border.all(2, ft.Colors.BLACK38) else ft.border.all(2, ft.Colors.BLACK38)
        
        e.control.update()
        
    async def save_photo_perfil(e:ft.FilePickerResultEvent):
        if e.files is None:
            return 0
        
        page.launcher.config.set("photo_perfil", e.files[0].path)
        
        img_control.src = e.files[0].path
        
        img_control.update()
        
    picker = ft.FilePicker(on_result=save_photo_perfil)
    picker.allowed_extensions = [".png", ".jpg", "jpeg"]
    page.overlay.append(picker)
    
        
    async def change_foto(e):
        picker.pick_files(allow_multiple=False)
        page.update()
        
    async def enable_premium(e):
        pass  
        
    img_control = ft.Image(
        filter_quality=ft.FilterQuality.MEDIUM,
        anti_alias=True,
        fit=ft.ImageFit.CONTAIN,
        src=page.launcher.config.get("photo_perfil"),
        border_radius=(page.ancho*0.35)/2,
        width=page.ancho*0.35, height=page.alto*0.35
    )

    name_user = ft.TextField(
        label=page.t("name_user"),
        width=page.ancho*0.30,
        border=ft.InputBorder.UNDERLINE,
        filled=True,
        hint_text=page.t("name_user_hint"),
        fill_color=ft.Colors.WHITE10,
        border_radius=3,
        focused_border_color=ft.Colors.WHITE,
        label_style=ft.TextStyle(color=ft.Colors.WHITE)
    )
    
    pass_user = ft.TextField(
        password=True,
        can_reveal_password=True,
        label=page.t("pass_user"),
        width=page.ancho*0.30,
        border=ft.InputBorder.UNDERLINE,
        filled=True,
        hint_text=page.t("pass_user_hint"),
        fill_color=ft.Colors.WHITE10,
        border_radius=3,
        focused_border_color=ft.Colors.WHITE,
        label_style=ft.TextStyle(color=ft.Colors.WHITE),
        visible=page.launcher.config.get("premium_mode"),
    )
    
    return ft.View(
        "/login",
        controls=[
            
            ft.Container(
                expand=True,
                border_radius=5,
                bgcolor=TYPES_COLORS[page.launcher.config.get("opacity")][2],
                border=ft.border.all(1, page.launcher.config.get("primary_color_schema")),
                alignment=ft.alignment.center,
                content=
                    ft.Column(
                        controls=[
                            ft.Container(
                                content=img_control,
                                padding=0,
                                alignment=ft.alignment.center,
                                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                width=page.ancho*0.35, height=page.alto*0.35,
                                bgcolor=ft.Colors.TRANSPARENT,
                                border=ft.border.all(2, ft.Colors.TRANSPARENT),
                                shape=ft.BoxShape.CIRCLE,
                                on_hover=change_perfil,
                                on_click=change_foto,
                                tooltip=page.t("Resolution_perfil"),
                                
                            ),
                            name_user,
                            pass_user,
                            ft.OutlinedButton(
                                
                                content=ft.Text(value=page.t("button_login"), text_align=ft.TextAlign.CENTER, font_family="Katana", size=page.ancho/40),
                                width=page.ancho*0.20,
                                height=page.alto*0.08,
                                style=ft.ButtonStyle(
                                    overlay_color=ft.Colors.WHITE10,
                                    color={
                                        ft.ControlState.DEFAULT: ft.Colors.WHITE,
                                        ft.ControlState.HOVERED: page.launcher.config.get("primary_color_schema"),
                                        ft.ControlState.FOCUSED: page.launcher.config.get("light_color_schema")
                                    },
                                    shape={
                                        ft.ControlState.HOVERED: ft.StadiumBorder(),
                                        #ft.ControlState.FOCUSED: ft.Colors.BLUE,
                                        ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(10)
                                    },
                                    bgcolor=ft.Colors.TRANSPARENT
                                    
                                    ),
                                on_click=goto_MainView)
                        ], 
                        alignment=ft.MainAxisAlignment.CENTER, 
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
            )
        ],
        decoration=ft.BoxDecoration(
            image=ft.DecorationImage( 
                src=page.launcher.config.get("wallpaper_launcher"), 
                fit=ft.ImageFit.FILL,
                opacity= 0.8
                ),
            
            ),
        bgcolor=ft.Colors.TRANSPARENT,
        floating_action_button=ft.FloatingActionButton(
            text="Normal Mode" if page.launcher.config.get("premium_mode") else "Premium Mode",
            bgcolor=ft.Colors.BLACK12, 
            width=130, scale=0.7, 
            on_click=enable_premium,
            disabled=True,
        ),
        
        floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT
    )