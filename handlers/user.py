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
        text += "/ban — забанить пользователя\n"
        text += "/mute — замутить пользователя\n"
    if role in ["admin", "superadmin"]:
        text += "/panel — вход в админ-панель\n/generate — создать ключи\n/keys — просмотр ключей\n"
    await msg.answer(text)

@router.message(Command("info"))
async def user_info(msg: types.Message):
    role = get_user_role(msg.from_user.id)
    await msg.answer(f"👤 Ваш ID: <code>{msg.from_user.id}</code>\n🔓 Ваша роль: {role}")
