import flet as ft
from ui.resources.Fonts import BaseFonts

class NavigatorRailModrinthProjects:
    def __init__(self, page:ft.Page, on_change):
        self.page = page
        self.navigator_category = ft.NavigationRail(
            selected_index=0,
            group_alignment=-1.0,
            label_type=ft.NavigationRailLabelType.ALL,
            indicator_color=page.global_vars["primary_color"],
            indicator_shape=ft.RoundedRectangleBorder(radius=10),
            
            
            selected_label_text_style=ft.TextStyle(color=page.global_vars["primary_color"], size=13),
            unselected_label_text_style=ft.TextStyle(size=12),

            destinations=[
                ft.NavigationRailDestination(
                    data="mod",
                    icon=ft.Container(
                        width=25,
                        height=25,
                        alignment=ft.alignment.center,
                        content=ft.Image(
                            src="iconos/foxy.png",
                            fit=ft.ImageFit.FILL
                        )
                    ),
                    label_content=ft.Text(
                        "Mods", font_family=BaseFonts.buttons,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ),
                ft.NavigationRailDestination(
                    data="modpack",
                    icon=ft.Container(
                        width=25,
                        height=25,
                        alignment=ft.alignment.center,
                        content=ft.Image(
                            src="iconos/box.png",
                            fit=ft.ImageFit.FILL
                        )
                    ),
                    label_content=ft.Text(
                        "Modpacks", font_family=BaseFonts.buttons,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ),
                ft.NavigationRailDestination(
                    data="resourcepack",
                    icon=ft.Container(
                        width=25,
                        height=25,
                        alignment=ft.alignment.center,
                        content=ft.Image(
                            src="iconos/paint.png",
                            fit=ft.ImageFit.FILL
                        )
                    ),
                    label_content=ft.Text(
                        "Resource packs", font_family=BaseFonts.buttons,
                        text_align=ft.TextAlign.CENTER,
                        max_lines=2
                    ),
                ),
                ft.NavigationRailDestination(
                    data="shader",
                    icon=ft.Container(
                        width=30,
                        height=30,
                        alignment=ft.alignment.center,
                        content=ft.Image(
                            src="iconos/shaders.gif",
                            fit=ft.ImageFit.FILL
                        )
                    ),
                    label_content=ft.Text(
                        "Shaders", font_family=BaseFonts.buttons,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ),
                ft.NavigationRailDestination(
                    data="datapack",
                    icon=ft.Container(
                        width=25,
                        height=25,
                        alignment=ft.alignment.center,
                        content=ft.Image(
                            src="iconos/map.png",
                            fit=ft.ImageFit.FILL
                        )
                    ),
                    label_content=ft.Text(
                        "Data packs", font_family=BaseFonts.buttons,
                        text_align=ft.TextAlign.CENTER,
                        max_lines=2
                    ),
                ),
                ft.NavigationRailDestination(
                    data="plugin",
                    icon=ft.Container(
                        width=25,
                        height=25,
                        alignment=ft.alignment.center,
                        content=ft.Image(
                            src="iconos/nut.png",
                            fit=ft.ImageFit.FILL
                        )
                    ),
                    label_content=ft.Text(
                        "Plugins", font_family=BaseFonts.buttons,
                        text_align=ft.TextAlign.CENTER,
                    ),
                )
            ],
            on_change=on_change, #self.change_category
            bgcolor=ft.Colors.BLACK12
        )
    
    def get(self) -> ft.NavigationRail:
        return self.navigator_category