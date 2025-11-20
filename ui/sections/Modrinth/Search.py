import flet as ft
from core.modrinthApi import ModrinthProject
from ui.sections.Modrinth.Utils import build_text

class Search:
    
    def __init__(self, page,list_mods_modrinth:ft.ListView, on_click_go_description):
        self.on_click_go_description = on_click_go_description
        self.page = page
        self.list_mods_modrinth = list_mods_modrinth
    
    def build(self,  mods_list:list[ModrinthProject]):
        self.list_mods_modrinth.controls = [
            self.__build_mod_item(mod)
            for mod in mods_list
        ]
        try:
            self.list_mods_modrinth.update()
        except:
            pass
        
    def __build_mod_item(self, mod:ModrinthProject):
        page = self.page
        return ft.Container(
            content=ft.Row(
                expand=True,
                controls=[
                    ft.Image(src=mod.icon, width=64, height=64),
                    ft.Column(
                        controls=[
                            build_text(mod.name, page.window.width / 80, page),
                            build_text(mod.description, page.window.width / 100, page),
                        ],
                        
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            ink=True,
            bgcolor=ft.Colors.WHITE10,
            border_radius=5,
            on_click=self.on_click_go_description,
            data=mod.slug,
        )
    
    def update(self, mods:list[ModrinthProject]):

        for container, mod in zip(self.list_mods_modrinth.controls, mods):
            container.data = mod.slug
            container.content.controls[0].src = mod.icon
            container.content.controls[1].controls[0].value = mod.name
            container.content.controls[1].controls[1].value = mod.description

        if len(self.list_mods_modrinth.controls) > len(mods):
            self.list_mods_modrinth.controls = self.list_mods_modrinth.controls[:len(mods)]

        try:
            self.list_mods_modrinth.scroll_to(offset=0, duration=100)
            self.list_mods_modrinth.update()
        except:
            pass
        