import asyncio
from pathlib import WindowsPath
import flet as ft

from ui.components.button import (
    ButtonNavigationSearch
)

from ui.components.input import InputModModrinth
from ui.components.dropdown import DropdownLimitSearch, DropdownLoaders
from ui.components.iconbutton import IconButtonFilterSearch
from ui.components.navigators import NavigatorRailModrinthProjects


from ui.components.floatingbuttons import SearchButtonsNavigation
from core.modrinthApi import ModrinthAPI

from ui.sections.Modrinth.Description import Description
from ui.sections.Modrinth.Search import Search
from ui.sections.Modrinth.Utils import show_error_toast


class Modrinth:
    def __init__(self, page):
        self.page = page
        self.api: ModrinthAPI = page.api

    async def go_mod_description(self, e):
        page:ft.Page = self.page
        slug = e.control.data
        datos = await self.api.get_project_details(slug=slug)
        
        cache = self.page.temp_config_modrinth.get("list_mods_cache", [])
        mods_index = self.page.temp_config_modrinth.get("mods_index", {})

        # lookup O(1), con fallback si no existe
        back_mod, next_mod = self.get_neighbors(cache, mods_index, datos.slug)
        
        if self.has_description_loaded == False:
            self.description_manager.build(datos=datos, back_mod=back_mod, next_mod=next_mod, search_modrinth=self.search_modrinth)
        else:
            self.description_manager.update(mod=datos, back_mod=back_mod, next_mod=next_mod)
        
        page.temp_config_modrinth["current_section_modrinth"] = "mod_description"
        
        self.has_description_loaded = True
        page.update()
        
    async def get_description_installed(self, file: ft.ControlEvent | WindowsPath):
        file_path = None
        if isinstance(file, ft.ControlEvent):
            file_path = file.control.data
        elif isinstance(file, WindowsPath):
            file_path = file
        
        self.page.overlay[-1].open = False
        project_type = self.page.global_vars["project_type"]
        details = await self.api.search_project(function_on_progress=None, file_path=file_path, algorithm="sha1", project_type=project_type)
        if details is None:
            return show_error_toast(page=self.page, value=f"No se pudo encontrar el {self.page.global_vars["project_type"]}")

        cache = self.page.temp_config_modrinth.get("list_mods_cache_installed", [])
        mods_index = self.page.temp_config_modrinth.get("mods_index_installed", {})
        back_mod, next_mod = self.get_neighbors(cache, mods_index, file_path)

        self.page.temp_config_modrinth["current_section_modrinth"] = "mod_description_installed"
        
        if self.has_description_loaded == False:
            self.description_manager.build(datos=details, back_mod=back_mod, next_mod=next_mod, search_modrinth=self.search_modrinth, get_description_installed=self.get_description_installed)
        else:
            self.description_manager.update(mod=details, back_mod=back_mod, next_mod=next_mod)
        
        self.has_description_loaded = True
        self.page.update()
        
    async def search_modrinth(self, e=None):
        #print(self.page.temp_config_modrinth)
        page:ft.Page = self.page
        

        self.floating_search_local.build(
            button_back=self.button_back_list_mods,
            button_home=self.button_home_list_mods,
            button_next=self.button_next_list_mods,
        )
        
        page.temp_config_modrinth["current_section_modrinth"] = "search_mods"

        if e == "description":
            page.content_menu.content.content.controls = page.temp_config_modrinth["page_modslist_return"]
            self.has_description_loaded = False
            page.update()
            return # -> esto es cuando sale de la descripcion de un mod

        query = "" if e == "home" else self.input_mod_modrinth.value # -> e == home significa que es el de carga
        limit = page.temp_config_modrinth["limit_search_mods"] # -> limite de busquedas
        loader = self.dropdown_loaders_list.get().value # -> esto es solo para mods y modpack

        
        project_type = self.page.global_vars["project_type"]
        mods = await self.api.search_projects(
            project_type= project_type,
            query= query, limit= limit,
            offset= page.temp_config_modrinth["offset"], loader=loader
        )

        if page.temp_config_modrinth["offset"] == 0:
            self.list_mods_.build(mods[0])
        else:
            self.list_mods_.update(mods[0])
    
    def get_neighbors(self, cache, mods_index, key):
        current_mod = mods_index.get(key, 0)
        back_mod = cache[current_mod - 1] if current_mod - 1 >= 0 else 0
        next_mod = cache[current_mod + 1] if current_mod + 1 < len(cache) else 0
        return back_mod, next_mod

    async def change_page(self, direction: str, e):
        page = self.page
        limit = page.temp_config_modrinth["limit_search_mods"]
        offset = page.temp_config_modrinth["offset"]
        total = page.temp_config_modrinth["total_mods_result"]
    
        if direction == "back" and offset - limit >= 0:
            page.temp_config_modrinth["offset"] -= limit
        elif direction == "next" and offset + limit < total:
            page.temp_config_modrinth["offset"] += limit
        elif direction == "home":
            page.temp_config_modrinth["offset"] = 0
            self.input_mod_modrinth.value = ""
            self.input_mod_modrinth.update()

        page.run_task(self.search_modrinth, e)

    async def change_limit_research_mod(self, e):
        self.page.temp_config_modrinth["limit_search_mods"] = int(self.dropdown_limit_search.value)
        self.page.run_task(self.search_modrinth, "")

    async def change_loader_mod(self, e):
        self.page.temp_config_modrinth["limit_search_mods"] = int(self.dropdown_limit_search.value)
        self.page.run_task(self.search_modrinth, "")
        
    async def change_category(self, e:ft.ControlEvent):
        self.page.global_vars["project_type"] = self.navigator_category.destinations[self.navigator_category.selected_index].data
        
        self.dropdown_loaders_list.update(project_type=self.page.global_vars["project_type"])
        
        self.page.temp_config_modrinth["offset"] = 0
        try:
            await self.search_modrinth("")
        except:
            pass

    async def get_filters_search(self, e):
        self.alert_dialg  =ft.AlertDialog(
            icon=ft.Row(controls=[
                    ft.Row(expand=True),
                    ft.IconButton(icon=ft.Icons.CLOSE, icon_color=self.page.global_vars["primary_color"], on_click=self.page.close_alert)
                ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        self.dropdown_limit_search,
                        self.dropdown_loaders_list.get()
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                ),
                width=self.page.window.width/2.5,
                height=self.page.window.height/3,
                alignment=ft.alignment.center
            ),
            
            bgcolor=ft.Colors.BLACK87,
            shape=ft.BeveledRectangleBorder(3),
            barrier_color=ft.Colors.TRANSPARENT
        )
        self.page.open(
            self.alert_dialg
        )

    async def load(self):
        page = self.page
        self.has_description_loaded = False
        self.page.global_vars["project_type"] = "mod"
        self.floating_search_local = SearchButtonsNavigation(page=page, modrinth_instance=self)
        page.temp_config_modrinth["current_section_modrinth"] = "modrinth"
        page.content_menu.alignment = ft.alignment.center
        
        self.iconbutton_filter_projects = IconButtonFilterSearch(page, self.get_filters_search).get()
        self.dropdown_limit_search = DropdownLimitSearch(page, self.change_limit_research_mod).get()
        self.dropdown_loaders_list = DropdownLoaders(page, self.change_loader_mod)
        self.input_mod_modrinth = InputModModrinth(
            page=page,
            iconbutton_filter_mod=self.iconbutton_filter_projects,
            on_change=self.search_modrinth
        ).get()

        bttns_cls = ButtonNavigationSearch(page)
        self.button_back_list_mods = bttns_cls.get_back(on_click_back=lambda e: page.run_task(self.change_page, "back", e))
        self.button_home_list_mods = bttns_cls.get_home(on_click_home=lambda e: page.run_task(self.change_page, "home", e))
        self.button_next_list_mods = bttns_cls.get_next(on_click_next=lambda e: page.run_task(self.change_page, "next", e))
        
        

        self.list_mods_modrinth = ft.ListView(spacing=5, controls=[])
        self.list_mods_ = Search(page=page, list_mods_modrinth=self.list_mods_modrinth, on_click_go_description=self.go_mod_description)
        
        self.description_manager = Description(page=page, on_click_function=self.go_mod_description)
        self.content_results_modrinth = ft.Container(expand=10, content=self.list_mods_modrinth, padding=0, margin=0)
        
        self.navigator_category = NavigatorRailModrinthProjects(page, on_change=self.change_category).get()
        

        page.content_menu.content = ft.Container(
            expand=True,
            padding=0,
            margin=0,
            content=ft.ResponsiveRow(
                vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                expand=True,
                controls=[
                    ft.Container(
                        content=self.navigator_category ,
                        bgcolor=ft.Colors.WHITE10,
                        col=0.8,
                        border_radius=5
                    ),
                    ft.Container(
                        col=11.2,
                        content=
                            ft.Column(
                                controls=[
                                    ft.Container(
                                        bgcolor=ft.Colors.WHITE10,
                                        border_radius=5,
                                        padding=ft.Padding(0, 0, 5, 0),
                                        content=ft.Row(
                                            controls=[
                                                self.input_mod_modrinth,

                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            expand=True,
                                        ),
                                    ),
                                    self.content_results_modrinth,
                                ],
                            expand=True,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        alignment=ft.alignment.center
                    )
                ]
            ),
        )

        page.temp_config_modrinth["page_modslist_return"] = page.content_menu.content.content.controls
        await self.search_modrinth("home")
        await asyncio.sleep(0)
