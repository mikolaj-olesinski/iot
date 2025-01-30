# import RPi.GPIO as GPIO
# from mfrc522 import MFRC522
# from buzzer import test as buzz
from connect_to_db import connect_to_database
import datetime
import time

class CompanyCheckInSystem:
    def __init__(self, company_id=1):
        self.company_id = company_id
        # self.reader = MFRC522.MFRC522()

    def connect_db(self):
        return connect_to_database()

    def process_check_in(self, conn, card_id):
        cursor = conn.cursor()
        try:
            # Check for active parking session
            cursor.execute("""
                SELECT id, company_checkin_id 
                FROM parking_entries 
                WHERE rfid_tag = %s AND exit_time IS NULL
            """, (card_id,))
            active_parking = cursor.fetchone()

            if not active_parking:
                return "NO_ACTIVE_SESSION"

            # If already checked in to this company
            if active_parking[1] == self.company_id:
                return "ALREADY_CHECKED_IN"

            # Update the parking entry with company check-in
            cursor.execute("""
                UPDATE parking_entries 
                SET company_checkin_id = %s
                WHERE id = %s
            """, (self.company_id, active_parking[0]))
            
            conn.commit()
            return "CHECK_IN_SUCCESS"

        except Exception as e:
            print(f"Error processing check-in: {e}")
            return "ERROR"

    def handle_no_active_session(self, card_id):
        print(f"Vehicle {card_id} has no active parking session.")

    def handle_already_checked_in(self, card_id):
        print(f"Vehicle {card_id} is already checked in at company {self.company_id}.")

    def handle_check_in_success(self, card_id):
        print(f"Vehicle {card_id} successfully checked in at company {self.company_id}.")

    def handle_error(self, card_id, error):
        print(f"Error processing card ID {card_id}: {error}")

    def run(self):
        try:
            print("Company check-in system ready. Please scan card.")
            while True:
                status, TagType = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
                if status == self.reader.MI_OK:
                    status, uid = self.reader.MFRC522_Anticoll()
                    if status == self.reader.MI_OK:
                        card_id = "".join([str(x) for x in uid])
                        buzz()
                        try:
                            with self.connect_db() as conn:
                                check_in_status = self.process_check_in(conn, card_id)
                                
                                if check_in_status == "NO_ACTIVE_SESSION":
                                    self.handle_no_active_session(card_id)
                                elif check_in_status == "ALREADY_CHECKED_IN":
                                    self.handle_already_checked_in(card_id)
                                elif check_in_status == "CHECK_IN_SUCCESS":
                                    self.handle_check_in_success(card_id)
                                else:
                                    self.handle_error(card_id, check_in_status)

                        except Exception as e:
                            self.handle_error(card_id, e)

        except KeyboardInterrupt:
            print("Program terminated.")
        finally:
            GPIO.cleanup()

def main():
    self = CompanyCheckInSystem(company_id=1)
    card_id = "123456785559"
    with self.connect_db() as conn:
        check_in_status = self.process_check_in(conn, card_id)
        
        if check_in_status == "NO_ACTIVE_SESSION":
            self.handle_no_active_session(card_id)
        elif check_in_status == "ALREADY_CHECKED_IN":
            self.handle_already_checked_in(card_id)
        elif check_in_status == "CHECK_IN_SUCCESS":
            self.handle_check_in_success(card_id)
        else:
            self.handle_error(card_id, check_in_status)

if __name__ == "__main__":
    main()