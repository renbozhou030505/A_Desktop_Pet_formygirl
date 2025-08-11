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
    "01-01": "新年快乐，希望我能陪你度过一年又一年",
    "02-14": "情人节快乐,亲爱的阳阳♡",
    "12-25": "Merry Christmas!",
    # Add your own special date here!
    "08-12": "今天是我的生日哦，记得给我庆祝哦！"
}

# --- Weather Feature Settings ---
WEATHER_ENABLED = True
# 填入你在和风天气申请的API Key
WEATHER_API_KEY = "" 
# 用户的默认城市，这里需要城市的Location ID，而不是中文名。
# 你可以在 https://github.com/qwd/LocationList/blob/master/China-City-List-latest.csv 找到
# 例如，北京的ID是 "101010100"
USER_CITY_ID = "" 
# 天气更新频率（单位：毫秒），例如每小时更新一次
WEATHER_UPDATE_INTERVAL = 60 * 60 * 1000