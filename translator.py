from deep_translator import GoogleTranslator
from langdetect import detect

SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "ta": "Tamil",
    "kn": "Kannada",
    "mr": "Marathi",
    "gu": "Gujarati",
    "bn": "Bengali",
    "pa": "Punjabi",
}

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def translate_to_english(text):
    # Don't translate if text is too short (less than 5 characters)
    if len(text.strip()) < 5:
        return text, "en"
    try:
        lang = detect_language(text)
        # Only translate if confidence is high — skip rare/unknown langs
        if lang not in SUPPORTED_LANGUAGES:
            return text, "en"
        if lang == "en":
            return text, "en"
        translated = GoogleTranslator(source=lang, target="en").translate(text)
        return translated, lang
    except:
        return text, "en"

def translate_from_english(text, target_lang):
    if target_lang == "en":
        return text
    return GoogleTranslator(source="en", target=target_lang).translate(text)