import time
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331
import board
import busio
import adafruit_bme280.advanced as adafruit_bme280
import datetime
from connect_to_db import connect_to_database

class CompanyDisplay:
    def __init__(self):
        self.disp = SSD1331.SSD1331()
        self.disp.Init()
        self.disp.clear()
        
        i2c = busio.I2C(board.SCL, board.SDA)
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)
        
        self.image = Image.new("RGB", (self.disp.width, self.disp.height), "WHITE")
        self.draw = ImageDraw.Draw(self.image)
        self.font_large = ImageFont.truetype('./lib/oled/Font.ttf', 20)
        self.font_small = ImageFont.truetype('./lib/oled/Font.ttf', 13)
        
        self.icon_temp = Image.open('/home/pi/tests/temperature_icon_resized.jpg').convert("RGBA")
        self.icon_humidity = Image.open('/home/pi/tests/humidity_icon_resized.jpg').convert("RGBA")
        self.icon_pressure = Image.open('/home/pi/tests/pressure_icon_resized.jpg').convert("RGBA")

    def clear_display(self):
        self.draw.rectangle([(0, 0), (self.disp.width, self.disp.height)], fill="WHITE")

    def show_sensor_data(self):
        temperature = self.bme280.temperature
        humidity = self.bme280.humidity
        pressure = self.bme280.pressure
        
        self.image.paste(self.icon_temp, (10, 0), self.icon_temp)
        self.image.paste(self.icon_humidity, (10, 20), self.icon_humidity)
        self.image.paste(self.icon_pressure, (10, 40), self.icon_pressure)
        
        self.draw.text((25, 0), f"{temperature:.1f}°C", font=self.font_small, fill="BLACK")
        self.draw.text((25, 20), f"{humidity:.1f}%", font=self.font_small, fill="BLACK")
        self.draw.text((25, 40), f"{pressure:.1f} hPa", font=self.font_small, fill="BLACK")

    def show_waiting_screen(self, company_id):
        self.clear_display()
        self.draw.text((10, 0), f"Company #{company_id}", font=self.font_small, fill="BLACK")
        self.draw.text((10, 15), "Scan Card", font=self.font_large, fill="BLACK")
        self.show_sensor_data()
        self.disp.ShowImage(self.image, 0, 0)

    def show_no_active_session(self, card_id):
        self.clear_display()
        self.draw.text((10, 0), "No Active", font=self.font_large, fill="BLACK")
        self.draw.text((10, 25), "Parking Session!", font=self.font_small, fill="BLACK")
        self.draw.text((10, 45), f"Card: {card_id[-4:]}", font=self.font_small, fill="BLACK")
        self.disp.ShowImage(self.image, 0, 0)

    def show_already_checked_in(self, company_id):
        self.clear_display()
        self.draw.text((10, 0), "Already", font=self.font_large, fill="BLACK")
        self.draw.text((10, 25), f"Checked In", font=self.font_small, fill="BLACK")
        self.draw.text((10, 45), f"Company #{company_id}", font=self.font_small, fill="BLACK")
        self.disp.ShowImage(self.image, 0, 0)

    def show_check_in_success(self, company_id):
        self.clear_display()
        self.draw.text((10, 0), "Welcome!", font=self.font_large, fill="BLACK")
        self.draw.text((10, 25), "Check-in", font=self.font_small, fill="BLACK")
        self.draw.text((10, 45), f"Company #{company_id}", font=self.font_small, fill="BLACK")
        self.disp.ShowImage(self.image, 0, 0)

    def show_error(self, error_msg):
        self.clear_display()
        self.draw.text((10, 0), "Error!", font=self.font_large, fill="BLACK")
        # Podziel długi komunikat błędu na krótsze linie
        words = error_msg.split()
        lines = []
        current_line = []
        for word in words:
            if len(' '.join(current_line + [word])) <= 20:  # maksymalna długość linii
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
            
        for i, line in enumerate(lines[:2]):  # Pokaż maksymalnie 2 linie błędu
            self.draw.text((10, 25 + i*20), line, font=self.font_small, fill="BLACK")
        self.disp.ShowImage(self.image, 0, 0)