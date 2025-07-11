import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # 🔥 добавляем путь

import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import start, chat
from database.models import init_db

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(chat.router)

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
