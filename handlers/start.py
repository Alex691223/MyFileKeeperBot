from aiogram import Router, types, F
from aiogram.filters import Command
from utils.auth import is_activated, activate_user
from utils.keygen import check_key
from static.agreement import AGREEMENT_RU, AGREEMENT_DE

router = Router()

@router.message(Command("start"))
async def start_handler(msg: types.Message):
    if not is_activated(msg.from_user.id):
        await msg.answer("Выберите язык / Sprache wählen:", reply_markup=lang_buttons())
    else:
        await msg.answer("Вы уже активированы. Используйте /panel для входа в панель управления.")

def lang_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("🇷🇺 Русский"), types.KeyboardButton("🇩🇪 Deutsch"))
    return kb

@router.message(F.text.in_(["🇷🇺 Русский", "🇩🇪 Deutsch"]))
async def agreement_handler(msg: types.Message):
    lang = "ru" if "Русский" in msg.text else "de"
    agreement = AGREEMENT_RU if lang == "ru" else AGREEMENT_DE
    await msg.answer(agreement)
    await msg.answer("Введите ключ активации:")

@router.message(F.text.regexp(r"^[A-Z0-9]{6,}$"))
async def key_handler(msg: types.Message):
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    if is_activated(msg.from_user.id):
        await msg.answer("Вы уже активированы.")
        return

    key = msg.text.strip().upper()
    if check_key(key, msg.from_user.id):
        builder = InlineKeyboardBuilder()
        builder.button(text="➕ Добавить бота в чат", url=f"https://t.me/{(await msg.bot.me()).username}?startgroup=true")
        await msg.answer("✅ Активация прошла успешно!", reply_markup=builder.as_markup())
    else:
        await msg.answer("❌ Неверный или уже использованный ключ.")
