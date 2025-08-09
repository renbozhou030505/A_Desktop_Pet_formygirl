# main.py
import sys
from PyQt6.QtWidgets import QApplication
from core.pet_window import PetWindow
from utils.logger import get_logger

if __name__ == '__main__':
    log = get_logger("main")
    log.info("Application starting...")
    
    app = QApplication(sys.argv)
    try:
        pet = PetWindow()
        sys.exit(app.exec())
    except Exception as e:
        log.critical("Unhandled exception caught.", exc_info=True)
        sys.exit(1)