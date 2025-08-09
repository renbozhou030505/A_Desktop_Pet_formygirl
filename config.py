# config.py
# Pet package to use
CURRENT_PET = "puppy_classic"

# Feature toggles
REMINDERS_ENABLED = True
RANDOM_CARE_ENABLED = True
EASTER_EGGS_ENABLED = True

# Reminder settings
MEAL_REMINDERS = {
    (12, 0): "主人，午饭时间到啦，要好好吃饭补充能量哦！(๑´ڡ`๑)",
    (18, 30): "工作辛苦啦，快去享用美味的晚餐吧！"
}
SLEEP_REMINDER_HOUR = 23 # 11 PM

# Intervals in milliseconds
REST_REMINDER_INTERVAL = 1 * 60 * 60 * 1000  # 1 hour
RANDOM_CARE_INTERVAL = 30 * 60 * 1000      # 30 minutes

# Special dates ("Month-Day": "Message")
SPECIAL_DATES = {
    "01-01": "新年快乐！新的一年也要元气满满哦！",
    "02-14": "无论是自己还是和别人过，今天都要开心呀，情人节快乐！(｡･ω･｡)ﾉ♡",
    "12-25": "Merry Christmas! 圣诞快乐！♪(･ω･)ﾉ",
    # Add your own special date here!
    "08-08": "这是一个只属于我们的秘密纪念日，要永远开心哦！"
}