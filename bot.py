from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

app = Client("moderator_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

from handlers import moderation, commands, pm_to_group, admin_panel

moderation.register_handlers(app)
commands.register_handlers(app)
pm_to_group.register_handlers(app)
admin_panel.register_handlers(app)

app.run()
