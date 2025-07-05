from pyrogram import filters
from pyrogram.types import Message

BANNED_WORDS = ["плохое_слово", "другое_плохое"]

def init(bot):
    @bot.on_message(filters.text & filters.group)
    async def check_text(client, message: Message):
        text = message.text.lower()
        for word in BANNED_WORDS:
            if word in text:
                await message.delete()
                await message.reply(f"⚠️ Сообщение удалено: запрещённое слово.")
                break
