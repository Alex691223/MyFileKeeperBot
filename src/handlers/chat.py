from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from services.personas import personas
from services.openai_api import ask_gpt
from keyboards.personas import persona_keyboard
from texts.i18n import t

router = Router()

@router.message(F.text.lower().in_(["персонаж", "character", "роль"]))
async def ask_to_choose(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "English")
    await message.answer(t("choose_persona", lang), reply_markup=persona_keyboard())

@router.callback_query(F.data.startswith("persona:"))
async def set_persona(callback: CallbackQuery, state: FSMContext):
    persona_name = callback.data.split(":")[1]
    await state.update_data(persona=persona_name)
    await callback.message.edit_text(f"✅ Персонаж выбран: {persona_name}")
    await callback.answer()

@router.message()
async def character_chat(message: Message, state: FSMContext):
    data = await state.get_data()
    persona = data.get("persona")
    lang = data.get("lang", "English")

    if not persona:
        await message.answer(t("choose_persona", lang), reply_markup=persona_keyboard())
        return

    reply = await ask_gpt(message.text, persona)
    if not reply.strip():
        reply = "⚠️ Ответ пуст. Попробуйте снова."
    await message.answer(reply)
