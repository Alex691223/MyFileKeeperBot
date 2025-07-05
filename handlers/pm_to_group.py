from pyrogram import Client, filters
from config import OWNER_ID, TARGET_GROUP_ID

def register_handlers(app: Client):
    @app.on_message(filters.private & filters.user(OWNER_ID))
    async def forward_to_group(_, msg):
        if msg.text:
            await app.send_message(
                chat_id=TARGET_GROUP_ID,
                text=f"📣 <b>Сообщение от владельца:</b>\n{msg.text}"
            )
            await msg.reply("✅ Отправлено в группу.")
