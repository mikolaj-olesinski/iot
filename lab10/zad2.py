#!/usr/bin/env python3

import time
from datetime import datetime
import RPi.GPIO as GPIO
from config import *
from mfrc522 import MFRC522

executing = True
last_uid = None
ignore_duration = 5 
last_scan_time = 0

def toggle_executing():
    global executing
    executing = not executing
    print(f"Stan wykonywania: {'Włączony' if executing else 'Wyłączony'}")

def buzzer_state(state):
    GPIO.output(buzzerPin, not state)

def buzzer_beep():
    buzzer_state(True)
    time.sleep(1)
    buzzer_state(False)

def led_blink():
    GPIO.output(led1, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(led1, GPIO.LOW)
    time.sleep(1)

def read_rfid():
    global last_uid, last_scan_time
    reader = MFRC522()

    while True:
        if not executing:
            time.sleep(0.1)
            continue

        current_time = time.time()
        status, tag_type = reader.MFRC522_Request(reader.PICC_REQIDL)
        if status == reader.MI_OK:
            status, uid = reader.MFRC522_Anticoll()
            if status == reader.MI_OK:
                card_id = sum(uid[i] << (i * 8) for i in range(len(uid)))

                if card_id != last_uid or (current_time - last_scan_time) > ignore_duration:
                    scan_time = datetime.now()

                    print(f"Karta odczytana UID: {card_id}")
                    print(f"Data i czas skanowania: {scan_time}")

                    last_uid = card_id
                    last_scan_time = current_time

                    buzzer_beep()
                    led_blink()

def main():
    try:
        print("Naciśnij spację, aby włączyć/wyłączyć wykonywanie odczytów.")
        while True:
            user_input = input(">> ").strip()
            if user_input == " ":
                toggle_executing()
            if executing:
                read_rfid()
    except KeyboardInterrupt:
        print("Program przerwany.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
