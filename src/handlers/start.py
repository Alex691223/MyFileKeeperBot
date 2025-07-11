from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.inline import language_keyboard, agree_keyboard
from database.models import set_user_language
from texts.i18n import t

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите язык:", reply_markup=language_keyboard())

@router.message(F.text.in_(["Русский", "Deutsch", "English"]))
async def set_language(message: Message, state: FSMContext):
    lang = message.text
    await state.update_data(lang=lang)
    set_user_language(message.from_user.id, lang)
    await message.answer(t("agree_prompt", lang), reply_markup=agree_keyboard(lang))

@router.message(F.text.in_(["Agree", "Согласен", "Zustimmen"]))
async def agree_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "English")
    await message.answer(t("rules_text", lang))
