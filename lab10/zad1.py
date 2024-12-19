#!/usr/bin/env python3

import time
import board
import busio
import neopixel
from PIL import Image, ImageDraw, ImageFont
import adafruit_bme280.advanced as adafruit_bme280
import lib.oled.SSD1331 as SSD1331
from config import *

def configure_bme280():
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)
    bme280.sea_level_pressure = 1013.25
    bme280.standby_period = adafruit_bme280.STANDBY_TC_500
    bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16
    return bme280

def read_bme280_data(bme):
    bme.overscan_pressure = adafruit_bme280.OVERSCAN_X16
    bme.overscan_humidity = adafruit_bme280.OVERSCAN_X1
    bme.overscan_temperature = adafruit_bme280.OVERSCAN_X2
    return {
        "temperature": round(bme.temperature, 2),
        "humidity": round(bme.humidity, 2),
        "pressure": round(bme.pressure, 2)
    }


def display_on_oled(parameters):
    disp = SSD1331.SSD1331()
    disp.Init()

    image = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image)

    font_large = ImageFont.truetype('./lib/oled/Font.ttf', 20)
    font_small = ImageFont.truetype('./lib/oled/Font.ttf', 8)

    icons = {
        "temperature": Image.open('./pictures/temperature.jpg').resize((15, 10)),
        "humidity": Image.open('./pictures/humidity.png').resize((15, 10)),
        "pressure": Image.open('./pictures/pressure.png').resize((15, 10))
    }

    image.paste(icons["temperature"], (0, 0))
    draw.text((20, 0), f'Temp: {parameters["temperature"]}°C', font=font_small, fill="BLACK")

    image.paste(icons["humidity"], (0, 25))
    draw.text((20, 25), f'Humidity: {parameters["humidity"]}%', font=font_small, fill="BLACK")

    image.paste(icons["pressure"], (0, 50))
    draw.text((20, 50), f'Pressure: {parameters["pressure"]} hPa', font=font_small, fill="BLACK")

    disp.ShowImage(image, 0, 0)

def main():
    pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0 / 32, auto_write=False)
    bme_sensor = configure_bme280()

    try:
        while True:
            sensor_data = read_bme280_data(bme_sensor)

            display_on_oled(sensor_data)

            time.sleep(1)

    except KeyboardInterrupt:
        print("Program zatrzymany przez użytkownika.")

    finally:
        disp = SSD1331.SSD1331()
        disp.Init()
        disp.clear()
        pixels.fill((0, 0, 0))
        pixels.show()

if __name__ == "__main__":
    main()
