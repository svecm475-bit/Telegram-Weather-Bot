import os

from dotenv import load_dotenv

load_dotenv(dotenv_path="data/api_keys.env")

def get_gemini_api():
    gemini_key = os.getenv("GEMINI")
    return gemini_key

def get_openweather_api():
    openweather_key = os.getenv("OPENWEATHER")
    return openweather_key

def get_bot_key():
    bot_key = os.getenv("TELEBOT")
    return bot_key