import RPi.GPIO as GPIO
from mfrc522 import MFRC522
from buzzer import test as buzz
import sqlite3
import datetime
import time

class ParkingSystem:
    def __init__(self):
        self.reader = MFRC522()
        self.price_per_hour = 5.5

    def connect_db(self):
        return connect_to_database()

    def check_or_create_user(self, conn, card_id):
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE rfid_tag = ?", (card_id,))
            user = cursor.fetchone()

            if not user:
                cursor.execute(
                    "INSERT INTO users (rfid_tag, name, balance) VALUES (?, ?, ?)",
                    (card_id, f"User_{card_id}", 0)
                )
                conn.commit()
                
                self.on_user_first_entry(conn, card_id)
                return True
            return False

    def process_parking_entry(self, conn, card_id, current_time):
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, entry_time, exit_time 
                FROM parking_entries 
                WHERE rfid_tag = ? AND exit_time IS NULL
            """, (card_id,))
            existing_entry = cursor.fetchone()

            if existing_entry:
                total_price = self.calculate_parking_price(existing_entry)
                cursor.execute("""
                    UPDATE parking_entries 
                    SET exit_time = ?, total_price = ? 
                    WHERE id = ?
                """, (current_time.strftime('%Y-%m-%d %H:%M:%S'), total_price, existing_entry[0]))
                
                self.update_user_balance(conn, card_id, total_price)
                print(f"User {card_id} exited. Total price: {total_price:.2f} PLN.")
                conn.commit()
                return "EXIT"
            else:
                cursor.execute("""
                    INSERT INTO parking_entries (rfid_tag, entry_time) 
                    VALUES (?, ?)
                """, (card_id, current_time.strftime('%Y-%m-%d %H:%M:%S')))
                print(f"User {card_id} entered.")
                conn.commit()
                return "ENTRY"

    def calculate_parking_price(self, entry_record):
        entry_time = datetime.datetime.strptime(entry_record[1], '%Y-%m-%d %H:%M:%S')
        now = datetime.datetime.now()
        duration = now - entry_time
        hours = duration.total_seconds() / 3600
        rounded_hours = int(hours) if hours == int(hours) else int(hours) + 1 
        total_price = rounded_hours * self.price_per_hour
        return total_price

    def update_user_balance(self, conn, card_id, amount):
        """Aktualizuje saldo użytkownika, odejmując opłatę za parkowanie."""
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT balance FROM users WHERE rfid_tag = ?", (card_id,))
            user = cursor.fetchone()
            if user:
                new_balance = user[0] - amount
                cursor.execute("UPDATE users SET balance = ? WHERE rfid_tag = ?", (new_balance, card_id))
                conn.commit()
                print(f"User {card_id} balance updated. New balance: {new_balance:.2f} PLN.")
        except sqlite3.Error as e:
            print(f"Error updating user balance: {e}")
            raise
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, entry_time, exit_time 
                FROM parking_entries 
                WHERE rfid_tag = ? AND exit_time IS NULL
            """, (card_id,))
            existing_entry = cursor.fetchone()

            if existing_entry:
                cursor.execute("""
                    UPDATE parking_entries 
                    SET exit_time = ?, total_price = 0 
                    WHERE id = ?
                """, (current_time.strftime('%Y-%m-%d %H:%M:%S'), existing_entry[0]))
                
                self.on_user_exit(conn, card_id, existing_entry)
                conn.commit()
                return "EXIT"
            else:
                cursor.execute("""
                    INSERT INTO parking_entries (rfid_tag, entry_time) 
                    VALUES (?, ?)
                """, (card_id, current_time.strftime('%Y-%m-%d %H:%M:%S')))
                
                self.on_user_entry(conn, card_id)
                conn.commit()
                return "ENTRY"

    def first_entry_handler(self, conn, card_id):
        print(f"New user registered: {card_id}")

    def entry_handler(self, conn, card_id):
        print(f"User entered: {card_id}")

    def exit_handler(self, conn, card_id, entry_record):
        print(f"User exited: {card_id}")
        duration = self.calculate_parking_duration(entry_record)
        print(f"Parking duration: {duration}")

    def error_handler(self, error):
        print(f"An error occurred: {error}")


    def run(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(buzzer_pin, GPIO.OUT)

        try:
            while True:
                status, TagType = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
                if status == self.reader.MI_OK:
                    status, uid = self.reader.MFRC522_Anticoll()
                    if status == self.reader.MI_OK:
                        card_id = "".join([str(x) for x in uid])
                        current_time = datetime.datetime.now()

                        try:
                            with self.connect_db() as conn:
                                user_created = self.check_or_create_user(conn, card_id)
                                entry_status = self.process_parking_entry(conn, card_id, current_time)

                                buzz()

                                if user_created:
                                    self.irst_entry_handler(conn, card_id)
                                elif entry_status == "ENTRY":
                                    self.entry_handler(conn, card_id)
                                elif entry_status == "EXIT":
                                    self.exit_handler(conn, card_id)

                                print(f"Card: {card_id} - {entry_status}")
                                print(f"Timestamp: {current_time}")



        except KeyboardInterrupt:
            print("Program terminated")
        finally:
            GPIO.cleanup()

def main():
    parking_system = ParkingSystem()

    parking_system.run()

if __name__ == "__main__":
    main()