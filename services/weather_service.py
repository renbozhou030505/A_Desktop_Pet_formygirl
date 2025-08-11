# services/weather_service.py
import requests
import logging
from typing import Union
# 获取一个专门用于此模块的日志记录器
logger = logging.getLogger(__name__)

# 和风天气API的URL是固定的，不需要修改
NOW_WEATHER_API_URL = "https://n44t2avku8.re.qweatherapi.com/v7/weather/now"

def get_current_weather(api_key: str, city_id: str) -> Union[dict, None]:
    """
    通过和风天气API获取指定城市的实时天气信息。

    Args:
        api_key (str): 和风天气的API Key。
        city_id (str): 城市的Location ID。

    Returns:
        dict | None: 如果成功，返回包含天气信息的字典；如果失败，返回None。
    """
    # 构建请求参数
    params = {
        'key': api_key,
        'location': city_id,
        'lang': 'zh',  # 返回语言为中文
        'unit': 'm'    # 使用公制单位（温度：摄氏度）
    }
    
    try:
        # 发起GET请求，设置10秒超时
        response = requests.get(NOW_WEATHER_API_URL, params=params, timeout=10)
        # 如果HTTP状态码是4xx或5xx，则主动引发异常
        response.raise_for_status()  
        
        data = response.json()
        
        # 检查API业务状态码是否为 '200' (表示成功)
        if data.get('code') == '200':
            weather_now = data.get('now', {})
            # 提取我们需要的信息，并整合成一个干净的字典返回
            processed_data = {
                "temp": weather_now.get('temp'),      # 当前温度
                "text": weather_now.get('text'),      # 天气状况文字，如“晴”、“多云”
                "windDir": weather_now.get('windDir'),# 风向
                "windScale": weather_now.get('windScale'), # 风力等级
                "humidity": weather_now.get('humidity') # 相对湿度
            }
            logger.info(f"成功获取天气数据: {processed_data}")
            return processed_data
        else:
            # 如果API返回业务错误（如Key无效、查询超额等）
            logger.error(f"天气API返回业务错误: code={data.get('code')}, message={response.text}")
            return None

    except requests.exceptions.RequestException as e:
        # 捕获所有requests相关的网络错误（如连接超时、DNS错误等）
        logger.error(f"请求天气API时发生网络错误: {e}")
        return None
    except Exception as e:
        # 捕获其他未知异常（如JSON解析失败等）
        logger.error(f"处理天气数据时发生未知错误: {e}")
        return None