import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import SUPPORTED_LANGUAGES
from database.models import set_user_language
from texts.i18n import t

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=lang)] for lang in SUPPORTED_LANGUAGES],
        resize_keyboard=True
    )
    await message.answer(t("start_choose_lang"), reply_markup=kb)

@router.message(F.text.in_(SUPPORTED_LANGUAGES))
async def language_chosen(message: types.Message, state: FSMContext):
    set_user_language(message.from_user.id, message.text)
    await message.answer(t("agree_prompt", message.text), reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t("agree_button", message.text))]],
        resize_keyboard=True
    ))
