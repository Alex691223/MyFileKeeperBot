import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import BotCommand

# Загружаем переменные окружения из .env файла
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # или вставь строку токена прямо сюда

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан! Установи переменную окружения или в .env файле.")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

async def set_commands():
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="mute", description="Заблокировать пользователя"),
        BotCommand(command="ban", description="Забанить пользователя"),
        BotCommand(command="kick", description="Выгнать пользователя"),
        # Добавляй свои команды сюда
    ]
    await bot.set_my_commands(commands)

async def main():
    await set_commands()
    # Здесь подключай роутеры и запускай поллинг
    from handlers import user, group, admin
    dp.include_router(user.router)
    dp.include_router(group.router)
    dp.include_router(admin.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен.")
