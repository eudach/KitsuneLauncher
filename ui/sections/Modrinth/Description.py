import flet as ft 
from core.modrinthApi import ModrinthVersionInfo
from ui.sections.Modrinth.Utils import SIZES, build_image, build_text
from ui.components.button import (
    ButtonOpenBrowser,
    ButtonNavigationDescription
)
class Description:
    def __init__(self, page, on_click_function):
        self.on_click_function = on_click_function
        self.page = page
        self.buttons_next_back = ButtonNavigationDescription(page)
    
    async def open_img_full_screen(self, e):
        page:ft.Page = self.page
        
        page.open(
            ft.AlertDialog(
                title=e.control.data[0],
                content=ft.Image(
                    filter_quality=ft.FilterQuality.HIGH,
                    expand=True,
                    src=e.control.data[1],
                    width=page.window.width,
                    height=page.window.height,
                    fit=ft.ImageFit.COVER,
                    border_radius=ft.border_radius.all(10),
                ),
                open=True,
                bgcolor=ft.Colors.BLACK38,
            )
        )
    
    async def open_mod_in_browser(self, e):
        self.page.launch_url(f"https://modrinth.com/mod/{e.control.data}")
    
    def build(self, datos:ModrinthVersionInfo, back_mod, next_mod, search_modrinth, get_description_installed=None):
        self.get_description_installed = get_description_installed
        self.search_modrinth = search_modrinth
        self.page.content_menu.content.content.controls = self.__build_mod_description(
            datos=datos, back_mod=back_mod, next_mod=next_mod
        )
        
        self.page.content_menu.content.update()
    
    def __build_mod_description(self, datos:ModrinthVersionInfo, back_mod, next_mod):
        
        page:ft.Page = self.page
        next_func = self.on_click_function
        back_func = self.on_click_function
        if page.temp_config_modrinth["current_section_modrinth"] == "mod_description_installed":
            next_func = lambda e: page.run_task(self.get_description_installed, next_mod)
            back_func = lambda e: page.run_task(self.get_description_installed, back_mod)

        page.views[0].floating_action_button = ft.Row(
            
            controls=[
                ft.Row(expand=True),
                self.buttons_next_back.get_before(
                    on_click=back_func,
                    have_before=back_mod == 0,
                    slug_before_mod=back_mod
                ),
                self.buttons_next_back.get_home(
                    function_search_mod=lambda e: page.run_task(self.search_modrinth, "description")
                ),
                self.buttons_next_back.get_next(
                    on_click=next_func,
                    have_next=next_mod == 0,
                    slug_next_mod=next_mod
                ),
                ft.Row(expand=True),
                ft.Container(
                    content=ButtonOpenBrowser(page, self.open_mod_in_browser, data=datos.slug).get(),
                    margin=ft.Margin(0, 0, 20, 0 )
                )
            ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER
            
        )
        
        return [
            ft.Container(
                border_radius=5,
                padding=5,
                blur=100,
                col=4,
                expand=True,
                content=ft.Column(
                    scroll=ft.ScrollMode.HIDDEN,
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[
                        build_image(
                            src=datos.icon_url if datos.icon_url is not None else 'iconos\\no_found_image.png',
                            w=128, h=128
                        ),
                        build_text(
                            value=datos.title,
                            size=SIZES["title"](page.window.width),
                            page=page, bold=True,
                            expand=True
                        ),
                        build_text(
                            value=datos.description,
                            size=SIZES["subtitle"](page.window.width),
                            page=page
                        ),
                        ft.Row(
                            controls=[
                                build_text(
                                    value=page.t("categories"),
                                    size=SIZES["category"](page.window.width),
                                    page=page, expand=False
                                )
                            ]
                            + [
                                ft.Container(
                                    content=build_text(
                                        value=cat,
                                        size=SIZES["chip"](page.window.width),
                                        page=page, 
                                        expand=False
                                    ),
                                    bgcolor=ft.Colors.BLACK12,
                                    padding=5,
                                    border_radius=5,
                                )
                                for cat in datos.categories
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Container(
                            padding=10,
                            content=ft.Column(
                                controls=[
                                    build_text(
                                        value=page.t("imgs"),
                                        size=SIZES["category"](page.window.width),
                                        page=page
                                    ),
                                    ft.Row(
                                        expand=1,
                                        wrap=True,
                                        scroll=ft.ScrollMode.ADAPTIVE,
                                        controls=[
                                            build_image(
                                                e["url"],
                                                128,
                                                128,
                                                on_click=self.open_img_full_screen,
                                                data=[e["title"], e["url"]],
                                                bgcolor=page.global_vars["primary_color"],
                                            )
                                            for e in datos.gallery
                                        ],
                                    ),
                                ]
                            ),
                        )
                        
                    ]
                ),
            ),
            ft.Container(
                border_radius=5,
                padding=5,
                blur=100,
                col=8,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Markdown(
                            value=datos.body,
                            
                        )
                    ]
                )
            ),
        ]
    
    def update(self, mod:ModrinthVersionInfo, next_mod, back_mod):
        page = self.page
        next_func = self.on_click_function
        back_func = self.on_click_function
        if page.temp_config_modrinth["current_section_modrinth"] == "mod_description_installed":
            next_func = lambda e: page.run_task(self.get_description_installed, next_mod)
            back_func = lambda e: page.run_task(self.get_description_installed, back_mod)
            
        page.views[0].floating_action_button = ft.Row(
            
            controls=[
                ft.Row(expand=True),
                self.buttons_next_back.get_before(
                    on_click=back_func,
                    have_before=back_mod == 0,
                    slug_before_mod=back_mod
                ),
                self.buttons_next_back.get_home(
                    function_search_mod=lambda e: page.run_task(self.search_modrinth, "description")
                ),
                self.buttons_next_back.get_next(
                    on_click=next_func,
                    have_next=next_mod == 0,
                    slug_next_mod=next_mod
                ),
                ft.Row(expand=True),
                ft.Container(
                    content=ButtonOpenBrowser(page, self.open_mod_in_browser, data=mod.slug).get(),
                    margin=ft.Margin(0, 0, 20, 0 )
                )
            ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER
            
        )
        
        self.page.content_menu.content.content.controls[0].content.controls[0].content.src = mod.icon_url if mod.icon_url is not None else 'iconos\\no_found_image.png'
        self.page.content_menu.content.content.controls[0].content.controls[1].value = mod.title
        self.page.content_menu.content.content.controls[0].content.controls[2].value = mod.description
        self.page.content_menu.content.content.controls[0].content.controls[3].controls = [self.page.content_menu.content.content.controls[0].content.controls[3].controls[0]]+ [
            ft.Container(
                content=build_text(e, SIZES["chip"](page.window.width), page, expand=False),
                bgcolor=ft.Colors.BLACK12,
                padding=5,
                border_radius=5,
            )
            for e in mod.categories
        ]
        self.page.content_menu.content.content.controls[0].content.controls[4].content.controls[1].controls = [
            build_image(
                src=image["url"],
                w=128,
                h=128,
                on_click=self.open_img_full_screen,
                data=[image["title"], image["url"]],
                bgcolor=page.global_vars["primary_color"],
            )
            for image in mod.gallery
        ]
        self.page.content_menu.content.content.controls[1].content.controls[0].value = mod.body
        
        self.page.content_menu.content.content.update()