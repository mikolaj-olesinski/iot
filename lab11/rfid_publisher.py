#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
from mfrc522 import MFRC522

# Konfiguracja MQTT
broker_address = "localhost"
client = mqtt.Client("RFID_Publisher")
terminal_id = "T0"

# Połączenie z brokerem MQTT
client.connect(broker_address)
client.loop_start()

# Inicjalizacja czytnika MFRC522
rfid_reader = MFRC522()

def read_rfid():
    """Funkcja odczytująca kartę z MFRC522"""
    try:
        print("Przyłóż kartę RFID do czytnika...")
        while True:
            # Wykrywanie karty w zasięgu
            (status, TagType) = rfid_reader.MFRC522_Request(rfid_reader.PICC_REQIDL)
            if status == rfid_reader.MI_OK:
                # Odczyt UID karty
                (status, uid) = rfid_reader.MFRC522_Anticoll()
                if status == rfid_reader.MI_OK:
                    card_id = sum([uid[i] << (i * 8) for i in range(len(uid))])
                    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
                    message = f"{card_id},{terminal_id},{current_time}"
                    client.publish("rfid/card", message)
                    print(f"Odczytano kartę: {card_id}")
                    time.sleep(1)  # Zabezpieczenie przed wielokrotnym odczytem
    except KeyboardInterrupt:
        print("Zatrzymano program.")
        GPIO.cleanup()
        client.disconnect()

if __name__ == "__main__":
    read_rfid()
