from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from services.personas import personas

def persona_keyboard() -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text=name, callback_data=f"persona:{name}")] for name in personas]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
