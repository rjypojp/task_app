import requests



def get_holidays():
    res = requests.get(
        "https://holidays-jp.github.io/api/v1/date.json"
    )
    
    holiday_data = res.json()
    
    holidays = [
        {
            "title": name,
            "start": date,
            "color": "red"
        }
        for date, name in holiday_data.items()
    ]
    
    return holidays