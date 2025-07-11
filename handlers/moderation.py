from aiogram import Router, types
from aiogram.filters import Command
from utils.auth import get_user_role
from aiogram.utils.markdown import hlink
from datetime import timedelta

router = Router()

async def get_chat_admin_ids(chat: types.Chat, bot) -> list:
    try:
        members = await bot.get_chat_administrators(chat.id)
        return [m.user.id for m in members]
    except:
        return []

def has_permission(user_id, admin_ids, required_roles):
    role = get_user_role(user_id, chat_admins=admin_ids)
    return role in required_roles

@router.message(Command("ban"))
async def ban(msg: types.Message):
    if msg.chat.type == "private":
        return await msg.answer("❌ Эта команда доступна только в группах.")

    if not msg.reply_to_message:
        return await msg.answer("Ответьте на сообщение, чтобы забанить пользователя.")

    admin_ids = await get_chat_admin_ids(msg.chat, msg.bot)
    if not has_permission(msg.from_user.id, admin_ids, ["moderator", "admin", "superadmin"]):
        return await msg.answer("❌ У вас нет прав.")

    try:
        await msg.chat.ban(msg.reply_to_message.from_user.id)
        await msg.answer("✅ Пользователь забанен.")
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {e}")

@router.message(Command("unban"))
async def unban(msg: types.Message):
    if msg.chat.type == "private":
        return await msg.answer("❌ Эта команда доступна только в группах.")

    if not msg.reply_to_message:
        return await msg.answer("Ответьте на сообщение, чтобы разбанить пользователя.")

    admin_ids = await get_chat_admin_ids(msg.chat, msg.bot)
    if not has_permission(msg.from_user.id, admin_ids, ["moderator", "admin", "superadmin"]):
        return await msg.answer("❌ У вас нет прав.")

    try:
        await msg.chat.unban(msg.reply_to_message.from_user.id)
        await msg.answer("✅ Пользователь разбанен.")
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {e}")

@router.message(Command("kick"))
async def kick(msg: types.Message):
    if msg.chat.type == "private":
        return await msg.answer("❌ Эта команда доступна только в группах.")

    if not msg.reply_to_message:
        return await msg.answer("Ответьте на сообщение, чтобы кикнуть пользователя.")

    admin_ids = await get_chat_admin_ids(msg.chat, msg.bot)
    if not has_permission(msg.from_user.id, admin_ids, ["moderator", "admin", "superadmin"]):
        return await msg.answer("❌ У вас нет прав.")

    try:
        await msg.chat.ban(msg.reply_to_message.from_user.id)
        await msg.chat.unban(msg.reply_to_message.from_user.id)
        await msg.answer("✅ Пользователь кикнут.")
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {e}")

@router.message(Command("warn"))
async def warn(msg: types.Message):
    if msg.chat.type == "private":
        return await msg.answer("❌ Эта команда доступна только в группах.")

    if not msg.reply_to_message:
        return await msg.answer("Ответьте на сообщение, чтобы выдать предупреждение.")

    admin_ids = await get_chat_admin_ids(msg.chat, msg.bot)
    if not has_permission(msg.from_user.id, admin_ids, ["moderator", "admin", "superadmin"]):
        return await msg.answer("❌ У вас нет прав.")

    try:
        warned_user = msg.reply_to_message.from_user
        await msg.answer(f"⚠️ Предупреждение выдано: {hlink(warned_user.full_name, f'tg://user?id={warned_user.id}')}")
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {e}")

@router.message(Command("mute"))
async def mute(msg: types.Message):
    if msg.chat.type == "private":
        return await msg.answer("❌ Эта команда доступна только в группах.")

    if not msg.reply_to_message:
        return await msg.answer("Ответьте на сообщение, чтобы замутить пользователя.")

    admin_ids = await get_chat_admin_ids(msg.chat, msg.bot)
    if not has_permission(msg.from_user.id, admin_ids, ["moderator", "admin", "superadmin"]):
        return await msg.answer("❌ У вас нет прав.")

    try:
        until_date = types.datetime.datetime.now() + timedelta(minutes=10)
        await msg.chat.restrict(
            user_id=msg.reply_to_message.from_user.id,
            permissions=types.ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        await msg.answer("🔇 Пользователь замучен на 10 минут.")
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {e}")
