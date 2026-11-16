import os
import sys
import requests
from dotenv import load_dotenv

# 加载 .env 配置文件
load_dotenv()

# 读取环境变量，设置默认值
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "太原")
TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "20"))
DEMO_API_KEY = os.getenv("DEMO_API_KEY", "demo_xxxx")  # 实训保留字段，不实际使用

# 内置支持城市列表
SUPPORT_CITY = ["太原", "北京", "上海", "广州", "深圳", "杭州", "南京", "成都", "重庆", "西安"]

def get_weather(city: str) -> dict:
    """获取实时天气"""
    if city not in SUPPORT_CITY:
        raise ValueError(f"暂不支持【{city}】，可选城市：{', '.join(SUPPORT_CITY)}")

    # wttr.in接口，返回json，中文城市
    url = f"https://wttr.in/{city}?format=j1"
    try:
        resp = requests.get(url, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        raise RuntimeError(f"网络请求失败: {e}") from e

    current = data["current_condition"][0]
    return {
        "city": city,
        "temp": current["temp_C"],
        "wind": current["windspeedKmph"],
        "time": current["observation_time"],   # ✅ 修改这里！
        "weather_desc": current["weatherDesc"][0]["value"]
    }

def main() -> None:
    # 命令行参数：python weather_cli.py 城市名
    if len(sys.argv) >= 2:
        city = sys.argv[1]
    else:
        city = DEFAULT_CITY

    w = get_weather(city)
    print(f"{w['city']} 当前天气：{w['weather_desc']}")
    print(f"温度：{w['temp']} ℃  风速：{w['wind']} km/h")
    print(f"观测时间：{w['time']}")

if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError) as err:
        print(f"[错误] {err}")
        sys.exit(1)