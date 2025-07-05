from pyrogram import Client, filters

def register_handlers(app: Client):
    @app.on_message(filters.private & filters.text)
    async def reply_pm(_, msg):
        await msg.reply("👋 Это ЛС. Добавь меня в группу, чтобы я мог модерировать.")
