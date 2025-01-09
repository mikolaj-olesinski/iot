#!/usr/bin/env python3

import sqlite3
import os

def create_database():
    # Usuń starą bazę danych, jeśli istnieje
    if os.path.exists("workers.db"):
        os.remove("workers.db")
        print("An old database removed.")
    
    # Utwórz nową bazę danych
    connection = sqlite3.connect("workers.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE workers_log (
            log_time TEXT,
            worker TEXT,
            terminal_id TEXT
        )
    """)
    connection.commit()
    connection.close()
    print("The new database created.")

if __name__ == "__main__":
    create_database()
