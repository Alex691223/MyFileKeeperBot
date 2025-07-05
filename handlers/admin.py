from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_all_users


from aiogram import Router, types
from aiogram.filters.command import Command
from config import ADMIN_ID

router = Router()

@router.message(Command("stats"))
async def stats(message: types.Message):
    print(f"Команда /stats от {message.from_user.id}")
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("Статистика: Пользователей: 10, Групп: 5")

@router.message(Command("sendto"))
async def send_to_group(message: types.Message):
    print(f"Команда /sendto от {message.from_user.id}")
    if message.from_user.id != ADMIN_ID:
        return
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer("Использование: /sendto <group_id> <сообщение>")
        return
    group_id = args[1]
    text = args[2]
    try:
        await message.bot.send_message(chat_id=int(group_id), text=text)
        await message.answer("Сообщение отправлено.")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")
