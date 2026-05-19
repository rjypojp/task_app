import requests
from datetime import datetime

WEEKDAYS = ["月", "火", "水", "木", "金", "土", "日"]
REQUEST_TIMEOUT = 10



def get_weather(city, api_key):
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={api_key}&units=metric&lang=ja"
    )
    
    weather_list = []
    weather = "取得失敗"
    temp = "-"
    
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        data = response.json()
        
        if data.get("cod") != "200":
            return weather, temp, weather_list
        
        for item in data["list"]:
            if "12:00:00" in item["dt_txt"]:
                
                dt = datetime.strptime(
                    item["dt_txt"],
                    "%Y-%m-%d %H:%M:%S"
                )
                
                weekday = WEEKDAYS[dt.weekday()]
                 
                if weekday =="土":
                     color = "blue"
                elif weekday == "日":
                     color = "red"
                else:
                    color = "black"
                    
                weather_list.append({
                    "date": item["dt_txt"],
                    "temp": item["main"]["temp"],
                    "description": item["weather"][0]["description"],
                    "icon": item["weather"][0]["icon"],
                    "weekday": weekday,
                    "color": color
                })
        
        first = data["list"][0]
        
        weather = first["weather"][0]["description"]
        temp = first["main"]["temp"]
    
    except Exception as e:
        print("天気取得エラー", e)
    return weather, temp, weather_list
        