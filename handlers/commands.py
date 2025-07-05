from pyrogram import Client, filters

def register_handlers(app: Client):
    @app.on_message(filters.command("start"))
    async def start(_, msg):
        await msg.reply("👋 Привет! Я модер-бот. Добавь меня в группу или общайся прямо здесь.")

    @app.on_message(filters.command("help"))
    async def help_cmd(_, msg):
        await msg.reply(
            "ℹ️ Возможности:\n"
            "• /check — проверить, что бот видит сообщения\n"
            "• /start — перезапустить\n"
            "• /help — помощь\n"
            "• работаю в группах и ЛС"
        )

    @app.on_message(filters.command("check") & filters.group)
    async def check(_, msg):
        await msg.reply("✅ Бот видит это сообщение. Всё работает!")
