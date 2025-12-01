import re
import flet as ft
import os

from ui.components.button import (
    ButtonListSearchModrinth,
    ButtonOpenFolder,
    ButtonRefreshModsLocal,
    ButtonNextPagMod,
    ButtonBackPagMod,
    ButtonHomePagMod,
    ButtonOpenBrowser)
from ui.components.container import ContainerModLocal
from ui.components.input import InputModModrinth
from ui.components.dropdown import DropdownLimitSearch, DropdownLoaders
from ui.components.iconbutton import IconButtonSearchMod

from core.modrinthApi import ModrinthAPI

from webbrowser import open_new

class Modrinth:
    def __init__(self, page):
        self.page = page
    
    async def open_img_full_screen(self, e):
        page = self.page
        page.open(
            ft.AlertDialog(
                title=e.control.data[0],
                content=ft.Image(
                    anti_alias=True,
                    filter_quality=ft.FilterQuality.HIGH,
                    expand=True,
                    src=e.control.data[1],
                    width=page.ancho,
                    height=page.alto,
                    fit=ft.ImageFit.COVER,
                    border_radius=ft.border_radius.all(10)
                ),
                open=True,
                bgcolor=ft.Colors.TRANSPARENT
            )
        )
        
    async def open_mod_in_browser(self, e):
        open_new(f"https://modrinth.com/mod/{e.control.data}")
    
    async def go_mod_description(self, e):
        page = self.page
        datos = None
        async with ModrinthAPI(page) as modrinth:
            datos = await modrinth.get_mod_description(e.control.data)
            
        current_mod = page.temp_config_modrinth['list_mods_cache'].index(e.control.data)
        have_back_mod = True
        have_next_mod = True
        back_mod = 0
        next_mod = 0
        if current_mod-1 >= 0:
            have_back_mod = False
            back_mod = page.temp_config_modrinth['list_mods_cache'][current_mod-1]
        
        if current_mod+1 <= len(page.temp_config_modrinth['list_mods_cache'])-1:
            have_next_mod = False
            next_mod = page.temp_config_modrinth['list_mods_cache'][current_mod+1]
        
        self.content_modrinth.padding = 5
        self.content_modrinth.content.controls = [
            ft.Container(
                margin=0,
                bgcolor=ft.Colors.TRANSPARENT,
                border_radius=10,
                content=ft.Row(
                    controls=[
                        ButtonBackPagMod(page, have_back_mod, back_mod, self.go_mod_description).get(),
                        ButtonHomePagMod(page, self.search_mods).get(),
                        ButtonNextPagMod(page, have_next_mod, next_mod, self.go_mod_description).get(),
                    ], expand=True, alignment=ft.MainAxisAlignment.CENTER
                )
            ),
            ft.Container(
                expand=True,
                content=
                ft.Column(
                    controls=[
                        ft.Row(controls=
                            [
                                ft.Container(content=
                                    ft.Image(
                                        src=datos['icon_url'],
                                        width=128, height=128,
                                        fit=ft.ImageFit.COVER
                                    ),
                                    border_radius=10,
                                    width=128, height=128,
                                    padding=1,
                                    border=ft.border.all(1, page.color_init)
                                )
                            ]
                        ),
                        ft.Text(
                            value=datos["title"],
                            font_family="liberation",
                            size=page.ancho/40
                            ),
                        ft.Text(
                            value=datos["description"],
                            font_family="liberation",
                            size=page.ancho/80),
                        ft.Row(
                            controls=[
                                ft.Text(
                                    value=page.t("categories"),
                                    font_family="liberation",
                                    size=page.ancho/90
                                )
                            ]+[
                            ft.Container(
                                content=ft.Text(
                                    value=e,
                                    font_family="liberation",
                                    size=page.ancho/110
                                ),
                                bgcolor=ft.Colors.BLACK12,
                                padding=5,
                                border_radius=5
                            )
                            for e in datos['categories']
                            ], alignment=ft.MainAxisAlignment.START
                        ),
                        ft.Container(
                            padding=10,
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        value=page.t("imgs"),
                                        font_family="liberation",
                                        size=page.ancho/90
                                    ),
                                    ft.Container(
                                        padding=5,
                                        content=
                                        ft.Row(
                                            expand=1,
                                            wrap=True,
                                            scroll=ft.ScrollMode.ADAPTIVE,
                                            controls=[
                                                ft.Container(
                                                    padding=1,
                                                    bgcolor=page.color_init,
                                                    border_radius=10,
                                                    content=ft.Image(
                                                        expand=True,
                                                        src=e['url'],
                                                        width=128,
                                                        height=128,
                                                        fit=ft.ImageFit.COVER,
                                                        repeat=ft.ImageRepeat.NO_REPEAT,
                                                        border_radius=ft.border_radius.all(10)
                                                    ),
                                                    ink=True, on_click=self.open_img_full_screen,
                                                    data=[e['title'], e['url']]
                                                )
                                            for e in datos['gallery']
                                            ]+[
                                                ft.Container(
                                                    padding=1,
                                                    bgcolor=page.color_init,
                                                    border_radius=10,
                                                    content=ft.Image(
                                                        expand=True,
                                                        src=e,
                                                        width=128,
                                                        height=128,
                                                        fit=ft.ImageFit.COVER,
                                                        repeat=ft.ImageRepeat.NO_REPEAT,
                                                        border_radius=ft.border_radius.all(10)
                                                    ),
                                                    ink=True, on_click=self.open_img_full_screen,
                                                    data=["", e]
                                                )
                                                for e in datos['body_images']
                                                ], vertical_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER
                                        )
                                    )
                                ]
                            )
                        )
                    ], scroll=ft.ScrollMode.ALWAYS, expand=True
                )
            ),
            ft.Container(
                margin=0,
                padding=0,
                border_radius=10,
                content=ButtonOpenBrowser(page, self.open_mod_in_browser, data=e.control.data).get()
            )
        ]
        self.content_modrinth.bgcolor = ft.Colors.WHITE10
        self.page.temp_config_modrinth['current_section_modrinth'] = 'mod_description'
        self.content_modrinth.update()
        
    async def search_mods(self, e, no_update:bool=True):
        page = self.page
        self.page.temp_config_modrinth['current_section_modrinth'] = 'search_mods'
        # Cambiar a modo de descripción
        if isinstance(e, ft.ControlEvent) and e.control.data == 'description':
            self.content_modrinth.content.controls = page.temp_config_modrinth['page_modslist_return']
            self.content_modrinth.padding = 0
            self.content_modrinth.bgcolor = None
            self.content_modrinth.update()
            return

        # Realiza la búsqueda
        query = "" if e == "home" else self.input_mod_modrinth.value
        
        limite = page.temp_config_modrinth['limit_search_mods']
        mods = []
        async with ModrinthAPI(page) as modrinth:
            mods = await modrinth.search_mod_modrinth(
                query=query,
                limit=limite,
                offset=page.temp_config_modrinth['offset'],
                loader=self.dropdown_loaders_list.value
            )

        # Crear los resultados
        self.content_results_modrinth.content.controls = [
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Image(src=mod["icon"], width=64, height=64),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    value=mod["name"],
                                    size=page.ancho / 80,
                                    text_align=ft.TextAlign.LEFT,
                                    font_family="liberation",
                                    expand=True,
                                ),
                                ft.Text(
                                    value=mod["description"],
                                    size=page.ancho / 100,
                                    text_align=ft.TextAlign.LEFT,
                                    font_family="liberation",
                                    expand=True,
                                ),
                            ],
                            expand=True,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.START
                ),
                ink=True,
                bgcolor=ft.Colors.WHITE10,
                border_radius=5,
                on_click=self.go_mod_description,
                data=mod["slug"]
            )
            for mod in mods
        ]
        if no_update:
            self.content_results_modrinth.update()
        else:
            pass
    
    async def back_page_mod(self, e):
        page = self.page
        self.button_next_list_mods.disabled = False
        self.button_next_list_mods.update()
        if page.temp_config_modrinth['offset'] - page.temp_config_modrinth['limit_search_mods'] < 0:
            self.button_back_list_mods.disabled = True
            self.button_back_list_mods.update()
            return
        page.temp_config_modrinth['offset'] -= page.temp_config_modrinth['limit_search_mods']
        page.run_task(self.search_mods, e)
        
    async def home_page_mod(self, e):
        page = self.page
        page.temp_config_modrinth['offset'] = 0
        self.input_mod_modrinth.value = ""
        self.input_mod_modrinth.update()
        page.run_task(self.search_mods, "home")
    
    async def next_page_mod(self, e):
        page = self.page
        self.button_back_list_mods.disabled = False
        self.button_back_list_mods.update()
        if page.temp_config_modrinth['offset'] + page.temp_config_modrinth['limit_search_mods'] >= page.temp_config_modrinth['total_mods_result']:
            self.button_next_list_mods.disabled = True
            self.button_next_list_mods.update()
            return
        page.temp_config_modrinth['offset'] += page.temp_config_modrinth['limit_search_mods']
        page.run_task(self.search_mods, e)
        
    async def change_limit_research_mod(self, e):
        self.page.temp_config_modrinth['limit_search_mods'] = int(self.dropdown_limit_search.value)
        self.page.run_task(self.search_mods, "")
        
    async def change_loader_mod(self, e):
        self.page.temp_config_modrinth['limit_search_mods'] = int(self.dropdown_limit_search.value)
        self.page.run_task(self.search_mods, "")
            
    async def search_mod_installed_modrinth(self, e):
        if self.page.temp_config_modrinth['current_section_modrinth'] != 'search_mods':
            return
        name_cleaned = re.match(r"^(.+?)(?=-v?\d)", e.control.data, re.IGNORECASE).group(1)
        self.input_mod_modrinth.value = name_cleaned
        self.input_mod_modrinth.update()
        await self.search_mods("")
        
    async def refresh_list_mods_local(self, e):
        actual_list_mods_local = self.page.launcher.get_list_mods()
        if self.promt_list_mods == actual_list_mods_local:
            return
        
        self.list_installed_mods.controls = [
                ContainerModLocal(self.page, mod, self.search_mod_installed_modrinth, self.remove_mod).get()
            for mod in actual_list_mods_local]
        
        self.total_local_mods.value = f"{self.page.t('total_mods_loaded')}: {len(actual_list_mods_local)}"
        self.total_local_mods.update()
        self.list_installed_mods.update()
        
    
        
    async def load(self):
        page = self.page
        page.temp_config_modrinth['current_section_modrinth'] = 'modrinth'
        page.content_menu.alignment = ft.alignment.center
        
        self.promt_list_mods = page.launcher.get_list_mods()
        self.list_installed_mods = ft.ListView(
            controls=[
                ContainerModLocal(page, mod, self.search_mod_installed_modrinth).get()
            
            for mod in self.promt_list_mods],
            spacing=5,
            padding=ft.Padding(5, 5, 5, 5)
        )
        
        
        self.iconbutton_search_mod = IconButtonSearchMod(page, self.search_mods)
        self.input_mod_modrinth = InputModModrinth(page, self.iconbutton_search_mod, self.search_mods).get()
        self.dropdown_limit_search = DropdownLimitSearch(page, self.change_limit_research_mod).get()
        self.dropdown_loaders_list = DropdownLoaders(page, self.change_loader_mod).get()
        
        bttns_cls = ButtonListSearchModrinth(page)
        self.button_back_list_mods = await bttns_cls.get_back(self.back_page_mod)
        self.button_home_list_mods = await bttns_cls.get_home(self.home_page_mod)
        self.button_next_list_mods = await bttns_cls.get_next(self.next_page_mod)
        self.total_local_mods = ft.Text(value=f"{page.t('total_mods_loaded')}: {len(self.promt_list_mods)}")
        self.list_mods_modrinth = ft.ListView(
            spacing=5,
            padding=ft.Padding(5, 0, 10, 0),
            controls=[],
        )
        
        self.content_results_modrinth = ft.Container(
            expand=10,
            content=self.list_mods_modrinth,
            padding=0,
            margin=0
        )
        
        self.content_modrinth = ft.Container(
            padding=0,
            margin=0,
            col=8,
            border_radius=5,
            content=ft.Column(
                controls=[
                    ft.Container(
                        bgcolor=ft.Colors.WHITE10,
                        border_radius=5,
                        padding=ft.Padding(0, 0, 5, 0),
                        content=ft.Row(
                            controls=[
                                self.input_mod_modrinth,
                                self.dropdown_limit_search,
                                self.dropdown_loaders_list,
                                self.button_back_list_mods,
                                self.button_home_list_mods,
                                self.button_next_list_mods
                            ],
                            alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER, expand=True
                        )
                    ),
                    self.content_results_modrinth,
                ],
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                alignment=ft.MainAxisAlignment.START,
            )
        )
        page.content_menu.content = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    col=4,
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                expand=9,
                                content=self.list_installed_mods
                            ),
                            ft.Container(
                                expand=1,
                                content=ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=self.total_local_mods,
                                            bgcolor=ft.Colors.WHITE10,
                                            padding=5,
                                            border_radius=10
                                        ),
                                        ButtonRefreshModsLocal(page, self.refresh_list_mods_local).get(),
                                        ButtonOpenFolder(page).get()
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                                )
                            ) 
                        ],
                        expand=True
                    )
                ),
                self.content_modrinth
            ], expand=True
        )
        page.temp_config_modrinth['page_modslist_return'] = self.content_modrinth.content.controls
        await self.search_mods("home", False)