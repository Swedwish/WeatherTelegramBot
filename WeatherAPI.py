import datetime
import json
from types import SimpleNamespace
from typing import Final
import requests

with open('myTokens.json') as json_file:
    data = json.load(json_file)

WEATHER_TOKEN: Final = data.get("weatherToken", None)
UNITS="metric"

def get_weather(city_name, WEATHER_TOKEN = WEATHER_TOKEN, lang = "en", UNITS=UNITS):
    city_params = {
        "q":city_name,
        "limit":1,
        "appid":WEATHER_TOKEN
    }
    city_response = requests.get("https://api.openweathermap.org/geo/1.0/direct", params=city_params)
    city_data = json.loads(city_response.text, object_hook=lambda d: SimpleNamespace(**d))
    
    wheather_params = {
        "lon":city_data[0].lon,
        "lat":city_data[0].lat,
        "lang":lang,
        "units":UNITS,
        "appid":WEATHER_TOKEN
    }
    
    wheather_response = requests.get("https://api.openweathermap.org/data/2.5/forecast",wheather_params)
    wheather_data = json.loads(wheather_response.text, object_hook=lambda d: SimpleNamespace(**d))
    result = ""
    skip = False
    for timestamp in wheather_data.list:
        if skip:
            skip = False
            continue
        date = datetime.datetime.fromtimestamp(timestamp.dt)
        temperature = timestamp.main.temp
        weather_description = timestamp.weather[0].description
        cloudness = timestamp.clouds.all
        wind_speed = timestamp.wind.speed
        if lang == "ru":
            result += f"""{date.strftime("%A, %B %d, %Y %H:%M")}
            Температура:{temperature} градусов цельсия,
            Погодные условия:{weather_description}, облачность:{cloudness}%
            Скорость ветра: {wind_speed} м/c.\n\n"""
        else:
            result += f"""{date.strftime("%A, %B %d, %Y %H:%M")}
            Temperature:{temperature} celsium,
            Weather description:{weather_description}, cloudness:{cloudness}%
            Wind speed:{wind_speed} m/s.\n\n"""
        skip = True
    return result

#print(get_weather(city_name="Новосибирск", lang="ru"))