from aiogram import Router, types, F
from aiogram.filters import Command
from config import ADMIN_PASSWORD
from utils.keygen import generate_keys, get_keys_info
from utils.auth import is_superadmin

router = Router()

@router.message(Command("panel"))
async def ask_password(msg: types.Message):
    await msg.answer("Введите пароль для входа в админ-панель:")

@router.message(F.text == ADMIN_PASSWORD)
async def admin_panel(msg: types.Message):
    if not is_superadmin(msg.from_user.id):
        await msg.answer("У вас нет доступа.")
        return
    await msg.answer("🔐 Админ-панель. Выберите команду:\n/generate — создать ключи\n/keys — просмотр ключей")

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
