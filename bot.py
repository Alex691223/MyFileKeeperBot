from pyrogram import Client
from threading import Thread
from flask import Flask
from config import API_ID, API_HASH, BOT_TOKEN

# 🧩 Имитация веб-сервера для Render
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "✅ Bot is running"

def run_flask():
    flask_app.run(host="0.0.0.0", port=5000)

# 🔁 Запуск Flask в отдельном потоке
Thread(target=run_flask).start()

# 🛠 Настройка Pyrogram бота
app = Client("moderator_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🔌 Регистрация обработчиков
from handlers import moderation, commands, pm_to_group, admin_panel

moderation.register_handlers(app)
commands.register_handlers(app)
pm_to_group.register_handlers(app)
admin_panel.register_handlers(app)

# ▶️ Запуск бота
app.run()
