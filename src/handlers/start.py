from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline import language_keyboard, agree_keyboard
from database.models import set_user_language
from texts.i18n import t

router = Router()

@router.message(F.text == "/start")
async def start_handler(message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите язык / Choose language / Sprache auswählen:", reply_markup=language_keyboard())

@router.callback_query(F.data.startswith("set_lang:"))
async def callback_set_language(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split(":")[1]
    await state.update_data(lang=lang)
    set_user_language(callback.from_user.id, lang)
    
    prompt = t("agree_prompt", lang)
    if not prompt.strip():
        prompt = "⚠️ Не найден текст приглашения."

    await callback.message.edit_text(prompt, reply_markup=agree_keyboard(lang))
    await callback.answer()

@router.callback_query(F.data == "agree")
async def callback_agree(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "English")

    rules = t("rules_text", lang)
    if not rules.strip():
        rules = "⚠️ Текст пользовательского соглашения не найден."

    await callback.message.edit_text(rules)
    await callback.answer()
