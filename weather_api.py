from telebot import types

import requests
import text_decoration as stickers
import language_handler

from user_data import get_user_language
from load_api_keys import get_openweather_api
from datetime import datetime, timedelta

data = language_handler.load_languages()

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

def prozess_forecast_weather(bot, callback, city_name, country_code, hours):
    api_key = get_openweather_api()
    now = datetime.now()

    time = now + timedelta(hours=hours)
    hours_for_data = int(hours / 3)

    lat, lon = get_latlon(city_name, country_code)
    if lat is None and lon is None:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Try Again", callback_data="City"))
        bot.send_message(callback.message.chat.id, "City was not found", reply_markup=markup)
        return

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"

    res = requests.get(url)

    if res.status_code == 200:
        data_w = res.json()
        tomorrow_data = data_w["list"][hours_for_data]
        display_weather(bot, callback, tomorrow_data, city_name, time)

def get_markup_for_weather(callback):
    user_id = callback.from_user.id
    lang = get_user_language(user_id)
    # Localization
    markup_data = data[lang]["markup_weather"]
    now_button_text = markup_data["now_button_text"]
    tomorrow_button_text = markup_data["tomorrow_button_text"]
    menu_button_text = markup_data["menu_button_text"]

    now = datetime.now()
    now_3h = (now + timedelta(hours=3)).strftime("%H:00")
    now_6h = (now + timedelta(hours=6)).strftime("%H:00")
    now_9h = (now + timedelta(hours=9)).strftime("%H:00")
    now_12h = (now + timedelta(hours=12)).strftime("%H:00")
    now_15h = (now + timedelta(hours=15)).strftime("%H:00")
    now_18h = (now + timedelta(hours=18)).strftime("%H:00")
    now_21h = (now + timedelta(hours=21)).strftime("%H:00")

    markup = types.InlineKeyboardMarkup()
    now_button = types.InlineKeyboardButton(now_button_text, callback_data="Weather now")
    tomorrow_button = types.InlineKeyboardButton(tomorrow_button_text, callback_data="Weather tomorrow")
    menu_button = types.InlineKeyboardButton(f"{menu_button_text} 🏕️", callback_data='Menu')

    now_3h_button = types.InlineKeyboardButton(text=f"{now_3h}", callback_data="Weather 3h")
    now_6h_button = types.InlineKeyboardButton(text=f"{now_6h}", callback_data="Weather 6h")
    now_9h_button = types.InlineKeyboardButton(text=f"{now_9h}", callback_data="Weather 9h")
    now_12h_button = types.InlineKeyboardButton(text=f"{now_12h}", callback_data="Weather 12h")
    now_15h_button = types.InlineKeyboardButton(text=f"{now_15h}", callback_data="Weather 15h")
    now_18h_button = types.InlineKeyboardButton(text=f"{now_18h}", callback_data="Weather 18h")
    now_21h_button = types.InlineKeyboardButton(text=f"{now_21h}", callback_data="Weather 21h")

    markup.add(menu_button)
    markup.add(now_button, tomorrow_button)
    markup.row(now_3h_button, now_6h_button, now_9h_button)
    markup.row(now_12h_button, now_15h_button, now_18h_button, now_21h_button)

    return markup

def display_weather(bot, callback, data_w, city, time):
    lang = get_user_language(callback.from_user.id)
    temp_text = data[lang]["display_weather"]
    now = datetime.now()
    now_day = now.strftime("%d")
    time_day = time.strftime("%d")
    if now_day == time_day:
        pass
    time = time.strftime("%h %d | %H:00")
    #Markup with buttons
    markup = get_markup_for_weather(callback)
    # Display message
    temp = data_w['main']['temp']
    desc = data_w["weather"][0]["description"]
    desc_text = data[lang]["desc"][desc]
    temp_sticker = stickers.process_temp_stickers(temp)
    bot.send_message(callback.message.chat.id, f"🏠 <b><u>{city}</u></b>, {time}\n🌡 {temp_text} {temp}°C {temp_sticker}\n{desc_text}", reply_markup=markup, parse_mode="HTML")