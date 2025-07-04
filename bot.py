import os
import sqlite3
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

from database import init_db

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN is not set in environment variables")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

init_db()

# --- Работа с БД ---
def save_file(user_id, file_id, file_type, caption, category):
    conn = sqlite3.connect("files.db")
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO files (user_id, file_id, file_type, caption, category, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, file_id, file_type, caption, category, datetime.utcnow()))
    conn.commit()
    conn.close()

def detect_category(mime):
    if not mime:
        return "Другое"
    if "image" in mime:
        return "Фото"
    if "video" in mime:
        return "Видео"
    if "audio" in mime:
        return "Аудио"
    if "application" in mime:
        return "Документы"
    return "Другое"

def add_category(user_id, name):
    conn = sqlite3.connect("files.db")
    cur = conn.cursor()
    cur.execute("SELECT id FROM categories WHERE user_id=? AND name=?", (user_id, name))
    if cur.fetchone():
        conn.close()
        return False
    cur.execute("INSERT INTO categories (user_id, name) VALUES (?, ?)", (user_id, name))
    conn.commit()
    conn.close()
    return True

def get_categories(user_id):
    conn = sqlite3.connect("files.db")
    cur = conn.cursor()
    cur.execute("SELECT name FROM categories WHERE user_id=?", (user_id,))
    categories = [row[0] for row in cur.fetchall()]
    conn.close()
    return categories

def get_files_by_category(user_id, category):
    conn = sqlite3.connect("files.db")
    cur = conn.cursor()
    cur.execute("SELECT file_id, caption FROM files WHERE user_id=? AND category=?", (user_id, category))
    files = cur.fetchall()
    conn.close()
    return files

# --- Для временного хранения информации о файлах, которым нужно выбрать категорию ---
user_pending_files = {}  # {user_id: {'file_id': ..., 'file_type': ..., 'caption': ...}}

# --- Хэндлеры бота ---

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.reply(
        "👋 Привет! Отправь мне файл — я сохраню его для тебя.\n\n"
        "Используй /addcategory <название> чтобы добавить категорию.\n"
        "Используй /categories чтобы увидеть список твоих категорий и выбрать для фильтрации."
    )

@dp.message_handler(commands=["addcategory"])
async def add_category_handler(message: types.Message):
    args = message.get_args()
    if not args:
        await message.reply("⚠️ Используй команду так: /addcategory <название категории>")
        return
    success = add_category(message.from_user.id, args.strip())
    if success:
        await message.reply(f"✅ Категория '{args.strip()}' добавлена.")
    else:
        await message.reply("⚠️ Такая категория уже существует.")

@dp.message_handler(commands=["categories"])
async def categories_handler(message: types.Message):
    categories = get_categories(message.from_user.id)
    if not categories:
        await message.reply("У тебя пока нет созданных категорий. Добавь их командой /addcategory.")
        return

    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(text=cat, callback_data=f"cat_{cat}") for cat in categories]
    keyboard.add(*buttons)
    await message.reply("Выбери категорию для просмотра файлов:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("cat_"))
async def category_filter_handler(callback_query: types.CallbackQuery):
    category = callback_query.data[4:]
    user_id = callback_query.from_user.id
    files = get_files_by_category(user_id, category)

    if not files:
        await bot.answer_callback_query(callback_query.id, text="Файлы в этой категории не найдены.", show_alert=True)
        return

    text_msgs = []
    for file_id, caption in files:
        text_msgs.append(f"📎 {caption} (file_id: {file_id})")

    await bot.send_message(user_id, f"Файлы в категории '{category}':\n\n" + "\n".join(text_msgs))
    await bot.answer_callback_query(callback_query.id)

@dp.message_handler(content_types=types.ContentType.ANY)
async def handle_files(msg: types.Message):
    file = msg.document or (msg.photo[-1] if msg.photo else None) or msg.video or msg.audio
    if not file:
        await msg.reply("⛔️ Файл не распознан.")
        return

    file_id = file.file_id
    file_type = getattr(file, 'mime_type', None) or 'unknown'
    caption = msg.caption or "Без описания"

    # Сохраняем файл во временный словарь — ждем выбора категории
    user_pending_files[msg.from_user.id] = {
        "file_id": file_id,
        "file_type": file_type,
        "caption": caption,
    }

    categories = get_categories(msg.from_user.id)
    keyboard = InlineKeyboardMarkup(row_width=2)

    buttons = [InlineKeyboardButton(text=cat, callback_data=f"choosecat_{cat}") for cat in categories]
    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton(text="➕ Добавить новую категорию", callback_data="add_new_category"))

    await msg.reply("Выбери категорию для сохранения файла или создай новую:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("choosecat_"))
async def choose_category_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    category = callback_query.data[10:]

    pending = user_pending_files.get(user_id)
    if not pending:
        await bot.answer_callback_query(callback_query.id, text="Нет файла для сохранения.", show_alert=True)
        return

    save_file(user_id, pending["file_id"], pending["file_type"], pending["caption"], category)
    del user_pending_files[user_id]

    await bot.answer_callback_query(callback_query.id, text=f"Файл сохранён в категории '{category}'.", show_alert=True)
    await bot.send_message(user_id, f"✅ Файл успешно сохранён в категорию: {category}")

@dp.callback_query_handler(lambda c: c.data == "add_new_category")
async def add_new_category_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)

    await bot.send_message(user_id, "Напиши название новой категории:")

    # Устанавливаем состояние ожидания названия категории — сделаем через простую логику в словаре
    user_pending_files[user_id]["awaiting_category_name"] = True

@dp.message_handler()
async def new_category_name_handler(message: types.Message):
    user_id = message.from_user.id
    pending = user_pending_files.get(user_id)

    if not pending or not pending.get("awaiting_category_name"):
        # Это обычное сообщение, обрабатываем по остальным хэндлерам
        return

    category_name = message.text.strip()
    if not category_name:
        await message.reply("Название категории не может быть пустым. Попробуй снова.")
        return

    success = add_category(user_id, category_name)
    if not success:
        await message.reply("Такая категория уже существует. Попробуй другое название.")
        return

    # Сохраняем файл в новую категорию
    save_file(user_id, pending["file_id"], pending["file_type"], pending["caption"], category_name)
    del user_pending_files[user_id]

    await message.reply(f"✅ Новая категория '{category_name}' создана и файл сохранён в неё.")

if __name__ == "__main__":
    executor.start_polling(dp)
