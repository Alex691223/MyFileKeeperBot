from pyrogram import filters

def init(bot):
    @bot.on_message(filters.new_chat_members)
    async def welcome(client, message):
        for user in message.new_chat_members:
            await message.reply(f"👋 Добро пожаловать, {user.mention}!")

    @bot.on_message(filters.left_chat_member)
    async def goodbye(client, message):
        await message.reply(f"👋 {message.left_chat_member.mention} покинул чат.")
