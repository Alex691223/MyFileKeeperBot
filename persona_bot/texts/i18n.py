
translations = {
    "start_choose_lang": {
        "en": "🌐 Choose your language:",
        "de": "🌐 Wähle deine Sprache:",
        "ru": "🌐 Выберите язык:",
        "uk": "🌐 Оберіть мову:",
        "es": "🌐 Elige tu idioma:"
    },
    "agree_prompt": {
        "en": "Before using the bot, you must agree to the terms.",
        "de": "Bevor du den Bot nutzt, musst du den Bedingungen zustimmen.",
        "ru": "Перед использованием бота вы должны принять условия.",
        "uk": "Перш ніж користуватися ботом, потрібно прийняти умови.",
        "es": "Antes de usar el bot, debes aceptar los términos."
    },
    "agree_button": {
        "en": "I agree",
        "de": "Ich stimme zu",
        "ru": "Я согласен",
        "uk": "Я погоджуюсь",
        "es": "Estoy de acuerdo"
    }
}

def t(key, lang='en'):
    return translations.get(key, {}).get(lang, translations[key]['en'])
