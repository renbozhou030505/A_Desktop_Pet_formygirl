# services/weather.py
import requests
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from utils.logger import get_logger

log = get_logger("WeatherService")

# 使用 wttr.in 的免费JSON API
WEATHER_API_URL = "https://wttr.in/?format=j1"

class WeatherWorker(QObject):
    """
    一个在后台线程工作的类，用于获取天气数据，避免UI卡顿。
    """
    finished = pyqtSignal(dict)  # 任务完成时发射信号，携带天气数据字典
    error = pyqtSignal(str)      # 任务出错时发射信号，携带错误信息

    def run(self):
        log.info("开始在后台获取天气数据...")
        try:
            response = requests.get(WEATHER_API_URL, timeout=10)
            response.raise_for_status()  # 如果HTTP状态码是4xx或5xx，则抛出异常
            weather_data = response.json()
            log.info("天气数据获取成功！")
            self.finished.emit(weather_data)
        except requests.exceptions.RequestException as e:
            log.error(f"网络请求失败: {e}")
            self.error.emit("网络连接好像出了点问题...")
        except Exception as e:
            log.error(f"处理天气数据时发生未知错误: {e}", exc_info=True)
            self.error.emit("获取天气的时候遇到了奇怪的错误...")

def get_weather_async(on_success, on_error):
    """
    异步获取天气的主函数。
    :param on_success: 成功时调用的回调函数，会接收一个格式化好的字符串。
    :param on_error: 失败时调用的回调函数，会接收一个错误字符串。
    """
    thread = QThread()
    worker = WeatherWorker()
    worker.moveToThread(thread)

    def process_data(data):
        try:
            current = data['current_condition'][0]
            area = data['nearest_area'][0]['areaName'][0]['value']
            
            weather_desc = current['weatherDesc'][0]['value']
            temp_c = current['temp_C']
            feels_like_c = current['FeelsLikeC']
            
            # 格式化成易于阅读的字符串
            formatted_string = f"主人好！\n{area}今天天气{weather_desc}，\n当前温度{temp_c}°C，体感{feels_like_c}°C哦。"
            on_success(formatted_string)
        except (KeyError, IndexError) as e:
            log.error(f"解析天气数据格式时出错: {e}")
            on_error("天气数据格式有点奇怪，看不懂了...")
        finally:
            thread.quit()

    def handle_error(error_message):
        on_error(error_message)
        thread.quit()

    worker.finished.connect(process_data)
    worker.error.connect(handle_error)
    thread.started.connect(worker.run)
    
    # 清理工作
    thread.finished.connect(thread.deleteLater)
    worker.finished.connect(worker.deleteLater)
    worker.error.connect(worker.deleteLater)
    
    thread.start()
    
    # 将thread对象返回或存储，以防止被垃圾回收
    return thread