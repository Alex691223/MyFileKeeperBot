import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from collections import defaultdict
from datetime import datetime, timedelta

API_TOKEN = 'YOUR_BOT_TOKEN_HERE'

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# ---------------- Данные ---------------- #

waiting_users = set()
active_chats = {}
chat_start_time = {}
user_profiles = {}
message_timestamps = defaultdict(list)

# Профили: {id: {'gender': 'm'/'f', 'language': 'ru'/'en', 'filter_gender': 'any'/'m'/'f'}}
GENDERS = {'m': '👨 Мужчина', 'f': '👩 Женщина'}
LANGS = {'ru': '🇷🇺 Русский', 'en': '🇬🇧 English'}

# ---------------- Интерфейсы ---------------- #

def get_lang(user_id):
    return user_profiles.get(user_id, {}).get("language", "ru")

def tr(user_id, ru, en):
    return ru if get_lang(user_id) == "ru" else en

def get_main_kb(user_id):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=tr(user_id, "🔍 Найти собеседника", "🔍 Find partner"))],
            [KeyboardButton(text=tr(user_id, "⚙️ Настройки", "⚙️ Settings"))],
        ],
        resize_keyboard=True
    )

def get_chat_kb(user_id):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=tr(user_id, "⏭ Следующий", "⏭ Next")),
             KeyboardButton(text=tr(user_id, "❌ Завершить чат", "❌ End chat"))],
        ],
        resize_keyboard=True
    )

def get_gender_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👨 Мужчина"), KeyboardButton(text="👩 Женщина")],
        ],
        resize_keyboard=True
    )

def get_lang_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇬🇧 English")],
        ],
        resize_keyboard=True=True
    )

def get_filter_kb(user_id):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=tr(user_id, "👫 Любой пол", "👫 Any gender"))],
            [KeyboardButton(text=tr(user_id, "👨 Только мужчины", "👨 Only men")),
             KeyboardButton(text=tr(user_id, "👩 Только женщины", "👩 Only women"))],
            [KeyboardButton(text=tr(user_id, "🔙 Назад", "🔙 Back"))],
        ],
        resize_keyboard=True
    )

# ---------------- Команды ---------------- #

@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    user_profiles[user_id] = {}
    await message.answer("👋 Привет! Укажи свой пол:", reply_markup=get_gender_kb())

@dp.message(F.text.in_({"👨 Мужчина", "👩 Женщина"}))
async def gender_select(message: types.Message):
    gender = "m" if "Мужчина" in message.text else "f"
    user_profiles[message.from_user.id]["gender"] = gender
    await message.answer("🌐 Выбери язык / Choose language:", reply_markup=get_lang_kb())

@dp.message(F.text.in_({"🇷🇺 Русский", "🇬🇧 English"}))
async def language_select(message: types.Message):
    lang = "ru" if "Русский" in message.text else "en"
    user_profiles[message.from_user.id]["language"] = lang
    user_profiles[message.from_user.id]["filter_gender"] = "any"
    await message.answer(tr(message.from_user.id, "✅ Готово! Меню ниже 👇", "✅ Done! Menu below 👇"),
                         reply_markup=get_main_kb(message.from_user.id))

@dp.message(F.text.in_({"⚙️ Настройки", "⚙️ Settings"}))
async def settings(message: types.Message):
    lang = get_lang(message.from_user.id)
    await message.answer(tr(message.from_user.id, "Выберите фильтр для поиска собеседника:",
                                            "Choose a gender filter:"),
                         reply_markup=get_filter_kb(message.from_user.id))

@dp.message(F.text.in_({"🔙 Назад", "🔙 Back"}))
async def back_to_menu(message: types.Message):
    await message.answer(tr(message.from_user.id, "Назад в меню", "Back to menu"),
                         reply_markup=get_main_kb(message.from_user.id))

@dp.message(F.text.in_({
    "👫 Любой пол", "👨 Только мужчины", "👩 Только женщины",
    "👫 Any gender", "👨 Only men", "👩 Only women"
}))
async def set_filter(message: types.Message):
    uid = message.from_user.id
    text = message.text

    if "Any" in text or "Любой" in text:
        user_profiles[uid]["filter_gender"] = "any"
    elif "мужчины" in text or "men" in text:
        user_profiles[uid]["filter_gender"] = "m"
    elif "женщины" in text or "women" in text:
        user_profiles[uid]["filter_gender"] = "f"

    await message.answer(tr(uid, "✅ Фильтр обновлён!", "✅ Filter updated!"),
                         reply_markup=get_main_kb(uid))

# ---------------- Поиск и чат ---------------- #

@dp.message(F.text.in_({"🔍 Найти собеседника", "🔍 Find partner"}))
async def find_partner(message: types.Message):
    user_id = message.from_user.id
    user_profile = user_profiles.get(user_id)
    if not user_profile:
        await start(message)
        return

    if user_id in active_chats:
        await message.answer(tr(user_id, "⚠️ Вы уже в чате.", "⚠️ You're already in chat."),
                             reply_markup=get_chat_kb(user_id))
        return

    # Поиск подходящего собеседника
    for partner_id in list(waiting_users):
        partner_profile = user_profiles.get(partner_id)
        if not partner_profile:
            continue

        # Фильтры
        if (user_profile["filter_gender"] in ("any", partner_profile["gender"]) and
            partner_profile["filter_gender"] in ("any", user_profile["gender"])):
            waiting_users.remove(partner_id)
            active_chats[user_id] = partner_id
            active_chats[partner_id] = user_id
            chat_start_time[user_id] = chat_start_time[partner_id] = datetime.now()

            await message.answer(tr(user_id, "✅ Собеседник найден!", "✅ Partner found!"),
                                 reply_markup=get_chat_kb(user_id))
            await bot.send_message(partner_id, tr(partner_id, "✅ Собеседник найден!", "✅ Partner found!"),
                                   reply_markup=get_chat_kb(partner_id))
            return

    # Если никого не нашли
    waiting_users.add(user_id)
    await message.answer(tr(user_id, "🔍 Поиск собеседника...", "🔍 Searching for a partner..."))

@dp.message(F.text.in_({"❌ Завершить чат", "❌ End chat"}))
async def end_chat(message: types.Message):
    await terminate_chat(message.from_user.id, manual=True)

@dp.message(F.text.in_({"⏭ Следующий", "⏭ Next"}))
async def next_chat(message: types.Message):
    await terminate_chat(message.from_user.id, manual=True)
    await find_partner(message)

# ---------------- Завершение ---------------- #

async def terminate_chat(user_id: int, manual: bool = False):
    partner_id = active_chats.pop(user_id, None)
    chat_start_time.pop(user_id, None)

    if partner_id:
        active_chats.pop(partner_id, None)
        chat_start_time.pop(partner_id, None)
        try:
            await bot.send_message(partner_id, "❌ Чат завершён.", reply_markup=get_main_kb(partner_id))
        except:
            pass

    if manual:
        await bot.send_message(user_id, "✅ Чат завершён.", reply_markup=get_main_kb(user_id))

# ---------------- Пересылка ---------------- #

@dp.message()
async def forward(message: types.Message):
    uid = message.from_user.id
    pid = active_chats.get(uid)
    if not pid:
        await message.answer(tr(uid, "Сначала найдите собеседника.", "Find a partner first."),
                             reply_markup=get_main_kb(uid))
        return

    now = datetime.now()
    message_timestamps[uid] = [t for t in message_timestamps[uid] if now - t < timedelta(seconds=5)]
    if len(message_timestamps[uid]) >= 5:
        await message.answer("⏳ Подожди немного.")
        return

    message_timestamps[uid].append(now)

    try:
        if message.text:
            await bot.send_message(pid, message.text)
        elif message.photo:
            await bot.send_photo(pid, photo=message.photo[-1].file_id, caption=message.caption or "")
        elif message.sticker:
            await bot.send_sticker(pid, message.sticker.file_id)
        elif message.voice:
            await bot.send_voice(pid, message.voice.file_id)
        elif message.video:
            await bot.send_video(pid, message.video.file_id)
    except Exception as e:
        await message.answer("⚠️ Ошибка отправки.")

# ---------------- Запуск ---------------- #

async def main():
    print("Бот запущен.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
