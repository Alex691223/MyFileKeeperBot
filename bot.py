import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault

from config import BOT_TOKEN
from database import init_db
from handlers import register_all_handlers

# Включаем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаём экземпляр бота
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Хранилище FSM
dp = Dispatcher(storage=MemoryStorage())


async def setup():
    # Инициализация БД
    init_db()

    # Установка команд
    await bot.set_my_commands([
        BotCommand(command="start", description="Перезапуск бота"),
        BotCommand(command="help", description="Справка и доступные команды"),
        BotCommand(command="panel", description="Вход в админ-панель"),
        BotCommand(command="info", description="Информация о вас"),
    ], scope=BotCommandScopeDefault())

    # Подключение всех роутеров
    register_all_handlers(dp)


async def main():
    await setup()
    logger.info("Запуск бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
