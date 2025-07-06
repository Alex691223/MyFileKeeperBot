import logging
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    member = await context.bot.get_chat_member(chat_id, user_id)
    return member.status in ['administrator', 'creator']

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return await update.message.reply_text("⛔ Только администратор может использовать эту команду.")
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Ответьте на сообщение пользователя, чтобы забанить его.")
    user = update.message.reply_to_message.from_user
    await context.bot.ban_chat_member(update.effective_chat.id, user.id)
    await update.message.reply_text(f"✅ Пользователь {user.mention_html()} забанен.", parse_mode='HTML')

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return await update.message.reply_text("⛔ Только администратор может использовать эту команду.")
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Ответьте на сообщение пользователя, чтобы замутить его.")
    user = update.message.reply_to_message.from_user
    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user.id,
        permissions=ChatPermissions(can_send_messages=False)
    )
    await update.message.reply_text(f"🔇 Пользователь {user.mention_html()} замучен.", parse_mode='HTML')

async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return await update.message.reply_text("⛔ Только администратор может использовать эту команду.")
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Ответьте на сообщение пользователя, чтобы размутить его.")
    user = update.message.reply_to_message.from_user
    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user.id,
        permissions=ChatPermissions(can_send_messages=True)
    )
    await update.message.reply_text(f"🔊 Пользователь {user.mention_html()} размучен.", parse_mode='HTML')

async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return await update.message.reply_text("⛔ Только администратор может использовать эту команду.")
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Ответьте на сообщение пользователя, чтобы кикнуть его.")
    user = update.message.reply_to_message.from_user
    await context.bot.ban_chat_member(update.effective_chat.id, user.id)
    await context.bot.unban_chat_member(update.effective_chat.id, user.id)
    await update.message.reply_text(f"👢 Пользователь {user.mention_html()} кикнут.", parse_mode='HTML')

def get_app():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))
    app.add_handler(CommandHandler("kick", kick))
    return app
