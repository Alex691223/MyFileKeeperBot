from pyrogram import filters
from pyrogram.types import Message
from config import LOG_CHANNEL

def init(bot):
    @bot.on_message(filters.group)
    async def log_message(client, message: Message):
        if message.text:
            log = f"👤 {message.from_user.mention} в {message.chat.title}:
{message.text}"
            await client.send_message(LOG_CHANNEL, log)
