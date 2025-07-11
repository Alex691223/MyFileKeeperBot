from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang:Русский"),
            InlineKeyboardButton(text="🇩🇪 Deutsch", callback_data="set_lang:Deutsch"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang:English"),
        ]
    ])

def agree_keyboard(lang: str) -> InlineKeyboardMarkup:
    text = {
        "Русский": "Согласен",
        "Deutsch": "Zustimmen",
        "English": "Agree"
    }.get(lang, "Agree")
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data="agree")]
    ])
