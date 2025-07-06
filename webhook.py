import os
from flask import Flask, request
from bot import get_app

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/{TOKEN}"
app = Flask(__name__)
tg_app = get_app()

@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    await tg_app.update_queue.put(await tg_app._parse_webhook_update(request))
    return "ok"

@app.before_first_request
async def setup_webhook():
    url = os.getenv("WEBHOOK_URL")
    if url:
        await tg_app.bot.set_webhook(f"{url}/{TOKEN}")

if __name__ == "__main__":
    tg_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        webhook_url=f"{os.getenv('WEBHOOK_URL')}/{TOKEN}"
    )
