from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def register_handlers(app: Client):
    @app.on_message(filters.command("panel") & filters.group)
    async def admin_panel(_, msg):
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📄 Правила", callback_data="rules")],
            [InlineKeyboardButton("👥 Участники", callback_data="members")]
        ])
        await msg.reply("🔧 Панель управления", reply_markup=kb)

    @app.on_callback_query()
    async def handle_callback(_, query):
        if query.data == "rules":
            await query.message.edit_text("📄 Правила: не нарушай!")
        elif query.data == "members":
            count = await query.message.chat.get_members_count()
            await query.message.edit_text(f"👥 Участников: {count}")
