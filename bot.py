import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import base, shop, games
from database import setup_database

BOT_TOKEN = "7402843316:AAEN65krpQ2saH7ZJxDm1cZb4cPgzoIJ3b4"

async def main():
    await setup_database()
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(base.router)
    dp.include_router(shop.router)
    dp.include_router(games.router)

    await bot.set_my_commands([
        BotCommand(command="start", description="Начать"),
        BotCommand(command="profile", description="Профиль"),
        BotCommand(command="daily", description="Получить ежедневный бонус"),
        BotCommand(command="shop", description="Магазин наград"),
        BotCommand(command="top", description="Топ пользователей"),
        BotCommand(command="casino", description="🎰 Казино"),
        BotCommand(command="guess", description="🎯 Угадай число"),
    ])

    print("✅ Бот запущен.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
