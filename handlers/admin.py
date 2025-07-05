from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import Command
from config import ADMIN_ID
from database import count_users, count_groups  # Предполагается, что у тебя есть такие функции

router = Router()

@router.message(Command("stats"))
async def stats(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    users = await count_users()
    groups = await count_groups()
    await message.answer(f"Пользователей: {users}\nГрупп: {groups}")

@router.message(F.text.startswith("/sendto"))
async def send_to_group(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        _, group_id, *msg = message.text.split()
        text = ' '.join(msg)
        await message.bot.send_message(chat_id=int(group_id), text=text)
        await message.answer("Сообщение отправлено.")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")
