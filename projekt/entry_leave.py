# import RPi.GPIO as GPIO
# from mfrc522 import MFRC522
# from buzzer import test as buzz
import datetime
import time
from connect_to_db import connect_to_database

class ParkingSystem:
    def __init__(self):
        # self.reader = MFRC522()
        self.price_per_hour = 10.00

    def connect_db(self):
        return connect_to_database()

    def is_first_time_entry(self, conn, card_id):
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM parking_entries 
                WHERE rfid_tag = %s
            """, (card_id,))
            count = cursor.fetchone()[0]
            return count == 0
        except Exception as e:
            print(f"Error checking first time entry: {e}")
            return False

    def get_company_bonus_hours(self, conn, parking_entry_id):
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT c.max_bonus_hours 
                FROM parking_entries pe
                JOIN companies c ON pe.company_checkin_id = c.id
                WHERE pe.id = %s
            """, (parking_entry_id,))
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error getting company bonus hours: {e}")
            return 0

    def process_parking_entry(self, conn, card_id, current_time):
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, entry_time, exit_time, company_checkin_id
                FROM parking_entries 
                WHERE rfid_tag = %s AND exit_time IS NULL
            """, (card_id,))

            existing_entry = cursor.fetchone()

            if existing_entry:
                # This is an exit
                bonus_hours = self.get_company_bonus_hours(conn, existing_entry[0])
                total_price, duration = self.calculate_parking_price(existing_entry, bonus_hours)
                
                cursor.execute("""
                    UPDATE parking_entries 
                    SET exit_time = %s, total_price = %s, duration = %s
                    WHERE id = %s
                """, (current_time.strftime('%Y-%m-%d %H:%M:%S'), 
                        total_price, 
                        duration,
                        existing_entry[0]))

                entry_time = datetime.datetime.strptime(str(existing_entry[1]), '%Y-%m-%d %H:%M:%S')
                
                conn.commit()
                return "EXIT", {
                    'entry_time': entry_time,
                    'exit_time': current_time,
                    'duration': duration,
                    'total_price': total_price,
                    'bonus_hours': bonus_hours
                }
            else:
                # This is an entry
                is_first_time = self.is_first_time_entry(conn, card_id)
                
                cursor.execute("""
                    INSERT INTO parking_entries (rfid_tag, entry_time) 
                    VALUES (%s, %s)
                """, (card_id, current_time.strftime('%Y-%m-%d %H:%M:%S')))
                
                conn.commit()
                return ("FIRST_ENTRY" if is_first_time else "ENTRY"), {
                    'entry_time': current_time
                }

        except Exception as e:
            print(f"Error processing parking entry: {e}")
            return "ERROR", None

    def calculate_parking_price(self, entry_record, bonus_hours=0):
        entry_time = entry_record[1]
        if isinstance(entry_time, str):
            entry_time = datetime.datetime.strptime(entry_time, '%Y-%m-%d %H:%M:%S')
        
        now = datetime.datetime.now()
        duration = (now - entry_time).total_seconds() / 3600
        
        if bonus_hours > 0:
            billable_hours = max(0, duration - bonus_hours)
            rounded_billable_hours = int(billable_hours) if billable_hours == int(billable_hours) else int(billable_hours) + 1
            total_price = rounded_billable_hours * self.price_per_hour
        else:

            rounded_hours = int(duration) if duration == int(duration) else int(duration) + 1
            total_price = rounded_hours * self.price_per_hour
        
        return total_price, duration

    def first_entry_handler(self, conn, card_id, data):
        print(f"Welcome! First time seeing vehicle with tag: {card_id}")
        print(f"Entry time: {data['entry_time'].strftime('%H:%M:%S')}")
        self.display.show_first_entry(data['entry_time'])
        time.sleep(2)  

    def entry_handler(self, conn, card_id, data):
        print(f"Welcome back! Vehicle entered: {card_id}")
        print(f"Entry time: {data['entry_time'].strftime('%H:%M:%S')}")
        self.display.show_entry(data['entry_time'])
        time.sleep(2) 

    def exit_handler(self, conn, card_id, data):
        print(f"Goodbye! Vehicle exited: {card_id}")
        print(f"Entry time: {data['entry_time'].strftime('%H:%M:%S')}")
        print(f"Exit time: {data['exit_time'].strftime('%H:%M:%S')}")
        duration_str = str(data['exit_time'] - data['entry_time']).split('.')[0]
        print(f"Duration: {duration_str}")
        if data['bonus_hours'] > 0:
            print(f"Company bonus hours used: {data['bonus_hours']}")
        print(f"Total price: {data['total_price']:.2f} PLN")
        
        self.display.show_exit(data)
        time.sleep(2)

    def run(self):
            try:
                print("System ready. Please scan card.")
                while True:
                    self.display.show_waiting_screen()
                    status, TagType = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
                    if status == self.reader.MI_OK:
                        status, uid = self.reader.MFRC522_Anticoll()
                        if status == self.reader.MI_OK:
                            card_id = "".join([str(x) for x in uid])
                            current_time = datetime.datetime.now()
                            buzz()
                            try:
                                with self.connect_db() as conn:
                                    entry_status, data = self.process_parking_entry(conn, card_id, current_time)

                                    if entry_status == "FIRST_ENTRY":
                                        self.first_entry_handler(conn, card_id, data)
                                    elif entry_status == "ENTRY":
                                        self.entry_handler(conn, card_id, data)
                                    elif entry_status == "EXIT":
                                        self.exit_handler(conn, card_id, data)

                            except Exception as e:
                                self.error_handler(e)

            except KeyboardInterrupt:
                print("Program terminated")
            finally:
                GPIO.cleanup()

def main():
    parking_system = ParkingSystem()
    card_id = "123456785559"
    with parking_system.connect_db() as conn:
        entry_status, data = parking_system.process_parking_entry(conn, card_id, datetime.datetime.now())

        if entry_status == "FIRST_ENTRY":
            parking_system.first_entry_handler(conn, card_id, data)
        elif entry_status == "ENTRY":
            parking_system.entry_handler(conn, card_id, data)
        elif entry_status == "EXIT":
            parking_system.exit_handler(conn, card_id, data)

if __name__ == "__main__":
    main()