#!/usr/bin/env python3

from config import *
import RPi.GPIO as GPIO
import time

class EncoderPWMController:
    def __init__(self, led_pin, encoder_left, encoder_right):
        self.brightness = 0
        self.led_pin = led_pin
        self.encoder_left = encoder_left
        self.encoder_right = encoder_right
        self.diode = GPIO.PWM(self.led_pin, 50)
        self.encoder_left_previous_state = GPIO.input(self.encoder_left)
        self.encoder_right_previous_state = GPIO.input(self.encoder_right)

    def turn_encoder(self, channel):
        encoder_left_current_state = GPIO.input(self.encoder_left)
        encoder_right_current_state = GPIO.input(self.encoder_right)

        if self.encoder_left_previous_state == 1 and encoder_left_current_state == 0 and self.brightness < 100:
            self.brightness += 10
            self.diode.ChangeDutyCycle(self.brightness)
            print(self.brightness)
        elif self.encoder_right_previous_state == 1 and encoder_right_current_state == 0 and self.brightness > 0:
            self.brightness -= 10
            self.diode.ChangeDutyCycle(self.brightness)
            print(self.brightness)

        self.encoder_left_previous_state = encoder_left_current_state
        self.encoder_right_previous_state = encoder_right_current_state

    def start(self):
        self.diode.start(0)
        GPIO.add_event_detect(self.encoder_left, GPIO.FALLING, callback=self.turn_encoder, bouncetime=200)
        GPIO.add_event_detect(self.encoder_right, GPIO.FALLING, callback=self.turn_encoder, bouncetime=200)

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led1, GPIO.OUT)
    GPIO.setup(encoderLeft, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(encoderRight, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    encoder = EncoderPWMController(led1, encoderLeft, encoderRight)
    enncoder.start()

    while True:
        pass

if __name__ == "__main__":
    main()