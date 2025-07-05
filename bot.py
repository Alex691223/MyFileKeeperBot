import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from handlers import user, group, admin  # твои роутеры

BOT_TOKEN = "7152364773:AAHhlKTUfQcoYz5myyxYm1FoPpzU9j-q9vU"

async def handle(request):
    return web.Response(text="OK")

async def start_webserver():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"HTTP server started on port {port}")

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_router(user.router)
    dp.include_router(group.router)
    dp.include_router(admin.router)

    await start_webserver()  # запускаем HTTP сервер
    await dp.start_polling(bot)  # запускаем бота

if __name__ == "__main__":
    asyncio.run(main())
