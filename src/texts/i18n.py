# texts/i18n.py

def t(key, lang):
    try:
        return translations.get(key, {}).get(lang, translations[key]['English'])
    except KeyError:
        return "⚠️ Missing translation."

translations = {
    "agree_prompt": {
        "Русский": "Пожалуйста, ознакомьтесь и согласитесь с пользовательским соглашением:",
        "Deutsch": "Bitte lesen und akzeptieren Sie die Nutzungsbedingungen:",
        "English": "Please review and accept the user agreement:"
    },
    "rules_text": {
        "Русский": "Пользовательское соглашение: вы соглашаетесь использовать бота на свой страх и риск. Бот не хранит персональные данные. Все действия соответствуют законам Германии.",
        "Deutsch": "Nutzungsbedingungen: Sie verwenden den Bot auf eigenes Risiko. Der Bot speichert keine personenbezogenen Daten. Alle Aktionen entsprechen dem deutschen Recht.",
        "English": "User Agreement: You use the bot at your own risk. The bot does not store personal data. All actions comply with German law."
    },
    "choose_persona": {
        "Русский": "Выберите персонажа перед началом общения:",
        "Deutsch": "Wähle einen Charakter aus:",
        "English": "Choose a character before chatting:"
    },
    "language_chosen": {
        "Русский": "Язык успешно выбран: Русский",
        "Deutsch": "Sprache erfolgreich gewählt: Deutsch",
        "English": "Language selected successfully: English"
    },
    "persona_selected": {
        "Русский": "✅ Персонаж выбран: {persona}",
        "Deutsch": "✅ Charakter ausgewählt: {persona}",
        "English": "✅ Persona selected: {persona}"
    }
}
