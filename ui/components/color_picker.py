import flet as ft

SLIDER_WIDTH = 180
CIRCLE_SIZE = 16


class color_utils:
    @staticmethod
    def rgb_to_hex(rgb_color):
        return "#{:02x}{:02x}{:02x}".format(rgb_color[0], rgb_color[1], rgb_color[2])

    @staticmethod
    def rgb_to_hsl(r, g, b):
        r /= 255.0
        g /= 255.0
        b /= 255.0
        max_c, min_c = max(r, g, b), min(r, g, b)
        delta = max_c - min_c
        l = (max_c + min_c) / 2

        if delta == 0:
            h = 0
            s = 0
        else:
            s = delta / (1 - abs(2 * l - 1))
            if max_c == r:
                h = 60 * (((g - b) / delta) % 6)
            elif max_c == g:
                h = 60 * (((b - r) / delta) + 2)
            else:
                h = 60 * (((r - g) / delta) + 4)

        return round(h), round(s * 100), round(l * 100)

    @staticmethod
    def rgb_to_hsv(r, g, b):
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        max_c, min_c = max(r, g, b), min(r, g, b)
        delta = max_c - min_c

        if max_c == min_c:
            h = 0
        elif max_c == r:
            h = (60 * ((g - b) / delta) + 360) % 360
        elif max_c == g:
            h = (60 * ((b - r) / delta) + 120) % 360
        else:
            h = (60 * ((r - g) / delta) + 240) % 360

        s = 0 if max_c == 0 else delta / max_c
        v = max_c
        return round(h), round(s * 100), round(v * 100)

    @staticmethod
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i: i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def hex_to_hsl(hex_color):
        r, g, b = color_utils.hex_to_rgb(hex_color)
        return color_utils.rgb_to_hsl(r, g, b)

    @staticmethod
    def mix_colors(color1, color2, ratio):
        return [
            int(color1[0] + (color2[0] - color1[0]) * ratio),
            int(color1[1] + (color2[1] - color1[1]) * ratio),
            int(color1[2] + (color2[2] - color1[2]) * ratio),
        ]

    @staticmethod
    def hsv_to_rgb(h, s, v):
        if s == 0:
            r = g = b = int(v * 255)
            return r, g, b

        i = int(h * 6)
        f = (h * 6) - i
        p = int(255 * v * (1 - s))
        q = int(255 * v * (1 - s * f))
        t = int(255 * v * (1 - s * (1 - f)))
        v = int(255 * v)
        i %= 6

        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        else:
            r, g, b = v, p, q
        return r, g, b

    @staticmethod
    def hex_to_hsv(hex_color):
        r, g, b = color_utils.hex_to_rgb(hex_color)
        return color_utils.rgb_to_hsv(r, g, b)


class HueSlider(ft.GestureDetector):
    def __init__(self, on_change_hue, hue=0.0):
        super().__init__()
        self.__hue = hue
        self.__number_of_hues = 10
        self.content = ft.Stack(height=CIRCLE_SIZE, width=SLIDER_WIDTH)
        self.generate_slider()
        self.on_change_hue = on_change_hue
        self.on_pan_start = self.drag
        self.on_pan_update = self.drag

    @property
    def hue(self) -> float:
        return self.__hue

    @hue.setter
    def hue(self, value: float):
        if not isinstance(value, float):
            raise Exception("Hue value must be float")
        if 0 <= value <= 1:
            self.__hue = value
        else:
            raise Exception("Hue value should be between 0 and 1")

    def before_update(self):
        self.thumb.left = self.__hue * self.track.width
        self.thumb.bgcolor = color_utils.rgb_to_hex(
            color_utils.hsv_to_rgb(self.__hue, 1, 1)
        )

    def drag(self, e: ft.DragUpdateEvent):
        self.__hue = max(0, min((e.local_x - CIRCLE_SIZE / 2) / self.track.width, 1))
        self.update()
        self.on_change_hue()

    def generate_gradient_colors(self):
        return [
            color_utils.rgb_to_hex(color_utils.hsv_to_rgb(i / self.__number_of_hues, 1, 1))
            for i in range(self.__number_of_hues + 1)
        ]

    def generate_slider(self):
        self.track = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=self.generate_gradient_colors(),
            ),
            width=SLIDER_WIDTH - CIRCLE_SIZE,
            height=CIRCLE_SIZE / 2,
            border_radius=5,
            top=CIRCLE_SIZE / 4,
            left=CIRCLE_SIZE / 2,
        )
        self.thumb = ft.Container(
            width=CIRCLE_SIZE,
            height=CIRCLE_SIZE,
            border_radius=CIRCLE_SIZE,
            border=ft.border.all(width=1, color="white"),
        )
        self.content.controls += [self.track, self.thumb]


class ColorPicker(ft.Container):
    def __init__(self, color="#000000", on_color_select=None, width=220, height=220, **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.current_color = color
        self._on_color_select = on_color_select
        self.color_display_ref = ft.Ref[ft.Container]()
        self.color_text_ref = ft.Ref[ft.Text]()
        self.hue_slider = HueSlider(
            on_change_hue=self.update_picker_color,
            hue=color_utils.hex_to_hsv(self.color)[0] / 360,
        )
        self._width, self._height = width, height
        self.init_controls()

    def init_controls(self):
        self.vertical_gradient = ft.Container(
            width=self._width,
            height=self._height,
            border_radius=10,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["transparent", "#000000"],
            ),
        )
        self.horizontal_gradient = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=["#ffffff", self.color],
            ),
            width=self._width,
            height=self._height,
            border_radius=10
        )
        self.selector_circle = ft.Container(
            width=20,
            height=20,
            border_radius=20,
            border=ft.border.all(2, "white"),
            bgcolor=self.color,
        )
        stack = ft.Stack(
            [self.horizontal_gradient, self.vertical_gradient, self.selector_circle],
            width=self._width,
            height=self._height,
        )
        color_area = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.CLICK,
            on_tap=self.on_tap,
            on_pan_start=self.on_drag,
            on_pan_update=self.on_drag,
            content=stack,
        )
        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(ref=self.color_display_ref, width=25, height=25,
                                     border_radius=7, bgcolor=self.color),
                        ft.Text(ref=self.color_text_ref, value=self.color,
                                style=ft.TextStyle(size=20, weight=ft.FontWeight.W_100), selectable=True),
                    ], alignment=ft.MainAxisAlignment.CENTER
                ),
                color_area,
                ft.Row([ft.Icon(ft.Icons.COLORIZE_ROUNDED, size=15, color="white"),
                        self.hue_slider], alignment=ft.MainAxisAlignment.CENTER),
            ], alignment=ft.MainAxisAlignment.CENTER
        )
        self.bgcolor = "transparent"
        self.width = self._width
        self.border_radius = 10

        h, s, v = color_utils.hex_to_hsv(self.color)
        x = (s / 100) * self._width
        y = (1 - v / 100) * self._height

        self.selector_circle.left = x - 10
        self.selector_circle.top = y - 10
        self.current_color = self.calculate_color(x, y)
        self.selector_circle.bgcolor = self.current_color

    def set_color(self, color: str):
        rgb = color_utils.hex_to_rgb(color)
        h, s, v = color_utils.rgb_to_hsv(*rgb)

        # mover el HueSlider
        self.hue_slider.hue = h / 360
        self.hue_slider.update()
        
        self.color = color_utils.rgb_to_hex(
        color_utils.hsv_to_rgb(self.hue_slider.hue, 1.0, 1.0)
        )
        self.horizontal_gradient.gradient.colors = ["#ffffff", self.color]
        self.horizontal_gradient.update()

        # calcular posición exacta del selector
        x = (s / 100) * self._width
        y = (1 - v / 100) * self._height

        self.set_selector(x, y)
        self.current_color = color

    def set_selector(self, x, y):
        self.selector_circle.left = x - self.selector_circle.width / 2
        self.selector_circle.top = y - self.selector_circle.height / 2
        self.current_color = self.calculate_color(x, y)

        self.selector_circle.bgcolor = self.current_color

        if self.color_display_ref.current and self.color_text_ref.current:
            self.color_display_ref.current.bgcolor = self.current_color
            self.color_text_ref.current.value = self.current_color
            self.color_display_ref.current.update()
            self.color_text_ref.current.update()

        self.update()

    def _get_xy(self, e):
        try:
            if hasattr(e, "local_x"):
                return float(e.local_x), float(e.local_y)

            if e.data and "," in e.data:
                x, y = e.data.split(",")
                return float(x), float(y)
        except:
            return None, None
        return None, None

    def on_tap(self, e):
        x, y = self._get_xy(e)
        if x is not None and y is not None:
            self.set_selector(x, y)

    def on_drag(self, e):
        x, y = self._get_xy(e)
        if x is not None and y is not None:
            self.set_selector(x, y)

    def calculate_color(self, x, y):
        # Normalizar posiciones
        s = max(0, min(1, x / self._width))
        v = max(0, min(1, 1 - (y / self._height)))

        # Tomar el hue actual
        h = self.hue_slider.hue

        # Convertir HSV → RGB → HEX
        r, g, b = color_utils.hsv_to_rgb(h, s, v)
        return color_utils.rgb_to_hex((r, g, b))

    def update_picker_color(self):
        # color base para el gradiente
        self.color = color_utils.rgb_to_hex(
            color_utils.hsv_to_rgb(self.hue_slider.hue, 1.0, 1.0)
        )
        self.horizontal_gradient.gradient.colors = ["#ffffff", self.color]

        # mantener la posición actual del selector y recalcular el color final
        x = float(self.selector_circle.left) + self.selector_circle.width / 2
        y = float(self.selector_circle.top) + self.selector_circle.height / 2
        self.set_selector(x, y)


