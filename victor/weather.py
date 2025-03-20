import requests
import os
import datetime
from config import WEATHER_API_KEY

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city, language="en", day_offset=0):
    """ Retrieve real-time or forecast weather for a given city. """
    if not WEATHER_API_KEY:
        raise ValueError("Missing OpenWeatherMap API key. Set the environment variable OPENWEATHER_API_KEY.")

    if day_offset == 0:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang={language}"
        date_label = "today"
    else:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric&lang={language}"
        date_label = f"in {day_offset} days"

    response = requests.get(url)
    if response.status_code != 200:
        print(f"⚠️ OpenWeatherMap API Error ({response.status_code}): {response.text}")
        return None

    data = response.json()

    if day_offset == 0:
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
    else:
        forecast_list = data["list"]
        forecast_day = datetime.datetime.now() + datetime.timedelta(days=day_offset)
        forecast_str = forecast_day.strftime("%Y-%m-%d")

        forecast = next((item for item in forecast_list if forecast_str in item["dt_txt"]), None)
        if not forecast:
            return None

        weather_desc = forecast["weather"][0]["description"]
        temp = forecast["main"]["temp"]

    return f"{weather_desc.capitalize()}, {temp}°C ({date_label})"

def generate_weather_intro(city, weather_info, language, is_high_altitude=False):
    """ Generate an introductory message based on weather conditions. """
    messages = {
        "en": {
            "default": f"The forecast for {city} is {weather_info}. Plan accordingly.",
            "altitude": f"The forecast for {city} is {weather_info}. Note that conditions might be colder and windier in high-altitude areas.",
            "rain": f"The forecast for {city} is {weather_info}. It might be best to plan indoor activities."
        },
        "fr": {
            "default": f"La météo prévue à {city} est {weather_info}. Planifiez en conséquence.",
            "altitude": f"La météo prévue à {city} est {weather_info}. Notez que les conditions peuvent être plus froides et venteuses en altitude.",
            "rain": f"La météo prévue à {city} est {weather_info}. Il est préférable de privilégier les activités en intérieur."
        }
    }

    if "rain" in weather_info.lower():
        return messages[language]["rain"]
    elif is_high_altitude:
        return messages[language]["altitude"]
    else:
        return messages[language]["default"]
