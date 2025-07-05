import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
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
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from config import BOT_TOKEN
from handlers import admin, group

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

dp.include_router(admin.router)
dp.include_router(group.router)

async def set_commands():
    commands = [
        BotCommand(command="admin", description="Открыть админ-панель"),
        BotCommand(command="stats", description="Статистика"),
        BotCommand(command="sendto", description="Отправить сообщение в группу"),
        BotCommand(command="kick", description="Кик пользователя"),
        BotCommand(command="ban", description="Бан пользователя"),
        BotCommand(command="unban", description="Разбан"),
        BotCommand(command="mute", description="Мут пользователя"),
        BotCommand(command="unmute", description="Снять мут"),
    ]
    await bot.set_my_commands(commands)

async def main():
    print("Бот запущен")
    await set_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
