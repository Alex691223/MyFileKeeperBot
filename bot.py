import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, ParseMode
from aiogram.filters import Command
from handlers import user, admin
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set in .env file")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Подключаем роутеры
dp.include_routers(user.router, admin.router)

async def set_commands():
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="mute", description="Заблокировать пользователя"),
        BotCommand(command="ban", description="Забанить пользователя"),
        BotCommand(command="kick", description="Кикнуть пользователя"),
        BotCommand(command="stats", description="Статистика")
    ]
    await bot.set_my_commands(commands)

async def main():
    await set_commands()
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
