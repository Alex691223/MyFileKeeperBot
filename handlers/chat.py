from aiogram import Router, types
import openai
from config import OPENAI_API_KEY
from database.models import get_user_language
from texts.i18n import t

router = Router()
openai.api_key = OPENAI_API_KEY

PERSONAS = {
    "философ": "Ты философ. Говори мудро, медленно, рассудительно.",
    "гопник": "Ты уличный гопник. Груби, используй уличный сленг.",
    "кот": "Ты игривый кот. Мяукай, веди себя мило.",
    "школьник": "Ты 12-летний школьник. Говори весело и по-детски."
}

@router.message()
async def character_chat(message: types.Message):
    lang = get_user_language(message.from_user.id)
    persona = None
    for key in PERSONAS:
        if key in message.text.lower():
            persona = key
            break

    if not persona:
        await message.answer(t("choose_persona", lang))
        return

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": PERSONAS[persona]},
            {"role": "user", "content": message.text}
        ]
    )
    reply = response.choices[0].message.content.strip()
    await message.answer(reply)
