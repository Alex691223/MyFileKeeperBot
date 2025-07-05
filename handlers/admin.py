from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_all_users


from aiogram import Router, types
from aiogram.filters.command import Command
from config import ADMIN_ID

router = Router()

@router.message(Command("stats"))
async def stats(message: types.Message):
    print(f"Команда /stats от {message.from_user.id}")
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("Статистика: Пользователей: 10, Групп: 5")

@router.message(Command("sendto"))
async def send_to_group(message: types.Message):
    print(f"Команда /sendto от {message.from_user.id}")
    if message.from_user.id != ADMIN_ID:
        return
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer("Использование: /sendto <group_id> <сообщение>")
        return
    group_id = args[1]
    text = args[2]
    try:
        await message.bot.send_message(chat_id=int(group_id), text=text)
        await message.answer("Сообщение отправлено.")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")
class BroadcastStates(StatesGroup):
    waiting_text = State()
    confirm = State()
@router.message(Command("broadcast"))
@router.message(F.text == "📢 Рассылка")
async def start_broadcast(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("Введи текст для рассылки:")
    await state.set_state(BroadcastStates.waiting_text)
@router.message(BroadcastStates.waiting_text)
async def confirm_broadcast(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_send"),
         InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_send")]
    ])
    await message.answer(f"Ты хочешь отправить:\n\n{message.text}", reply_markup=kb)
    await state.set_state(BroadcastStates.confirm)
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

    await callback.message.edit_text(f"Рассылка завершена. Успешно: {count}")
    await state.clear()

@router.callback_query(F.data == "cancel_send")
async def cancel_broadcast(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ Рассылка отменена.")
    await state.clear()
