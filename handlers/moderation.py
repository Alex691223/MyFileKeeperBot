from pyrogram import Client, filters
from pyrogram.types import Message

BAD_WORDS = ["badword1", "badword2"]
CAPS_THRESHOLD = 70

def register_handlers(app: Client):
    @app.on_message(filters.group & filters.text)
    async def moderate_message(_, msg: Message):
        text = msg.text

        if any(word in text.lower() for word in BAD_WORDS):
            await msg.delete()
            return await msg.reply("🚫 Мат запрещён.")

        caps = sum(1 for c in text if c.isupper())
        if caps > CAPS_THRESHOLD and len(text) > 10:
            await msg.delete()
            return await msg.reply("🔇 Слишком много капса.")

        if "http" in text or "t.me/" in text:
            await msg.delete()
            return await msg.reply("❌ Ссылки запрещены.")
