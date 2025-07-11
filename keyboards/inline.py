from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_persona_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="🧠 Философ", callback_data="persona_философ")],
        [InlineKeyboardButton(text="😼 Кот", callback_data="persona_кот")],
        [InlineKeyboardButton(text="🎒 Школьник", callback_data="persona_школьник")],
        [InlineKeyboardButton(text="🧢 Гопник", callback_data="persona_гопник")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
