#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import tkinter

# Konfiguracja
terminal_id = "T0"  # ID terminala
broker = "localhost"  # Adres brokera MQTT

# Klient MQTT
client = mqtt.Client()

# Główne okno
window = tkinter.Tk()

def call_worker(worker_name):
    """Wysyłanie informacji o pracowniku przez MQTT."""
    client.publish("worker/name", f"{worker_name}.{terminal_id}")

def create_main_window():
    """Tworzenie GUI."""
    window.geometry("300x200")
    window.title("SENDER")

    intro_label = tkinter.Label(window, text="Select employee:")
    intro_label.grid(row=0, columnspan=5)

    workers = [
        "Employee 1", "Employee 2", "Employee 3",
        "Employee 4", "Employee 5", "Employee 6"
    ]

    for idx, worker in enumerate(workers):
        button = tkinter.Button(
            window, text=worker, command=lambda w=worker: call_worker(w)
        )
        button.grid(row=1 + idx // 3, column=idx % 3)

    stop_button = tkinter.Button(window, text="Stop", command=window.quit)
    stop_button.grid(row=4, columnspan=3)

def connect_to_broker():
    """Łączenie z brokerem MQTT."""
    client.connect(broker)
    call_worker("Client connected")

def disconnect_from_broker():
    """Rozłączanie z brokerem MQTT."""
    call_worker("Client disconnected")
    client.disconnect()

def run_sender():
    """Uruchomienie programu."""
    connect_to_broker()
    create_main_window()
    window.mainloop()
    disconnect_from_broker()

if __name__ == "__main__":
    run_sender()
