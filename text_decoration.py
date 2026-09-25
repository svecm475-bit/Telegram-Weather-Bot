def temperature_to_str(temp):
    temp_str = ""
    match temp:
        case _ if temp < 0:
            temp_str = "freezing"
        case _ if 0 <= temp <= 15:
            temp_str = "cold"
        case _ if 15 < temp < 25:
            temp_str = "warm"
        case _ if temp >= 25:
            temp_str = "hot"
        case _:
            temp_str = "unknown"
    return temp_str

def process_temp_stickers(temp):
    temp_desc = temperature_to_str(temp)
    temp_sticker = ""
    match temp_desc:
        case _ if temp_desc == "freezing":
            temp_sticker = "🧊"
        case _ if temp_desc == "cold":
            temp_sticker = "🥶"
        case _ if temp_desc == "warm":
            temp_sticker = "☕"
        case _ if temp_desc == "hot":
            temp_sticker = "🔥"
    return temp_sticker

def get_time_of_day(time, lang):
    time_f = int(time.strftime("%H"))
    time_of_day = ""
    if lang == "en":
        if 12 >= time_f > 6:
            time_of_day = "<3 Good morning 🌅, traveler"
        elif 16 >= time_f > 12:
            time_of_day = "<3 Good day 🏢, traveler"
        elif 21 >= time_f > 16:
            time_of_day = "<3 Good evening 🌆, traveler"
        elif time_f > 21 or time_f <= 6:
            time_of_day = "<3 Good night 🌃, traveler"
        return time_of_day
    elif lang == "ru":
        if 12 >= time_f > 6:
            time_of_day = "<3 Доброе утро 🌅, странник"
        elif 16 >= time_f > 12:
            time_of_day = "<3 Добрый день 🏢, странник"
        elif 21 >= time_f > 16:
            time_of_day = "<3 Добрый вечер 🌆, странник"
        elif time_f > 21 or time_f <= 6:
            time_of_day = "<3 Доброй ночи 🌃, странник"
        return time_of_day
    elif lang == "uk":
        if 12 >= time_f > 6:
            time_of_day = "<3 Доброго ранку 🌅, мандрівнику"
        elif 16 >= time_f > 12:
            time_of_day = "<3 Доброго дня 🏙, мандрівнику"
        elif 21 >= time_f > 16:
            time_of_day = "<3 Доброго вечора 🌆, мандрівнику"
        elif time_f > 21 or time_f <= 6:
            time_of_day = "<3 Добраніч 🌌, мандрівнику"
        return time_of_day
    elif lang == "de":
        if 12 >= time_f > 6:
            time_of_day = "<3 Guten Morgen 🌅, Reisender"
        elif 16 >= time_f > 12:
            time_of_day = "<3 Guten Tag 🏙, Reisender"
        elif 21 >= time_f > 16:
            time_of_day = "<3 Guten Abend 🌆, Reisender"
        elif time_f > 21 or time_f <= 6:
            time_of_day = "<3 Gute Nacht 🌌, Reisender"
        return time_of_day
    elif lang == "da":
        if 12 >= time_f > 6:
            time_of_day = "<3 Godmorgen 🌅, rejsende"
        elif 16 >= time_f > 12:
            time_of_day = "<3 Goddag 🏙, rejsende"
        elif 21 >= time_f > 16:
            time_of_day = "<3 Godeften 🌆, rejsende"
        elif time_f > 21 or time_f <= 6:
            time_of_day = "<3 Godnat 🌌, rejsende"
        return time_of_day
    return "Hi"