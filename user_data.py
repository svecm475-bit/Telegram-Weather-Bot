import json

PATH = "data/user_data.json"

def get_user_code_city_enabled(user_id):
    user_id = str(user_id)
    try:
       with open(PATH, "r", encoding="utf-8") as file:
           data = json.load(file)
           if user_id not in data:
               print("No user found")
               return None, None, None
           user_data = data[user_id]
           code = user_data["country_code"]
           city = user_data["city_name"]
           enabled = user_data["notify"]
           return code, city, enabled
    except (FileNotFoundError, json.decoder.JSONDecodeError) as er:
           print(er)
    return None, None, None

def update_user_settings(callback, city_name, country_code="-"):
    user_id = str(callback.from_user.id)

    try:
        with open(PATH, "r", encoding="utf-8") as readfile:
            data = json.load(readfile)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("File not found or its empty")
        data = {}

    if user_id not in data:
        data[user_id] = {
            "city_name": city_name,
            "country_code": country_code,
            "notify": False,
            "language": "en"
        }
    else:
        data[user_id]["city_name"] = city_name
        data[user_id]["country_code"] = country_code

    with open(PATH, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

def update_user_language(callback, language):
    user_id = str(callback.from_user.id)

    try:
        with open(PATH, "r", encoding="utf-8") as readfile:
            data = json.load(readfile)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("File not found or its empty")
        data = {}

    if user_id not in data:
        print("No user found")
        return

    data[user_id]["language"] = language

    with open(PATH, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

def get_user_language(user_id):
    user_id = str(user_id)
    try:
        with open(PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            if user_id not in data:
                print("No user found")
                return "en"
            language = data[user_id]["language"]
            return language
    except (FileNotFoundError, json.decoder.JSONDecodeError) as er:
        print(er)
    return "en"

def enable_disable_notifications(callback, boolean: bool):
    user_id = str(callback.from_user.id)
    try:
        with open(PATH, "r", encoding="utf-8") as readfile:
            data = json.load(readfile)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("File not found or its empty")
        data = {}

    if user_id not in data:
        return

    data[user_id]["notify"] = boolean

    with open(PATH, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

def get_country_code(country_name):
    cleaned_name = country_name.strip().lower()
    with open("data/country_codes.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    code = data.get(cleaned_name)
    if code:
        return code
    else:
        return "-"



