from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboard import main_kb

router = Router()

@router.message(Command("mute"))
async def mute_handler(message: Message):
    await message.answer("Введите ID пользователя, чтобы замутить. (Функционал заглушка)")

@router.message(Command("ban"))
async def ban_handler(message: Message):
    await message.answer("Введите ID пользователя, чтобы забанить. (Функционал заглушка)")

@router.message(Command("kick"))
async def kick_handler(message: Message):
    await message.answer("Введите ID пользователя, чтобы кикнуть. (Функционал заглушка)")

@router.message(Command("stats"))
async def stats_handler(message: Message):
    await message.answer("Статистика групп и пользователей в разработке.")

@router.message(Command("broadcast"))
async def broadcast_handler(message: Message):
    await message.answer("Рассылка сообщений всем группам. (Требуется реализация)")
