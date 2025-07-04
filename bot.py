import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, Message, PhotoSize

from config import API_TOKEN, ADMINS
from database import (
    init_db, add_user, set_avatar, get_avatar, set_chat,
    remove_chat, get_partner, get_all_users, get_all_chats
)

# Логгирование
logging.basicConfig(level=logging.INFO)

# Инициализация
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Временные состояния
waiting_users = set()
avatar_waiting = set()


# === Команды меню ===
async def set_bot_commands():
    commands = [
        BotCommand(command="next", description="🔍 Найти собеседника"),
        BotCommand(command="stop", description="🛑 Завершить чат"),
        BotCommand(command="setavatar", description="📸 Установить аватар"),
        BotCommand(command="avatar", description="🖼 Посмотреть аватар собеседника"),
        BotCommand(command="report", description="🚫 Пожаловаться на собеседника"),
        BotCommand(command="help", description="ℹ️ Помощь"),
        BotCommand(command="stats", description="📊 Статистика (админ)"),
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
        "👋 Привет! Это <b>анонимный чат</b>.\n\n"
        "Нажми / и выбери команду:\n"
        "🔍 /next — начать чат\n"
        "🛑 /stop — завершить чат\n"
        "📸 /setavatar — установить аватар\n"
        "🖼 /avatar — посмотреть аву собеседника\n"
        "🚫 /report — пожаловаться"
    )


@dp.message(F.text == "/help")
async def cmd_help(message: Message):
    await message.answer(
        "<b>Команды:</b>\n"
        "/next — найти собеседника\n"
        "/stop — завершить чат\n"
        "/setavatar — установить аватар\n"
        "/avatar — посмотреть аватар собеседника\n"
        "/report — пожаловаться на собеседника\n"
        "/stats — статистика (админ)"
    )


@dp.message(F.text == "/setavatar")
async def cmd_setavatar(message: Message):
    avatar_waiting.add(message.from_user.id)
    await message.answer("📸 Отправь фото, чтобы установить его как аватар.")


@dp.message(F.photo)
async def photo_handler(message: Message):
    user_id = message.from_user.id
    if user_id in avatar_waiting:
        set_avatar(user_id, message.photo[-1].file_id)
        avatar_waiting.discard(user_id)
        await message.answer("✅ Аватар установлен!")
        return

    partner = get_partner(user_id)
    if partner:
        await bot.send_photo(partner, message.photo[-1].file_id, caption=message.caption or "")


@dp.message(F.text == "/next")
async def cmd_next(message: Message):
    user_id = message.from_user.id

    if get_partner(user_id):
        await message.answer("❗ Ты уже в чате. Напиши /stop, чтобы завершить.")
        return

    if user_id in waiting_users:
        await message.answer("⏳ Уже ищем для тебя собеседника...")
        return

    partner = next((u for u in waiting_users if u != user_id), None)

    if partner:
        waiting_users.discard(partner)
        set_chat(user_id, partner)
        set_chat(partner, user_id)
        await bot.send_message(user_id, "✅ Собеседник найден! Общение началось. Напиши /stop чтобы завершить.")
        await bot.send_message(partner, "✅ Собеседник найден! Общение началось. Напиши /stop чтобы завершить.")
    else:
        waiting_users.add(user_id)
        await message.answer("🔍 Ищу собеседника...")


@dp.message(F.text == "/stop")
async def cmd_stop(message: Message):
    user_id = message.from_user.id
    partner = get_partner(user_id)

    if partner:
        remove_chat(user_id)
        remove_chat(partner)
        await message.answer("🛑 Ты завершил чат.")
        await bot.send_message(partner, "🛑 Собеседник завершил чат.")
    elif user_id in waiting_users:
        waiting_users.discard(user_id)
        await message.answer("❌ Ты вышел из режима поиска.")
    else:
        await message.answer("ℹ️ Ты не в чате и не ищешь собеседника.")


@dp.message(F.text == "/avatar")
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
        await message.answer("🚫 Собеседник не установил аватар.")


@dp.message(F.text == "/report")
async def cmd_report(message: Message):
    user_id = message.from_user.id
    partner = get_partner(user_id)
    if not partner:
        await message.answer("⚠️ Ты не в чате.")
        return

    remove_chat(user_id)
    remove_chat(partner)

    await message.answer("🚨 Жалоба отправлена. Чат завершён.")
    await bot.send_message(partner, "🛑 Чат завершён. Пользователь пожаловался.")

    for admin_id in ADMINS:
        await bot.send_message(admin_id, f"🚫 Жалоба от {user_id} на {partner}")


@dp.message(F.text == "/stats")
async def cmd_stats(message: Message):
    if message.from_user.id not in ADMINS:
        await message.answer("⛔️ Команда только для админов.")
        return

    users = get_all_users()
    chats = get_all_chats()

    await message.answer(
        f"📊 Статистика:\n"
        f"Пользователей: {len(users)}\n"
        f"Активных чатов: {len(chats)//2}"
    )


@dp.message()
async def relay_message(message: Message):
    user_id = message.from_user.id
    partner = get_partner(user_id)
    if not partner:
        await message.answer("⚠️ Ты не в чате. Напиши /next.")
        return

    # Пересылаем текст или мультимедиа
    if message.text:
        await bot.send_message(partner, message.text)
    elif message.sticker:
        await bot.send_sticker(partner, message.sticker.file_id)
    elif message.voice:
        await bot.send_voice(partner, message.voice.file_id)
    elif message.video:
        await bot.send_video(partner, message.video.file_id)
    elif message.animation:
        await bot.send_animation(partner, message.animation.file_id)
    elif message.document:
        await bot.send_document(partner, message.document.file_id)
    else:
        await message.answer("⚠️ Этот тип сообщений не поддерживается.")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
