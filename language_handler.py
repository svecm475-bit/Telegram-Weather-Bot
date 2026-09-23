import json

PATH = "data/language.json"

def load_languages():
    try:
        with open(PATH, encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        print(e)
        data = {}

    return data

