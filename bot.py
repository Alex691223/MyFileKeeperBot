import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from config import BOT_TOKEN
from handlers import admin, group
from database import init_db

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(admin.router)
dp.include_router(group.router)

# 🔘 Команды Telegram
async def set_commands():
    commands = [
        BotCommand(command="admin", description="Открыть админ-панель"),
        BotCommand(command="broadcast", description="Начать рассылку"),
        BotCommand(command="kick", description="Кик пользователя"),
        BotCommand(command="ban", description="Бан пользователя"),
        BotCommand(command="unban", description="Разбан"),
        BotCommand(command="mute", description="Мут пользователя"),
        BotCommand(command="unmute", description="Снять мут"),
    ]
    await bot.set_my_commands(commands)

# 🚀 Запуск
async def main():
    print("📁 Инициализация базы данных...")
    await init_db()
    print("✅ База готова.")
    await set_commands()
    print("🤖 Бот запущен.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
