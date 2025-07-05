from pyrogram import filters
from config import ADMINS

def is_admin():
    return filters.user(ADMINS)
