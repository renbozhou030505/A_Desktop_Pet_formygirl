# test_events.py
import sys
from unittest.mock import patch
from datetime import datetime
from PyQt6.QtWidgets import QApplication

sys.path.insert(0, '.')
import config
from features.event_manager import EventManager

# A mock object to simulate the pet window for testing purposes
class PetWindowMock:
    def __init__(self):
        self.last_message = None
    
    def show_message_and_interact(self, message, duration=8000, interact=True):
        self.last_message = message
        print(f"MockPet received message: '{message}'")
    
    def is_busy(self):
        return False

def run_test(date_str):
    print(f"\n--- Testing for date: {date_str} ---")
    fake_date = datetime.strptime(date_str, "%Y-%m-%d")

    with patch('features.event_manager.datetime') as mock_dt:
        mock_dt.now.return_value = fake_date
        
        mock_pet = PetWindowMock()
        EventManager(mock_pet)
        
        expected = config.SPECIAL_DATES.get(fake_date.strftime("%m-%d"))
        if expected and mock_pet.last_message == expected:
            print("  [SUCCESS] Correct event triggered.")
        elif not expected and not mock_pet.last_message:
            print("  [SUCCESS] No event triggered as expected.")
        else:
            print(f"  [FAILURE] Mismatch! Expected '{expected}', got '{mock_pet.last_message}'.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    print("--- Running Event Manager Unit Tests ---")
    run_test("2024-12-25")
    run_test("2024-08-08")
    run_test("2024-06-01") # A non-special date
    print("\n--- Tests finished ---")