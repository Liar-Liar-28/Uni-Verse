# main.py
import json
from googletrans import Translator

# Load slang dictionary
with open("slangs.json", "r") as f:
    slang_dict = json.load(f)

translator = Translator()

def handle_slangs(text):
    words = text.split()
    return " ".join([slang_dict.get(w.lower(), w) for w in words])

def translate_text(text, dest_lang):
    text = handle_slangs(text)
    translated = translator.translate(text, dest=dest_lang)
    return translated.text

if __name__ == "__main__":
    print("Welcome to Uni-Verse Translator!")
    text = input("Enter text: ")
    dest_lang = input("Enter target language code (e.g., 'en', 'hi', 'mr', 'gu'): ")
    result = translate_text(text, dest_lang)
    print(f"Translated Text: {result}")
