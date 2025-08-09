# features/reminder_manager.py
from PyQt6.QtCore import QTimer
from datetime import datetime
import config

class ReminderManager:
    def __init__(self, pet):
        self.pet = pet
        self.last_meal_day = -1
        
        if config.REMINDERS_ENABLED:
            self.minute_timer = QTimer(timeout=self.check_schedule)
            self.minute_timer.start(60 * 1000)

            self.rest_timer = QTimer(timeout=self.remind_to_rest)
            self.rest_timer.start(config.REST_REMINDER_INTERVAL)
            
    def check_schedule(self):
        now = datetime.now()
        
        # Meal reminders
        time_now = (now.hour, now.minute)
        if time_now in config.MEAL_REMINDERS and now.day != self.last_meal_day:
            message = config.MEAL_REMINDERS[time_now]
            self.pet.show_message_and_interact(message)
            self.last_meal_day = now.day

        # Sleep reminder
        if now.hour == config.SLEEP_REMINDER_HOUR and now.minute == 0:
            self.pet.show_message_and_interact("夜深啦，主人。为了身体健康，要早点休息哦。晚安！")

    def remind_to_rest(self):
        self.pet.show_message_and_interact("主人，你已经坐了很久啦！起来活动一下，看看远方吧！")