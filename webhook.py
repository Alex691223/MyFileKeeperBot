import os
from flask import Flask, request
from bot import get_app
import asyncio

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PATH = f"/{TOKEN}"

app = Flask(__name__)
tg_app = get_app()

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    # Обрабатываем update синхронно через asyncio.run
    update = tg_app.update_queue._loop.create_task(tg_app._parse_webhook_update(request))
    asyncio.get_event_loop().run_until_complete(update)
    asyncio.get_event_loop().create_task(tg_app.update_queue.put(update.result()))
    return "ok"

def set_webhook():
    if WEBHOOK_URL:
        asyncio.get_event_loop().run_until_complete(
            tg_app.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
        )

if __name__ == "__main__":
    set_webhook()
    tg_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
    )
