from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
import asyncio
from config import BOT_TOKEN
from handlers import user, group, admin
from middlewares.user_agreement import AgreementMiddleware
from database import init_db

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

dp.message.middleware(AgreementMiddleware())
dp.include_routers(user.router, group.router, admin.router)

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
