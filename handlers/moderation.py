from aiogram import Router, types
from aiogram.filters import Command
from utils.auth import get_user_role

router = Router()

async def get_chat_admin_ids(chat: types.Chat, bot) -> list:
    try:
        members = await bot.get_chat_administrators(chat.id)
        return [m.user.id for m in members]
    except:
        return []

@router.message(Command("ban"))
async def ban(msg: types.Message):
    if not msg.chat or msg.chat.type == "private":
        await msg.answer("❌ Эта команда доступна только в группах.")
        return

    if not msg.reply_to_message:
        await msg.answer("Ответьте на сообщение пользователя, чтобы его забанить.")
        return

    admin_ids = await get_chat_admin_ids(msg.chat, msg.bot)
    role = get_user_role(msg.from_user.id, chat_admins=admin_ids)

    if role not in ["moderator", "admin", "superadmin"]:
        await msg.answer("❌ У вас нет прав на выполнение этой команды.")
        return

    try:
        await msg.chat.ban(msg.reply_to_message.from_user.id)
        await msg.answer("✅ Пользователь забанен.")
    except Exception as e:
        await msg.answer(f"❌ Ошибка при бане: {e}")
