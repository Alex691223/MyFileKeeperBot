from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
import modules.moderation
import modules.automod
import modules.logging
import modules.greetings

bot = Client("IrisBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

modules.moderation.init(bot)
modules.automod.init(bot)
modules.logging.init(bot)
modules.greetings.init(bot)

print("✅ Бот запущен.")
bot.run()
