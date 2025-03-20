import requests
import os
import datetime

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city, language="en", day_offset=0):
    """ Retrieve weather forecast for a given city and date offset (0=today, 1=tomorrow, etc.) """
    if not WEATHER_API_KEY:
        raise ValueError("Missing OpenWeatherMap API key. Set the environment variable OPENWEATHER_API_KEY.")

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric&lang={language}"
    
    response = requests.get(url)
    if response.status_code != 200:
        return None

    data = response.json()
    forecast_list = data["list"]
    
    forecast_day = datetime.datetime.now() + datetime.timedelta(days=day_offset)
    forecast_str = forecast_day.strftime("%Y-%m-%d")

    forecast = next((item for item in forecast_list if forecast_str in item["dt_txt"]), None)
    if not forecast:
        return None

    weather_desc = forecast["weather"][0]["description"]
    temp = forecast["main"]["temp"]

    return f"{weather_desc.capitalize()}, {temp}°C ({'today' if day_offset == 0 else 'tomorrow'})"
