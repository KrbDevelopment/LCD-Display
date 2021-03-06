from src.wrapper.sh1106 import Screen
from src.modules.clock_module import Module as ClockModule
from src.modules.temperature_module import Module as TemperatureModule
from PIL import Image, ImageDraw, ImageFont
import os

font_path = os.path.join('assets', 'Font.ttf')

class MenuItem:
    def __init__(self, title, module):
        self.title = title
        self.module = module

class Settings: 
    items_on_display = 2
    items_margin = 25

class Menu:
    def __init__(self, display):
        self.display = display
        self.font = ImageFont.truetype(font_path, 20)
        self.current_scroll_index = 0

        self.start_image = Image.new('1', (display.width, display.height), "WHITE")
        self.draw = ImageDraw.Draw(self.start_image)

        self.module = None

        self.menu_items = [
            MenuItem('Uhrzeit', ClockModule(self.display)),
            MenuItem('Temp.', TemperatureModule(self.display))
        ]

        self.reload_menu_items()
        self.draw_menu()

    def draw_menu(self):
        for index, item in enumerate(self.shown_menu):
            self.draw.text((5, Settings.items_margin * index + 5), f"{index + 1} {item.title}", font=self.font, fill=0)
    
    def reload_menu_items(self):
        self.shown_menu = self.menu_items[self.current_scroll_index : (Settings.items_on_display + self.current_scroll_index)]

    def rerender_display(self):
        self.reload_menu_items()
        self.display.clear()
        self.start_image = Image.new('1', (self.display.width, self.display.height), "WHITE")
        self.draw = ImageDraw.Draw(self.start_image)
        self.draw_menu()

    def menu_up(self, channel):
        self.current_scroll_index = min(self.current_scroll_index + 1, len(self.menu_items) - 1)
        self.rerender_display()

    def menu_down(self, channel):
        self.current_scroll_index = max(0, self.current_scroll_index - 1)
        self.rerender_display()

    def menu_option1(self, channel):
        self.select(1)
    
    def menu_option2(self, channel):
        self.select(2)

    def menu_option3(self, channel):
        if self.module is None:
            self.select(3)
        else:
            self.module = None
    
    def select(self, option):
        try:
            module_class = self.shown_menu[option - 1].module
            self.module = module_class
        except IndexError:
            print("This option does not exists.")
        except Exception:
            pass