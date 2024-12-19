#!/usr/bin/env python3

import time
import os
import board
import busio
import neopixel
import RPi.GPIO as GPIO
import adafruit_bme280.advanced as adafruit_bme280
import w1thermsensor
from config import *


current_parameter = 0
use_ds18b20 = True
color = (255, 0, 0)
LED_COUNT = 8 


PARAMETERS = {
    "ds18b20_temperature": {
        "min": 18,
        "max": 25,
        "color": (255, 0, 0)
    },
    "bme280_temperature": {
        "min": 18,
        "max": 25,
        "color": (255, 127, 0)
    },
    "humidity": {
        "min": 40,
        "max": 47,
        "color": (0, 255, 0)
    },
    "pressure": {
        "min": 995,
        "max": 1002,
        "color": (0, 0, 255)
    }
}


def read_ds18b20():
    sensor = w1thermsensor.W1ThermSensor()
    temp = sensor.get_temperature()
    print(f"\nDS18B20 Temp: {temp} °C")
    return temp

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
        "temperature": bme.temperature,
        "humidity": bme.humidity,
        "pressure": bme.pressure
    }

def map_value_to_led(value, min_value, max_value, led_count):
    if value < min_value:
        return 0
    if value > max_value:
        return led_count - 1

    normalized = (value - min_value) / (max_value - min_value)
    return int(normalized * (led_count - 1))

def update_led_strip(pixel, sensor_data):
    global current_parameter

    pixel.fill((0, 0, 0))

    parameter_keys = list(PARAMETERS.keys())
    parameter_key = parameter_keys[current_parameter]
    parameter_data = PARAMETERS[parameter_key]

    value = sensor_data[parameter_key]
    led_index = map_value_to_led(value, parameter_data["min"], parameter_data["max"], LED_COUNT)

    print(f"{parameter_key.capitalize()}: {value}")

    pixel[led_index] = parameter_data["color"]
    pixel.show()

def space_pressed_callback():
    global current_parameter

    current_parameter = (current_parameter + 1) % len(PARAMETERS)
    parameter_keys = list(PARAMETERS.keys())
    parameter_key = parameter_keys[current_parameter]

    print(f"Spacebar pressed. Current parameter: {parameter_key.capitalize()}")

if __name__ == "__main__":
    pixels = neopixel.NeoPixel(board.D18, LED_COUNT, brightness=1.0 / 32, auto_write=False)
    bme_sensor = configure_bme280()

    try:
        while True:
            ds18b20_temperature = read_ds18b20()
            bme_data = read_bme280_data(bme_sensor)

            sensor_data = {
                "ds18b20_temperature": ds18b20_temperature,
                "bme280_temperature": bme_data["temperature"],
                "humidity": bme_data["humidity"],
                "pressure": bme_data["pressure"]
            }

            update_led_strip(pixels, sensor_data)

            user_input = input("Press space to change parameter, or Enter to continue: ")
            if user_input.strip() == " ":
                space_pressed_callback()

            time.sleep(1)

    except KeyboardInterrupt:
        print("Program terminated.")

    finally:
        GPIO.cleanup()
        pixels.fill((0, 0, 0))
        pixels.show()
