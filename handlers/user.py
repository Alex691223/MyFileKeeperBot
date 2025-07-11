from aiogram import Router, types
from aiogram.filters import Command
from utils.auth import get_user_role

router = Router()

@router.message(Command("help"))
async def help_command(msg: types.Message):
    role = get_user_role(msg.from_user.id)
    text = "📖 <b>Доступные команды:</b>\n"
    text += "/help — справка\n"
    text += "/info — информация о вас\n"
    if role in ["moderator", "admin", "superadmin"]:
        text += "/ban — бан по ответу на сообщение\n/mute — мут пользователя\n"
    if role in ["admin", "superadmin"]:
        text += "/panel — вход в админ-панель\n/generate — создать ключи\n/keys — просмотр ключей\n/setrole — назначить роль пользователю\n"
    await msg.answer(text)

@router.message(Command("info"))
async def user_info(msg: types.Message):
    role = get_user_role(msg.from_user.id)
    await msg.answer(
        f"👤 <b>Пользователь:</b> {msg.from_user.full_name}\n"
        f"🆔 <b>ID:</b> <code>{msg.from_user.id}</code>\n"
        f"🔓 <b>Роль:</b> {role}"
    )
