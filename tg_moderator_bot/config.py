import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPERADMIN_ID = int(os.getenv("SUPERADMIN_ID", 954426279))  # твой Telegram ID
ADMIN_PASSWORD = "DEWolf228"

LANGUAGES = ["ru", "de"]
DEFAULT_LANG = "ru"

DB_PATH = "database.sqlite"
