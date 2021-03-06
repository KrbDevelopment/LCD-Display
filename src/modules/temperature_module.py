from src.modules.module import Module as TemplateModule
from PIL import Image, ImageDraw, ImageFont
import os
import json
import time

font_path = os.path.join('assets', 'Font.ttf')

class Module(TemplateModule):
    def __init__(self, display):
        super().__init__(display)
        
        self.display = display
        
        self.font = ImageFont.truetype(font_path, 15)
        
        self.start_image = Image.new('1', (display.width, display.height), "WHITE")
        self.draw_object = ImageDraw.Draw(self.start_image)

        self.temperature = 0
        self.humidity =0

    
    def get_data(self):
        f = open("sensor_data.txt","r")
        data = json.loads(f.read())
        return data["temperature"], data["humidity"]
     
    def draw(self):
        try:
            temperature, humidity = self.get_data()

            if temperature != self.temperature or humidity != self.humidity:
                self.temperature = temperature
                self.humidity = humidity
            
                self.start_image = Image.new('1', (self.display.width, self.display.height), "WHITE")
                self.draw_object = ImageDraw.Draw(self.start_image)
                self.display.clear()
                self.draw_object.text((5, 5), f"Temp: {temperature} °C", font=self.font, fill=0)
                self.draw_object.text((5, 30), f"Hum: {humidity} %", font=self.font, fill=0)
        except:
            pass
    
        return self.start_image
    
    def update(self):
        super().update()
        self.get_data()
    
