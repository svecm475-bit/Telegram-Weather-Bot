import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from language_handler import load_languages
import load_api_keys

class KnightWeatherAdvice(BaseModel):
    greeting: str = Field(description="Noble knightly greeting with emojis ⚔️")
    forecast_summary: str = Field(description="A very short overall weather summary in 1 or two"
                                              "sentence with ONE fitting weather emoji and average temperature for the day (e.g. '☀️ Today will be warm and sunny"
                                              " throughout the realm' or '🌧️ Expect rain and cold winds, ready thy cloak').")
    gear_advice: str = Field(description="Advice on armor/cloak and umbrella/shield")
    parting_words: str = Field(description="Inspirational closing knightly words")


client = genai.Client(api_key=load_api_keys.get_gemini_api())
translation = load_languages()

def ask_gemini(weather_info_string: str, lang):
    match lang:
        case "ru":
            lang_full = "Russian"
        case "en":
            lang_full = "English"
        case "de":
            lang_full = "German"
        case "da":
            lang_full = "Danish"
        case "uk":
            lang_full = "Ukrainian"
        case _:
            lang_full = "English"
    try:
        chat = client.chats.create(
            model="gemini-3.5-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=f"""
                    You are a wise and noble medieval knight-advisor in a fantasy realm.
                    Your task is to analyze the provided weather forecast string and convert it into a heroic guide in {lang_full}.
                    
                    STRICT EMOJI RULES:
                    Map every weather condition to a matching emoji:
                    - Clear sky / sunny: ☀️
                    - Few / scattered clouds: 🌤️ or ⛅
                    - Overcast / clouds: ☁️
                    - Rain / showers: 🌧️ or 🌦️
                    - Thunderstorm: 🌩️
                    """,
                response_mime_type="application/json",
                response_schema=KnightWeatherAdvice,
                temperature=0.3,
            )
        )

        response = chat.send_message(f"Forecast data: {weather_info_string}")

        data = json.loads(response.text)

        return (
            f"{data['greeting']}\n\n"
            f"📜 <b>{translation[lang]["gemini"]["realm_forecast"]}</b>\n{data["forecast_summary"]}\n\n"
            f"🛡️ <b>{translation[lang]["gemini"]["gear_advice"]}</b>\n{data["gear_advice"]}\n\n"
            f"⚔️ <i>{data["parting_words"]}</i>"
        )
    except Exception as e:
        print(f"[Gemini Error]: {e}")
        return f"⚔️ <i>{translation[lang]["gemini"]["gemini_error_text"]}</i>"