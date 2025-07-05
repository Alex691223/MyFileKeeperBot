import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from config import BOT_TOKEN
from handlers import admin

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

dp.include_router(admin.router)

async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
