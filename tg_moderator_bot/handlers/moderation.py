from aiogram import Router, types
from aiogram.filters import Command
from utils.auth import get_user_role

router = Router()

@router.message(Command("ban"))
async def ban(msg: types.Message):
    if get_user_role(msg.from_user.id) not in ["moderator", "admin", "superadmin"]:
        await msg.answer("❌ У вас нет прав на использование этой команды.")
        return
    if not msg.reply_to_message:
        await msg.answer("Ответьте на сообщение пользователя для бана.")
        return
    try:
        await msg.chat.kick(msg.reply_to_message.from_user.id)
        await msg.answer("✅ Пользователь забанен.")
    except:
        await msg.answer("❌ Ошибка при бане.")

@router.message(Command("mute"))
async def mute(msg: types.Message):
    if get_user_role(msg.from_user.id) not in ["moderator", "admin", "superadmin"]:
        await msg.answer("❌ У вас нет прав на использование этой команды.")
        return
    await msg.answer("⏳ Команда /mute реализуется позже.")
