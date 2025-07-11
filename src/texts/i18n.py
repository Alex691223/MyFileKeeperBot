translations = {
    "choose_language": {
        "Русский": "Выберите язык:",
        "Deutsch": "Sprache auswählen:",
        "English": "Choose a language:"
    },
    "agree_prompt": {
        "Русский": "Пожалуйста, согласитесь с условиями перед использованием.",
        "Deutsch": "Bitte stimmen Sie den Bedingungen zu, bevor Sie fortfahren.",
        "English": "Please agree to the terms before using."
    },
    "rules_text": {
        "Русский": "Перед использованием вы должны согласиться с условиями использования. Здесь может быть ссылка или текст.",
        "Deutsch": "Bevor Sie fortfahren, müssen Sie den Nutzungsbedingungen zustimmen. Hier könnte ein Link stehen.",
        "English": "Before using the bot, you must agree to the terms of use. Insert link or text here."
    }
}


def t(key: str, lang: str) -> str:
    # Найдём текст по ключу и языку, или вернем английскую версию
    return translations.get(key, {}).get(lang, translations.get(key, {}).get("English", ""))
