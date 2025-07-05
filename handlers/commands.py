from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from database.mongo import warns, rules
from utils.filters import is_admin
from utils.helpers import extract_user_id

def register_handlers(app: Client):
    @app.on_message(filters.command("ban") & filters.group & is_admin())
    async def ban(_, msg):
        uid = extract_user_id(msg)
        if uid:
            await msg.chat.ban_member(uid)
            await msg.reply("👢 Пользователь забанен.")

    @app.on_message(filters.command("warn") & filters.group & is_admin())
    async def warn(_, msg):
        uid = extract_user_id(msg)
        if uid:
            warns.insert_one({"user_id": uid, "chat_id": msg.chat.id})
            await msg.reply("⚠️ Предупреждение выдано.")

    @app.on_message(filters.command("warns") & filters.group)
    async def get_warns(_, msg):
        uid = extract_user_id(msg) or msg.from_user.id
        count = warns.count_documents({"user_id": uid, "chat_id": msg.chat.id})
        await msg.reply(f"У пользователя {count} предупреждений.")

    @app.on_message(filters.command("setrules") & is_admin())
    async def set_rules(_, msg):
        text = msg.text.split(" ", 1)
        if len(text) == 2:
            rules.update_one({"chat_id": msg.chat.id}, {"$set": {"text": text[1]}}, upsert=True)
            await msg.reply("✅ Правила обновлены.")

    @app.on_message(filters.command("rules") & filters.group)
    async def show_rules(_, msg):
        doc = rules.find_one({"chat_id": msg.chat.id})
        await msg.reply(doc["text"] if doc else "Правила не заданы.")
