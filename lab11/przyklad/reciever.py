#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import tkinter
import sqlite3
import time

# Konfiguracja
broker = "localhost"  # Adres brokera MQTT
client = mqtt.Client()  # Klient MQTT

# Główne okno
window = tkinter.Tk()

def process_message(client, userdata, message):
    """Przetwarzanie wiadomości MQTT."""
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")

    if message_decoded[0] not in ["Client connected", "Client disconnected"]:
        print(f"{time.ctime()}, {message_decoded[0]} used the RFID card.")
        connection = sqlite3.connect("workers.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO workers_log VALUES (?, ?, ?)", 
                       (time.ctime(), message_decoded[0], message_decoded[1]))
        connection.commit()
        connection.close()
    else:
        print(f"{message_decoded[0]}: {message_decoded[1]}")

def print_log_to_window():
    """Wyświetlanie logów w oknie GUI."""
    connection = sqlite3.connect("workers.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM workers_log")
    log_entries = cursor.fetchall()
    connection.close()

    log_window = tkinter.Tk()
    log_window.title("Log Viewer")
    for log_entry in log_entries:
        label = tkinter.Label(log_window, text=(
            f"On {log_entry[0]}, {log_entry[1]} used terminal {log_entry[2]}"
        ))
        label.pack()

    log_window.mainloop()

def create_main_window():
    """Tworzenie GUI."""
    window.geometry("250x100")
    window.title("RECEIVER")

    label = tkinter.Label(window, text="Listening to the MQTT")
    label.pack()

    print_log_button = tkinter.Button(window, text="Print log", command=print_log_to_window)
    print_log_button.pack(side="right")

    exit_button = tkinter.Button(window, text="Stop", command=window.quit)
    exit_button.pack(side="right")

def connect_to_broker():
    """Łączenie z brokerem MQTT."""
    client.connect(broker)
    client.on_message = process_message
    client.loop_start()
    client.subscribe("worker/name")

def disconnect_from_broker():
    """Rozłączanie z brokerem MQTT."""
    client.loop_stop()
    client.disconnect()

def run_receiver():
    """Uruchomienie programu."""
    connect_to_broker()
    create_main_window()
    window.mainloop()
    disconnect_from_broker()

if __name__ == "__main__":
    run_receiver()
