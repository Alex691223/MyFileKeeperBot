from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

app = Client("moderator_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Импорт обработчиков
from handlers import commands, moderation, pm_support
commands.register_handlers(app)
moderation.register_handlers(app)
pm_support.register_handlers(app)

# Старт
app.run()
