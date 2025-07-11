from aiogram import Router, types, F
from aiogram.filters import Command
from config import ADMIN_PASSWORD
from utils.keygen import generate_keys, get_keys_info
from utils.auth import is_superadmin, set_user_role

router = Router()

@router.message(Command("panel"))
async def ask_password(msg: types.Message):
    await msg.answer("Введите пароль для входа в админ-панель:")

@router.message(F.text == ADMIN_PASSWORD)
async def admin_panel(msg: types.Message):
    user_id = msg.from_user.id
    set_user_role(user_id, "admin")
    await msg.answer("🔐 Доступ разрешён. Ваша роль: admin.\n\nКоманды:\n/generate — сгенерировать ключи\n/keys — просмотр ключей\n/setrole — назначить роль")

@router.message(Command("generate"))
async def generate(msg: types.Message):
    if not is_superadmin(msg.from_user.id):
        await msg.answer("❌ У вас нет прав.")
        return
    keys = generate_keys(10, created_by=msg.from_user.id)
    await msg.answer("🔑 Сгенерированы ключи:\n" + "\n".join(keys))

@router.message(Command("keys"))
async def keys_info(msg: types.Message):
    if not is_superadmin(msg.from_user.id):
        await msg.answer("❌ У вас нет прав.")
        return
    await msg.answer(get_keys_info())

@router.message(Command("setrole"))
async def setrole(msg: types.Message):
    if not is_superadmin(msg.from_user.id):
        await msg.answer("❌ Только супер-админ может назначать роли.")
        return

    parts = msg.text.split()
    if len(parts) != 3:
        await msg.answer("Использование: /setrole <user_id> <роль>\nПример: /setrole 123456789 moderator")
        return

    user_id, role = parts[1], parts[2]
    set_user_role(int(user_id), role)
    await msg.answer(f"✅ Роль '{role}' назначена пользователю {user_id}")
