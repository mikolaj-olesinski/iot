import RPi.GPIO as GPIO
from mfrc522 import MFRC522
from buzzer import test as buzz
from connect_to_db import connect_to_database
import datetime
import time


class CompanyCheckInSystem:
    def __init__(self, company_id=1, bonus_hours=2):
        self.company_id = company_id
        self.bonus_hours = bonus_hours
        self.reader = MFRC522.MFRC522()

    def connect_db(self):
        return connect_to_database()
        

    def get_user(self, conn, card_id):
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE rfid_tag = ?", (card_id,))
            return cursor.fetchone()

    def process_check_in(self, conn, card_id):
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id FROM parking_entries 
                WHERE rfid_tag = ? AND exit_time IS NULL
            """, (card_id,))
            active_parking = cursor.fetchone()

            if not active_parking:
                return "NO_ACTIVE_SESSION"

            cursor.execute("""
                SELECT id FROM bonus_hours 
                WHERE rfid_tag = ? AND company_id = ? AND timestamp >= (
                    SELECT entry_time FROM parking_entries 
                    WHERE rfid_tag = ? AND exit_time IS NULL
                )
            """, (card_id, self.company_id, card_id))
            existing_bonus = cursor.fetchone()

            if existing_bonus:
                return "ALREADY_CHECKED_IN"

            cursor.execute("""
                INSERT INTO bonus_hours (rfid_tag, company_id, bonus_hours) 
                VALUES (?, ?, ?)
            """, (card_id, self.company_id, self.bonus_hours))
            conn.commit()
            return "CHECK_IN_SUCCESS"

    def handle_user_not_found(self, card_id):
        print(f"Error: User with card ID {card_id} does not exist.")

    def handle_no_active_session(self, card_id):
        print(f"User {card_id} has no active parking session.")

    def handle_already_checked_in(self, card_id):
        print(f"User {card_id} already checked in at company {self.company_id}.")

    def handle_check_in_success(self, card_id):
        print(f"User {card_id} successfully checked in at company {self.company_id}.")

    def handle_unknown_status(self, status, card_id):
        print(f"Unknown status for card ID {card_id}: {status}")

    def run(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)  

        try:
            while True:
                status, TagType = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
                if status == self.reader.MI_OK:
                    status, uid = self.reader.MFRC522_Anticoll()
                    if status == self.reader.MI_OK:
                        card_id = "".join([str(x) for x in uid])
                        try:
                            with self.connect_db() as conn:
                                user = self.get_user(conn, card_id)

                                if not user:
                                    self.handle_status("USER_NOT_FOUND", card_id)
                                    continue

                                check_in_status = self.process_check_in(conn, card_id)
                                if check_in_status == "USER_NOT_FOUND":
                                    self.handle_user_not_found(card_id)
                                elif check_in_status == "NO_ACTIVE_SESSION":
                                    self.handle_no_active_session(card_id)
                                elif check_in_status == "ALREADY_CHECKED_IN":
                                    self.handle_already_checked_in(card_id)
                                elif check_in_status == "CHECK_IN_SUCCESS":
                                    self.handle_check_in_success(card_id)
                                else:
                                    self.handle_unknown_status(check_in_status, card_id)

                                buzz()

        except KeyboardInterrupt:
            print("Program terminated.")
        finally:
            GPIO.cleanup()


def main():
    company_check_in_system = CompanyCheckInSystem(company_id=1, bonus_hours=3)
    company_check_in_system.run()


if __name__ == "__main__":
    main()
