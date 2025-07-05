from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import add_user, accept_user

router = Router()

class AgreementFSM(StatesGroup):
    waiting = State()

@router.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    await add_user(message.from_user.id)
    with open("texts/agreement_ru.txt", encoding="utf-8") as f:
        agreement_text = f.read()
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Принять", callback_data="agree")]
    ])
    await message.answer(agreement_text, reply_markup=markup)
    await state.set_state(AgreementFSM.waiting)

@router.callback_query(F.data == "agree")
async def agree_callback(callback: CallbackQuery, state: FSMContext):
    await accept_user(callback.from_user.id)
    await state.clear()
    await callback.message.edit_text("Спасибо, вы приняли условия!")
