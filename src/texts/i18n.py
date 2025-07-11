translations = {
    "start_choose_lang": {
        "Русский": "Выберите язык:",
        "Deutsch": "Wähle eine Sprache:",
        "English": "Choose a language:"
    },
    "agree_prompt": {
        "Русский": "Перед использованием подтвердите согласие с правилами.",
        "Deutsch": "Bitte bestätigen Sie die Nutzungsbedingungen.",
        "English": "Please agree to the terms before using."
    },
    "agree_button": {
        "Русский": "Согласен",
        "Deutsch": "Einverstanden",
        "English": "Agree"
    },
    "choose_persona": {
        "Русский": "Пожалуйста, укажите персонажа в сообщении (например, 'философ', 'кот', 'гопник'...).",
        "Deutsch": "Bitte gib eine Figur im Text an (z.B. 'Philosoph', 'Katze', 'Gopnik'...).",
        "English": "Please specify a character in your message (e.g., 'philosopher', 'cat', 'gopnik'...)."
    }
}


def t(key, lang="Русский"):
    """
    Возвращает перевод по ключу и языку. Если перевода нет, возвращает английский или сам ключ.
    """
    if key in translations and lang in translations[key]:
        return translations[key][lang]
    return translations.get(key, {}).get("English", key)
