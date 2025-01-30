# import RPi.GPIO as GPIO
# from mfrc522 import MFRC522
# from buzzer import test as buzz
from connect_to_db import connect_to_database
from company_display import CompanyDisplay
import datetime
import time

class CompanyCheckInSystem:
    def __init__(self, company_id=1):
        self.company_id = company_id
        self.display = CompanyDisplay()
        # self.reader = MFRC522.MFRC522()
        
        self.editing_mode = False
        self.current_hours = 0
        self.max_hours = 0
        
        # Konfiguracja GPIO
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(GREEN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # GPIO.setup(ENCODER_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # GPIO.setup(ENCODER_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Rejestracja zdarzeń
        # GPIO.add_event_detect(GREEN_BUTTON, GPIO.FALLING, self.button_callback, bouncetime=200)
        # GPIO.add_event_detect(ENCODER_LEFT, GPIO.FALLING, self.encoder_callback, bouncetime=50)
        # GPIO.add_event_detect(ENCODER_RIGHT, GPIO.FALLING, self.encoder_callback, bouncetime=50)

    def connect_db(self):
        return connect_to_database()

    def button_callback(self, channel):
        if not self.editing_mode:
            # Rozpocznij edycję - pobierz aktualne godziny z bazy
            with self.connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT max_bonus_hours FROM companies WHERE id = %s", (self.company_id,))
                result = cursor.fetchone()
                self.max_hours = result[0] if result else 0
                self.current_hours = self.max_hours
            
            self.editing_mode = True
            self.display_edit_mode()
        else:
            # Zakończ edycję i zapisz do bazy
            self.save_hours_to_db()
            self.editing_mode = False
            self.display.show_confirmation("Hours updated!")
            time.sleep(2)

    def encoder_callback(self, channel):
        if self.editing_mode:
            if channel == ENCODER_LEFT:
                self.current_hours = min(self.current_hours + 1, 24)  # Maksymalnie 24 godziny
            elif channel == ENCODER_RIGHT:
                self.current_hours = max(self.current_hours - 1, 0)
            
            self.display_edit_mode()

    def display_edit_mode(self):
        lines = [
            "Editing hours:",
            f"Current: {self.current_hours}h",
            "Press GREEN to save"
        ]
        self.display.display_message(lines)

    def save_hours_to_db(self):
        try:
            with self.connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE companies 
                    SET max_bonus_hours = %s 
                    WHERE id = %s
                """, (self.current_hours, self.company_id))
                conn.commit()
        except Exception as e:
            print(f"Error saving hours: {e}")
            self.display.show_error("Save failed!")

    def process_check_in(self, conn, card_id):
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, company_checkin_id 
                FROM parking_entries 
                WHERE rfid_tag = %s AND exit_time IS NULL
            """, (card_id,))
            active_parking = cursor.fetchone()

            if not active_parking:
                return "NO_ACTIVE_SESSION"

            if active_parking[1] == self.company_id:
                return "ALREADY_CHECKED_IN"

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
        self.display.show_no_active_session(card_id)
        time.sleep(2)

    def handle_already_checked_in(self, card_id):
        print(f"Vehicle {card_id} is already checked in at company {self.company_id}.")
        self.display.show_already_checked_in(self.company_id)
        time.sleep(2)

    def handle_check_in_success(self, card_id):
        print(f"Vehicle {card_id} successfully checked in at company {self.company_id}.")
        self.display.show_check_in_success(self.company_id)
        time.sleep(2)

    def handle_error(self, card_id, error):
        error_msg = f"Error processing card ID {card_id}: {error}"
        print(error_msg)
        self.display.show_error(str(error))
        time.sleep(2)


    def run(self):
        try:
            print("Company check-in system ready. Please scan card.")
            while True:
                self.display.show_waiting_screen(self.company_id)
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