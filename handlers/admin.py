from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.types import (
    Message, ReplyKeyboardMarkup, KeyboardButton,
    ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from config import ADMIN_ID
from database import count_users, count_groups, get_all_groups, get_all_users

router = Router()

# 📋 Состояния для рассылки
class BroadcastStates(StatesGroup):
    waiting_text = State()
    confirm = State()

# 🔘 Команда: открыть админ-панель
@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="📢 Рассылка")],
            [KeyboardButton(text="📜 Группы")],
            [KeyboardButton(text="👥 Пользователи")]
        ],
        resize_keyboard=True
    )
    await message.answer("🔧 Админ-панель", reply_markup=kb)

# 📊 Статистика
@router.message(F.text == "📊 Статистика")
@router.message(Command("stats"))
async def stats(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    users = await count_users()
    groups = await count_groups()
    await message.answer(f"📊 Статистика:\n👥 Пользователей: {users}\n👥 Групп: {groups}")

# 📜 Список групп
@router.message(F.text == "📜 Группы")
async def list_groups(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    groups = await get_all_groups()
    if not groups:
        await message.answer("⚠️ Групп нет.")
    else:
        text = "📜 Список групп:\n" + "\n".join([str(g) for g in groups])
        await message.answer(text)

# 👥 Список пользователей
@router.message(F.text == "👥 Пользователи")
async def list_users(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    users = await get_all_users()
    await message.answer(f"👥 Всего пользователей: {len(users)}")

# 📢 Запуск рассылки
@router.message(Command("broadcast"))
@router.message(F.text == "📢 Рассылка")
async def start_broadcast(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("✉️ Введи текст для рассылки:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(BroadcastStates.waiting_text)

# 📢 Подтверждение рассылки
@router.message(BroadcastStates.waiting_text)
async def confirm_broadcast(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_send"),
         InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_send")]
    ])
    await message.answer(f"Вот текст рассылки:\n\n{message.text}", reply_markup=kb)
    await state.set_state(BroadcastStates.confirm)

# ✅ Отправка рассылки
@router.callback_query(F.data == "confirm_send")
async def do_broadcast(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    users = await get_all_users()
    count = 0

    for user_id in users:
        try:
            await callback.bot.send_message(user_id, text)
            count += 1
        except:
            continue

    await callback.message.edit_text(f"✅ Рассылка завершена.\nУспешно отправлено: {count}")
    await state.clear()

# ❌ Отмена рассылки
@router.callback_query(F.data == "cancel_send")
async def cancel_broadcast(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ Рассылка отменена.")
    await state.clear()
