# features/event_manager.py
from PyQt6.QtCore import QTimer
from datetime import datetime
import random
import config

CARE_MESSAGES = ["今天也要开心呀！(｡･ω･｡)ﾉ♡", "在忙吗？别太累啦，我会一直陪着你的。", "你对我真好，最喜欢你啦！"]

class EventManager:
    def __init__(self, pet):
        self.pet = pet
        self.has_special_event_today = False
        
        if config.EASTER_EGGS_ENABLED:
            self.check_special_day()
            
        if config.RANDOM_CARE_ENABLED:
            self.care_timer = QTimer(timeout=self.trigger_random_care)
            # Start after a short delay to avoid overlapping with startup messages
            QTimer.singleShot(60 * 1000, lambda: self.care_timer.start(config.RANDOM_CARE_INTERVAL))

    def check_special_day(self):
        msg = config.SPECIAL_DATES.get(datetime.now().strftime("%m-%d"))
        if msg:
            self.has_special_event_today = True
            QTimer.singleShot(2000, lambda: self.pet.show_message_and_interact(msg, duration=15000))

    def trigger_random_care(self):
        if not self.pet.is_busy():
            self.pet.show_message_and_interact(random.choice(CARE_MESSAGES))