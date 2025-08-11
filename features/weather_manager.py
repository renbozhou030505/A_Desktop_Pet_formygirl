# features/weather_manager.py
from PyQt6.QtCore import QTimer
import logging

# 导入config模块以获取配置
import config
# 导入我们纯粹的服务模块
from services import weather_service

# 获取一个专门用于此模块的日志记录器
logger = logging.getLogger(__name__)

class WeatherManager:
    def __init__(self, pet_window):
        self.pet = pet_window
        self.current_weather = None # 用于存储最新的天气数据

        # 只有在config中开启了天气功能时，才启动管理器
        if config.WEATHER_ENABLED:
            self.weather_timer = QTimer(timeout=self.update_weather)
            
            # 启动时立即获取一次天气，然后按设定的间隔重复
            self.update_weather() 
            self.weather_timer.start(config.WEATHER_UPDATE_INTERVAL)
            logger.info("天气管理器已启动。")
    
    def update_weather(self):
        """定时从服务层获取天气数据并存储。"""
        logger.info("正在尝试更新天气数据...")
        # 从config中读取Key和城市ID，并传递给服务函数
        weather_data = weather_service.get_current_weather(
            config.WEATHER_API_KEY,
            config.USER_CITY_ID
        )
        if weather_data:
            self.current_weather = weather_data
            # 如果成功获取，可以检查一下是否需要根据天气让宠物说些什么
            self.check_weather_and_react()

    def check_weather_and_react(self):
        """(可选功能) 检查当前天气并让宠物做出一些自发的反应。"""
        if not self.current_weather:
            return

        # 将温度字符串转为整数，如果失败则默认为0
        try:
            temp = int(self.current_weather.get("temp", 0))
        except (ValueError, TypeError):
            temp = 0
            
        text = self.current_weather.get("text", "")

        # 简单的天气反应逻辑示例
        if "雨" in text:
            self.pet.show_message_and_interact("外面在下雨哦，主人出门的话千万别忘了带伞！", interact=False)
        elif temp > 30:
             self.pet.show_message_and_interact(f"今天好热呀，有{temp}度呢！主人要注意防暑哦。", interact=False)
        elif temp < 10:
             self.pet.show_message_and_interact(f"天气有点凉，只有{temp}度，主人要多穿一件衣服呀。", interact=False)

    def show_weather_to_user(self):
        """当用户请求时，格式化天气信息并通过气泡框显示。"""
        if self.current_weather:
            # 格式化显示给用户的消息
            message = (
                f"查询城市: 长沙\n"  # 可以硬编码或未来从config读取城市中文名
                f"天气: {self.current_weather['text']}\n"
                f"温度: {self.current_weather['temp']}°C\n"
                f"风向: {self.current_weather['windDir']} ({self.current_weather['windScale']}级)\n"
                f"湿度: {self.current_weather['humidity']}%"
            )
            # 让宠物用交互动作来显示天气，持续8秒
            self.pet.show_message_and_interact(message, duration=8000)
        else:
            # 如果没有获取到天气数据，给出友好提示
            self.pet.show_message_and_interact("哎呀，获取天气失败了...\n请检查网络或API Key配置哦。")