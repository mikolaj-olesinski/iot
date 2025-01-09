#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import tkinter as tk

# Konfiguracja brokera MQTT
broker_address = "localhost"
client = mqtt.Client("RFID_Subscriber")

# Funkcja obsługująca odebrane dane
def on_message(client, userdata, message):
    decoded_message = message.payload.decode("utf-8")
    card_id, terminal_id, timestamp = decoded_message.split(",")
    log_label.config(text=f"Karta: {card_id}\nTerminal: {terminal_id}\nCzas: {timestamp}")
    print(f"Odebrano: Karta {card_id} | Terminal {terminal_id} | Czas: {timestamp}")

# Konfiguracja klienta MQTT
client.on_message = on_message
client.connect(broker_address)
client.subscribe("rfid/card")
client.loop_start()

# GUI z Tkinter
def create_main_window():
    global log_label
    window = tk.Tk()
    window.title("RFID Subscriber")
    window.geometry("300x200")

    tk.Label(window, text="Oczekiwanie na dane z czytnika...").pack(pady=10)
    log_label = tk.Label(window, text="", fg="green")
    log_label.pack(pady=10)

    quit_button = tk.Button(window, text="Zamknij", command=window.quit)
    quit_button.pack(pady=20)

    window.mainloop()
    client.loop_stop()

if __name__ == "__main__":
    create_main_window()
