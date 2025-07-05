from pyrogram import filters
from pyrogram.types import Message
import json
import os

eula_db_path = "eula_acceptance.json"
if not os.path.exists(eula_db_path):
    with open(eula_db_path, "w") as f:
        json.dump({}, f)

def has_accepted(user_id):
    with open(eula_db_path, "r") as f:
        data = json.load(f)
    return str(user_id) in data and data[str(user_id)] is True

def accept(user_id):
    with open(eula_db_path, "r") as f:
        data = json.load(f)
    data[str(user_id)] = True
    with open(eula_db_path, "w") as f:
        json.dump(data, f)

def init(bot):
    @bot.on_message(filters.command("start"))
    async def start_command(client, message: Message):
        if has_accepted(message.from_user.id):
            await message.reply("✅ Вы уже приняли условия использования. Спасибо!")
        else:
            await message.reply(
                "📜 Привет! Чтобы использовать этого бота, вы должны принять пользовательское соглашение (EULA).
"
                "Отправьте команду /accept для продолжения.

"
                "Текст соглашения: https://telegra.ph/EULA-TelegramBot-07-05"
            )

    @bot.on_message(filters.command("accept"))
    async def accept_command(client, message: Message):
        accept(message.from_user.id)
        await message.reply("✅ Спасибо! Вы приняли соглашение и теперь можете пользоваться ботом.")

    @bot.on_message(filters.command("ban") & filters.group)
    async def ban_user(client, message: Message):
        if not has_accepted(message.from_user.id):
            return await message.reply("❌ Примите соглашение с помощью команды /accept.")
        if not message.reply_to_message:
            return await message.reply("Ответьте на сообщение пользователя для бана.")
        try:
            await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            await message.reply("Пользователь забанен.")
        except Exception as e:
            await message.reply(f"Ошибка: {e}")

    @bot.on_message(filters.command("kick") & filters.group)
    async def kick_user(client, message: Message):
        if not has_accepted(message.from_user.id):
            return await message.reply("❌ Примите соглашение с помощью команды /accept.")
        if not message.reply_to_message:
            return await message.reply("Ответьте на сообщение пользователя для кика.")
        try:
            await client.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            await client.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            await message.reply("Пользователь кикнут.")
        except Exception as e:
            await message.reply(f"Ошибка: {e}")
