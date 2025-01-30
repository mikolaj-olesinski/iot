import time
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331
import board
import busio
import adafruit_bme280.advanced as adafruit_bme280
import datetime

class ParkingDisplay:
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

    def show_waiting_screen(self):
        self.clear_display()
        self.draw.text((10, 10), "Scan Card", font=self.font_large, fill="BLACK")
        self.show_sensor_data()
        self.disp.ShowImage(self.image, 0, 0)

    def show_entry(self, entry_time):
        self.clear_display()
        self.draw.text((10, 0), "Welcome!", font=self.font_large, fill="BLACK")
        self.draw.text((10, 25), f"Time: {entry_time.strftime('%H:%M:%S')}", 
                      font=self.font_small, fill="BLACK")
        self.disp.ShowImage(self.image, 0, 0)

    def show_first_entry(self, entry_time):
        self.clear_display()
        self.draw.text((10, 0), "First Visit!", font=self.font_large, fill="BLACK")
        self.draw.text((10, 25), f"Time: {entry_time.strftime('%H:%M:%S')}", 
                      font=self.font_small, fill="BLACK")
        self.disp.ShowImage(self.image, 0, 0)

    def show_exit(self, data):
        self.clear_display()
        duration = str(data['exit_time'] - data['entry_time']).split('.')[0]
        
        self.draw.text((10, 0), "Goodbye!", font=self.font_large, fill="BLACK")
        self.draw.text((10, 25), f"Duration: {duration}", 
                      font=self.font_small, fill="BLACK")
        self.draw.text((10, 40), f"Price: {data['total_price']:.2f} PLN", 
                      font=self.font_small, fill="BLACK")
        self.disp.ShowImage(self.image, 0, 0)