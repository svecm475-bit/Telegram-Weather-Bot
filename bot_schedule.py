import json
import threading
import time
from datetime import datetime, timedelta
from gemini_api import ask_gemini
from load_api_keys import get_openweather_api
from user_data import get_user_language

import requests
import schedule

TIME = "06:00"

def get_latlon(city, country_code):
    api_key = get_openweather_api()
    if not city:
        print("You have to type a city")
        return None, None

    url = f"http://api.openweathermap.org/geo/1.0/direct?"

    if country_code != "-":
        url += f"q={city},{country_code}&limit=1&appid={api_key}"
    else:
        url += f"q={city}&limit=1&appid={api_key}"

    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        if data:
            lon = data[0]["lon"]
            lat = data[0]["lat"]
            return lat, lon
        else:
            return None, None
    else:
        print(f"Error:[{res.status_code}]")
    return None, None

def get_weather_text(city_name, country_code):
    api_key = get_openweather_api()

    lat, lon = get_latlon(city_name, country_code)

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"

    res = requests.get(url)
    text = ""
    if res.status_code == 200:
        data = res.json()
        for idx in range(0, 6):
            hour = (datetime.now() + timedelta(hours=idx * 3)).strftime("%H:00")
            tomorrow_data = data["list"][idx]
            temp = tomorrow_data['main']['temp']
            desc = tomorrow_data["weather"][0]["description"]
            text += f"{hour} {temp:.2f}°C, {desc};"
    return text

def bot_message(bot):
    try:
        with open("data/user_data.json", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError) as er:
        print(er)
    for user, value in data.items():
        if value.get("notify"):
            lang = get_user_language(user)
            text = get_weather_text(value.get("city_name"), value.get("country_code"))
            bot.send_message(int(user), ask_gemini(text, lang), parse_mode="HTML")

def notify(bot):
    schedule.every().day.at(TIME).do(bot_message, bot=bot)
    while True:
        schedule.run_pending()
        time.sleep(30)


def start_thread(bot):
    threading.Thread(target=notify, args=(bot,)).start()
