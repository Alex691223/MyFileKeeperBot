import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.types import (
    BotCommand,
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from config import API_TOKEN, ADMINS
from database import (
    init_db, add_user, set_avatar, get_avatar, set_chat,
    remove_chat, get_partner, get_all_users, get_all_chats
)

# === Настройки ===
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

waiting_users = set()
avatar_waiting = set()


# === Клавиатура ===
user_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="🔍 Найти"), KeyboardButton(text="🛑 Стоп")],
        [KeyboardButton(text="📸 Аватар"), KeyboardButton(text="🖼 Моя аватарка")],
        [KeyboardButton(text="🚫 Жалоба")]
    ]
)


# === Команды ===
async def set_bot_commands():
    commands = [
        BotCommand(command="next", description="🔍 Найти собеседника"),
        BotCommand(command="stop", description="🛑 Завершить чат"),
        BotCommand(command="setavatar", description="📸 Установить аватар"),
        BotCommand(command="avatar", description="🖼 Посмотреть аватар собеседника"),
        BotCommand(command="myavatar", description="🖼 Посмотреть свою аватарку"),
        BotCommand(command="report", description="🚫 Пожаловаться на собеседника"),
        BotCommand(command="help", description="ℹ️ Помощь"),
    ]
    await bot.set_my_commands(commands)


@dp.startup()
async def on_start(bot: Bot):
    init_db()
    await set_bot_commands()


# === Обработчики ===

@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    add_user(user_id, username)

    await message.answer(
        "👋 Привет! Это <b>анонимный чат</b>.\n"
        "Используй кнопки снизу 👇",
        reply_markup=user_keyboard
    )


@dp.message(F.text.lower() == "бот")
async def keyword_bot(message: Message):
    await message.answer("✅ Я работаю! Чем помочь?")


@dp.message(F.text.in_(["/help", "ℹ️ Помощь"]))
async def cmd_help(message: Message):
    await message.answer(
        "<b>Команды:</b>\n"
        "🔍 /next — найти собеседника\n"
        "🛑 /stop — завершить чат\n"
        "📸 /setavatar — установить аватар\n"
        "🖼 /avatar — аватар собеседника\n"
        "🖼 /myavatar — моя аватарка\n"
        "🚫 /report — пожаловаться\n"
        "ℹ️ /help — помощь",
        reply_markup=user_keyboard
    )


@dp.message(F.text.in_(["📸 Аватар", "/setavatar"]))
async def cmd_setavatar(message: Message):
    avatar_waiting.add(message.from_user.id)
    await message.answer("📸 Отправь фото, которое станет твоим аватаром.")


@dp.message(F.photo)
async def photo_handler(message: Message):
    user_id = message.from_user.id
    if user_id in avatar_waiting:
        set_avatar(user_id, message.photo[-1].file_id)
        avatar_waiting.discard(user_id)
        await message.answer("✅ Аватар успешно установлен!")
        return

    partner = get_partner(user_id)
    if partner:
        await bot.send_photo(partner, message.photo[-1].file_id, caption=message.caption or "")


@dp.message(F.text.in_(["🔍 Найти", "/next"]))
async def cmd_next(message: Message):
    user_id = message.from_user.id
    if get_partner(user_id):
        await message.answer("❗ Ты уже в чате. Напиши /stop.")
        return
    if user_id in waiting_users:
        await message.answer("⏳ Уже ищем собеседника...")
        return

    partner = next((u for u in waiting_users if u != user_id), None)

    if partner:
        waiting_users.discard(partner)
        set_chat(user_id, partner)
        set_chat(partner, user_id)
        await bot.send_message(user_id, "✅ Собеседник найден! Напиши ему.\n🛑 /stop — завершить", reply_markup=user_keyboard)
        await bot.send_message(partner, "✅ Собеседник найден! Напиши ему.\n🛑 /stop — завершить", reply_markup=user_keyboard)
    else:
        waiting_users.add(user_id)
        await message.answer("🔍 Ищу собеседника...")

@dp.message(F.text.in_(["🛑 Стоп", "/stop"]))
async def cmd_stop(message: Message):
    user_id = message.from_user.id
    partner = get_partner(user_id)

    if partner:
        remove_chat(user_id)
        remove_chat(partner)
        await message.answer("🛑 Чат завершён.", reply_markup=user_keyboard)
        await bot.send_message(partner, "🛑 Собеседник завершил чат.", reply_markup=user_keyboard)
    elif user_id in waiting_users:
        waiting_users.discard(user_id)
        await message.answer("❌ Вышел из поиска.", reply_markup=user_keyboard)
    else:
        await message.answer("ℹ️ Ты не в чате и не в поиске.", reply_markup=user_keyboard)


@dp.message(F.text.in_(["🖼 Аватар", "/avatar"]))
async def cmd_avatar(message: Message):
    user_id = message.from_user.id
    partner = get_partner(user_id)
    if not partner:
        await message.answer("⚠️ Ты не в чате.")
        return
    avatar = get_avatar(partner)
    if avatar:
        await bot.send_photo(user_id, avatar, caption="🖼 Аватар собеседника")
    else:
        await message.answer("🚫 У собеседника нет аватара.")


@dp.message(F.text.in_(["🖼 Моя аватарка", "/myavatar"]))
async def cmd_myavatar(message: Message):
    avatar = get_avatar(message.from_user.id)
    if avatar:
        await message.answer_photo(avatar, caption="🖼 Вот твой аватар")
    else:
        await message.answer("🚫 У тебя пока нет аватара.")


@dp.message(F.text.in_(["🚫 Жалоба", "/report"]))
async def cmd_report(message: Message):
    user_id = message.from_user.id
    partner = get_partner(user_id)
    if not partner:
        await message.answer("⚠️ Ты не в чате.")
        return

    remove_chat(user_id)
    remove_chat(partner)

    await message.answer("🚨 Жалоба отправлена. Чат завершён.", reply_markup=user_keyboard)
    await bot.send_message(partner, "🛑 Собеседник завершил чат.")

    for admin_id in ADMINS:
        await bot.send_message(admin_id, f"🚫 Жалоба от {user_id} на {partner}")


@dp.message()
async def relay(message: Message):
    user_id = message.from_user.id
    partner = get_partner(user_id)
    if not partner:
        await message.answer("❗ Ты не в чате. Нажми «🔍 Найти».")
        return

    if message.text:
        await bot.send_message(partner, message.text)
    elif message.sticker:
        await bot.send_sticker(partner, message.sticker.file_id)
    elif message.voice:
        await bot.send_voice(partner, message.voice.file_id)
    elif message.video:
        await bot.send_video(partner, message.video.file_id, caption=message.caption or "")
    elif message.animation:
        await bot.send_animation(partner, message.animation.file_id)
    elif message.document:
        await bot.send_document(partner, message.document.file_id)
    else:
        await message.answer("⚠️ Этот тип сообщений не поддерживается.")


# === Запуск ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
