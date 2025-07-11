import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault

from config import BOT_TOKEN
from database.models import init_db
from handlers import start, chat

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


async def setup_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="🌐 Change language / Сменить язык"),
        BotCommand(command="help", description="ℹ️ Help information"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())

    await bot.set_my_description("")  # Удалим описание
    await bot.set_my_short_description("")


async def main():
    init_db()

    dp.include_routers(
        start.router,
        chat.router
    )

    await setup_bot_commands(bot)

    print("✅ Бот запущен и готов к работе.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
