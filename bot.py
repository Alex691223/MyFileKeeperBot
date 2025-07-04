import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from database import init_db, add_user, set_avatar, get_avatar, set_chat, remove_chat, get_partner, get_all_users, get_all_chats
from config import API_TOKEN, ADMINS

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

init_db()

waiting_users = set()
avatar_waiting = set()  # Пользователи, которые отправили /setavatar и ждут фото

def add_to_waiting(user_id):
    waiting_users.add(user_id)

def remove_from_waiting(user_id):
    waiting_users.discard(user_id)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    add_user(user_id, username)
    await message.reply(
        "👋 Привет! Это анонимный чат-бот.\n\n"
        "💬 Используй /next для поиска собеседника.\n"
        "🛑 /stop для завершения чата.\n"
        "📸 /setavatar чтобы установить аватар.\n"
        "ℹ️ /help для справки."
    )

@dp.message_handler(commands=["help"])
async def help_handler(message: types.Message):
    await message.reply(
        "Команды:\n"
        "/next — найти собеседника\n"
        "/stop — завершить чат\n"
        "/setavatar — установить аватар\n"
        "/help — это сообщение\n"
        "Админ команды:\n"
        "/stats — статистика бота\n"
        "/users — список пользователей"
    )

@dp.message_handler(commands=["setavatar"])
async def setavatar_cmd(message: types.Message):
    user_id = message.from_user.id
    avatar_waiting.add(user_id)
    await message.reply("📸 Отправь фото, чтобы установить его как аватар.")

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def photo_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id in avatar_waiting:
        photo = message.photo[-1]
        set_avatar(user_id, photo.file_id)
        avatar_waiting.discard(user_id)
        await message.reply("✅ Аватар установлен.")
    else:
        # Если пользователь в чате — пересылаем фото партнеру
        partner_id = get_partner(user_id)
        if partner_id:
            await bot.send_photo(partner_id, message.photo[-1].file_id, caption=message.caption or "")
        else:
            await message.reply("⚠️ Ты не в чате. Используй /next для поиска собеседника.")

@dp.message_handler(commands=["next"])
async def next_handler(message: types.Message):
    user_id = message.from_user.id

    if get_partner(user_id):
        await message.reply("❗️ Ты уже в чате. Используй /stop, чтобы закончить его.")
        return

    if user_id in waiting_users:
        await message.reply("⏳ Ты уже ищешь собеседника. Подожди.")
        return

    partner = None
    for candidate in waiting_users:
        if candidate != user_id:
            partner = candidate
            break

    if partner:
        set_chat(user_id, partner)
        set_chat(partner, user_id)
        remove_from_waiting(user_id)
        remove_from_waiting(partner)
        await bot.send_message(user_id, "✅ Собеседник найден! Начинайте общение.\nЧтобы закончить чат — /stop.")
        await bot.send_message(partner, "✅ Собеседник найден! Начинайте общение.\nЧтобы закончить чат — /stop.")
    else:
        add_to_waiting(user_id)
        await message.reply("🔎 Ищу для тебя собеседника...")

@dp.message_handler(commands=["stop"])
async def stop_handler(message: types.Message):
    user_id = message.from_user.id
    partner_id = get_partner(user_id)
    if partner_id:
        remove_chat(user_id)
        remove_chat(partner_id)
        await message.reply("🛑 Чат завершён.")
        await bot.send_message(partner_id, "🛑 Твой собеседник завершил чат.")
    elif user_id in waiting_users:
        remove_from_waiting(user_id)
        await message.reply("❌ Ты вышел из поиска собеседника.")
    else:
        await message.reply("ℹ️ Ты не в активном чате и не ищешь собеседника.")

@dp.message_handler(commands=["stats"])
async def stats_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        await message.reply("❌ У тебя нет прав для использования этой команды.")
        return

    users = get_all_users()
    chats = get_all_chats()
    text = f"📊 Статистика бота:\n\nПользователей: {len(users)}\nАктивных чатов: {len(chats)//2}"
    await message.reply(text)

@dp.message_handler(commands=["users"])
async def users_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        await message.reply("❌ У тебя нет прав для использования этой команды.")
        return

    users = get_all_users()
    if not users:
        await message.reply("Список пользователей пуст.")
        return

    text = "👥 Пользователи бота:\n"
    for uid, uname in users:
        text += f"ID: {uid}, username: @{uname if uname else '-'}\n"
    await message.reply(text)

@dp.message_handler()
async def relay_message(message: types.Message):
    user_id = message.from_user.id
    partner_id = get_partner(user_id)

    if not partner_id:
        await message.reply("⚠️ Ты не в чате. Используй /next для поиска собеседника.")
        return

    # Пересылаем сообщения партнеру (текст, стикеры, фото и др.)
    if message.text:
        await bot.send_message(partner_id, message.text)
    elif message.sticker:
        await bot.send_sticker(partner_id, message.sticker.file_id)
    elif message.photo:
        await bot.send_photo(partner_id, message.photo[-1].file_id, caption=message.caption or "")
    elif message.video:
        await bot.send_video(partner_id, message.video.file_id, caption=message.caption or "")
    elif message.voice:
        await bot.send_voice(partner_id, message.voice.file_id, caption=message.caption or "")
    else:
        await message.reply("⚠️ Этот тип сообщения пока не поддерживается.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

