from aiogram import BaseMiddleware
from aiogram.types import Message
from database import add_user

class AgreementMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        await add_user(event.from_user.id)
        return await handler(event, data)
