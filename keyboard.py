from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📢 Рассылка"))
    kb.add(KeyboardButton("📊 Статистика"))
    kb.add(KeyboardButton("🔨 Мут"))
    kb.add(KeyboardButton("❌ Бан"))
    kb.add(KeyboardButton("👢 Кик"))
    return kb
