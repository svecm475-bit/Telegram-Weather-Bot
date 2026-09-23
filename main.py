from datetime import datetime

import telebot
from telebot import types

import bot_schedule as schedule
import text_decoration as stickers
import user_data as usr
import weather_api as weather
from language_handler import load_languages
from load_api_keys import get_bot_key

bot_key = get_bot_key()

bot = telebot.TeleBot(bot_key)

if __name__ == '__main__':
    schedule.start_thread(bot)

    data = load_languages()


def process_city(message, lang):
    enter_city = data[lang]["enter_city"]
    cheek_slap_text = enter_city["cheek_slap_text"]
    skip_button_text = enter_city["skip_button_text"]
    type_country_text = enter_city["type_country_text"]
    or_skip_text = enter_city["or_skip_text"]
    menu_button_text = data[lang]["markup_weather"]["menu_button_text"]

    if not message.text:
        markup = types.InlineKeyboardMarkup()
        menu_button = types.InlineKeyboardButton(f"{menu_button_text} 🏕️", callback_data="Menu")
        markup.add(menu_button)
        bot.send_message(message.chat.id, cheek_slap_text, reply_markup=markup)
        return
    city_name = message.text.strip()

    markup = types.InlineKeyboardMarkup()
    skip_button = types.InlineKeyboardButton(skip_button_text, callback_data=f"Skip:{city_name}")
    markup.add(skip_button)

    msg = bot.send_message(message.chat.id,
                           f"{type_country_text} 🏰<u><b> {city_name} </b></u>🏰, {or_skip_text}",
                           reply_markup=markup, parse_mode="HTML")

    bot.register_next_step_handler(msg, process_country, city_name, lang)

def process_country(message, city_name, lang):
    menu_button_text = data[lang]["markup_weather"]["menu_button_text"]
    cheek_slap_text = data[lang]["enter_city"]["cheek_slap_text"]
    if not message.text:
        markup = types.InlineKeyboardMarkup()
        menu_button = types.InlineKeyboardButton(f"{menu_button_text} 🏕️", callback_data="Menu")
        markup.add(menu_button)
        bot.send_message(message.chat.id, cheek_slap_text, reply_markup=markup)
        return
    country_name = message.text.strip()

    usr.update_user_settings(message, city_name, country_name)

    menu(message)

@bot.message_handler(commands=["start", "menu"])
def menu(message, lang="-", text=""):
    # Language processing
    if lang == "-":
        lang = usr.get_user_language(message.from_user.id)

    menu_text = data[lang]["main_menu"]

    # Text localization for buttons and messages
    welcome_text = f"{menu_text["welcome_text"]}\n{text}"
    enable_notification_text = menu_text["enable_notification_button_text"]
    change_city_text = menu_text["city_button_text"]
    show_weather_text = menu_text["show_weather_button_text"]

    # Markup with buttons
    markup = types.InlineKeyboardMarkup()
    enable_notification_button = types.InlineKeyboardButton(enable_notification_text, callback_data="Notification")
    city_button = types.InlineKeyboardButton(change_city_text, callback_data='City')
    show_weather_button = types.InlineKeyboardButton(show_weather_text, callback_data='Weather')
    en_button = types.InlineKeyboardButton("EN", callback_data="EN")
    ru_button = types.InlineKeyboardButton("RU", callback_data="RU")
    uk_button = types.InlineKeyboardButton("UK", callback_data="UK")
    de_button = types.InlineKeyboardButton("DE", callback_data="DE")
    da_button = types.InlineKeyboardButton("DA", callback_data="DA")

    markup.add(city_button)
    markup.add(enable_notification_button)
    markup.row(en_button, de_button, da_button, uk_button, ru_button)
    markup.row(show_weather_button)
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    bot.answer_callback_query(callback.id)
    lang = usr.get_user_language(callback.from_user.id)
    # Main menu
    if callback.data == "Menu":
        menu(callback.message, lang)
    elif callback.data == "City":
        msg = bot.send_message(callback.message.chat.id, data[lang]["enter_city"]["enter_city_text"])
        bot.register_next_step_handler(msg, process_city, lang)
    # Enable/Disable user notification
    elif callback.data == "Notification":
        _, _, enabled = usr.get_user_code_city_enabled(callback.from_user.id)
        if enabled is None:
            return
        if enabled:
            enabled_text = data[lang]["notification"]["notification_disabled_text"]
            usr.enable_disable_notifications(callback, False)
            menu(callback.message, lang, enabled_text)
        else:
            disabled_text = data[lang]["notification"]["notification_enabled_text"]
            usr.enable_disable_notifications(callback, True)
            menu(callback.message, lang, disabled_text)
    # Localization
    elif callback.data == "EN":
        if lang != "en":
            usr.update_user_language(callback, "en")
            menu(callback.message, "en")
    elif callback.data == "RU":
        if lang != "ru":
            usr.update_user_language(callback, "ru")
            menu(callback.message, "ru")
    elif callback.data == "UK":
        if lang != "uk":
            usr.update_user_language(callback, "uk")
            menu(callback.message, "uk")
    elif callback.data == "DE":
        if lang != "de":
            usr.update_user_language(callback, "de")
            menu(callback.message, "de")
    elif callback.data == "DA":
        if lang != "da":
            usr.update_user_language(callback, "da")
            menu(callback.message, "da")
    # Skip typing of country
    elif callback.data.startswith("Skip:"):
        city_name = callback.data.split(":")[1]
        bot.clear_step_handler_by_chat_id(callback.message.chat.id)
        usr.update_user_settings(callback, city_name, "-")
        menu(callback.message, lang)
    elif callback.data == "Weather":
        now = datetime.now()
        markup = weather.get_markup_for_weather(callback)
        bot.send_message(callback.message.chat.id, stickers.get_time_of_day(now, lang), reply_markup=markup)
    # Shows Weather now
    elif callback.data == "Weather now":
        code, city, _ = usr.get_user_code_city_enabled(callback.from_user.id)

        weather.prozess_forecast_weather(bot, callback, city, code, 0)
    # Shows Weather tomorrow
    elif callback.data == "Weather tomorrow":
        code, city, _ = usr.get_user_code_city_enabled(callback.from_user.id)

        weather.prozess_forecast_weather(bot, callback, city, code, 24)
    elif callback.data == "Weather 3h":
        code, city, _ = usr.get_user_code_city_enabled(callback.from_user.id)

        weather.prozess_forecast_weather(bot, callback, city, code, 3)
    elif callback.data == "Weather 6h":
        code, city, _ = usr.get_user_code_city_enabled(callback.from_user.id)

        weather.prozess_forecast_weather(bot, callback, city, code, 6)
    elif callback.data == "Weather 9h":
        code, city, _ = usr.get_user_code_city_enabled(callback.from_user.id)

        weather.prozess_forecast_weather(bot, callback, city, code, 9)
    elif callback.data == "Weather 12h":
        code, city, _ = usr.get_user_code_city_enabled(callback.from_user.id)

        weather.prozess_forecast_weather(bot, callback, city, code, 12)
    elif callback.data == "Weather 15h":
        code, city, _ = usr.get_user_code_city_enabled(callback.from_user.id)

        weather.prozess_forecast_weather(bot, callback, city, code, 15)
    elif callback.data == "Weather 18h":
        code, city, _ = usr.get_user_code_city_enabled(callback.from_user.id)

        weather.prozess_forecast_weather(bot, callback, city, code, 18)
    elif callback.data == "Weather 21h":
        code, city, _ = usr.get_user_code_city_enabled(callback.from_user.id)

        weather.prozess_forecast_weather(bot, callback, city, code, 21)

bot.polling(non_stop=True)