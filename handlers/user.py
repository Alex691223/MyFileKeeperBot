from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, Text
from keyboard import main_kb

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Привет! Я модератор бот. Используй меню кнопок для команд.",
        reply_markup=main_kb()
    )

@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "/mute - Замутить пользователя\n"
        "/ban - Забанить пользователя\n"
        "/kick - Кикнуть пользователя\n"
        "/stats - Показать статистику"
    )

@router.message(Text(text=["📢 Рассылка", "📊 Статистика", "🔨 Мут", "❌ Бан", "👢 Кик"]))
async def buttons_handler(message: Message):
    text = message.text
    if text == "📢 Рассылка":
        await message.answer("Рассылка - доступна только для админов.")
    elif text == "📊 Статистика":
        await message.answer("Показ статистики в разработке.")
    elif text == "🔨 Мут":
        await message.answer("Для мутирования используйте команду /mute.")
    elif text == "❌ Бан":
        await message.answer("Для бана используйте команду /ban.")
    elif text == "👢 Кик":
        await message.answer("Для кика используйте команду /kick.")
    else:
        await message.answer("Команда не распознана.")
