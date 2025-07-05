from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions
from datetime import timedelta
import asyncio

router = Router()

@router.message(Command("kick"))
async def kick_user(message: Message):
    if not message.reply_to_message:
        await message.answer("Ответь на сообщение пользователя, которого хочешь кикнуть.")
        return
    await message.chat.kick(user_id=message.reply_to_message.from_user.id)
    await asyncio.sleep(1)
    await message.chat.unban(user_id=message.reply_to_message.from_user.id)
    await message.answer("Пользователь кикнут.")

@router.message(Command("ban"))
async def ban_user(message: Message):
    if not message.reply_to_message:
        await message.answer("Ответь на сообщение пользователя, которого хочешь забанить.")
        return
    await message.chat.kick(user_id=message.reply_to_message.from_user.id)
    await message.answer("Пользователь забанен.")

@router.message(Command("unban"))
async def unban_user(message: Message):
    if not message.reply_to_message:
        await message.answer("Ответь на сообщение пользователя, которого хочешь разбанить.")
        return
    await message.chat.unban(user_id=message.reply_to_message.from_user.id)
    await message.answer("Пользователь разбанен.")

@router.message(Command("mute"))
async def mute_user(message: Message):
    if not message.reply_to_message:
        await message.answer("Ответь на сообщение пользователя, которого хочешь замьютить.")
        return
    mute_time = 10  # минут
    until_date = message.date + timedelta(minutes=mute_time)
    await message.chat.restrict(
        user_id=message.reply_to_message.from_user.id,
        permissions=ChatPermissions(can_send_messages=False),
        until_date=until_date
    )
    await message.answer(f"Пользователь замьючен на {mute_time} минут.")

@router.message(Command("unmute"))
async def unmute_user(message: Message):
    if not message.reply_to_message:
        await message.answer("Ответь на сообщение пользователя, которого хочешь размьютить.")
        return
    await message.chat.restrict(
        user_id=message.reply_to_message.from_user.id,
        permissions=ChatPermissions(can_send_messages=True)
    )
    await message.answer("Пользователь размьючен.")
