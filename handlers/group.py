from aiogram import Router
from aiogram.types import Message
from database import add_user

router = Router()

@router.message()
async def handle_group_message(message: Message):
    if message.chat.type in ("group", "supergroup"):
        await add_user(message.from_user.id)
        banned_words = ["плохослова", "badword"]
        if any(word in message.text.lower() for word in banned_words):
            await message.delete()
