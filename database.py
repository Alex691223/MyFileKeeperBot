import aiosqlite

DB_PATH = "data.db"

# 📦 Создание таблиц
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                group_id INTEGER PRIMARY KEY
            )
        """)
        await db.commit()

# ➕ Добавление пользователя
async def add_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.commit()

# ➕ Добавление группы
async def add_group(group_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO groups (group_id) VALUES (?)", (group_id,))
        await db.commit()

# 📊 Кол-во пользователей
async def count_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            return (await cursor.fetchone())[0]

# 📊 Кол-во групп
async def count_groups():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM groups") as cursor:
            return (await cursor.fetchone())[0]

# 📥 Получить всех пользователей
async def get_all_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT user_id FROM users") as cursor:
            return [row[0] for row in await cursor.fetchall()]

# 📥 Получить все группы
async def get_all_groups():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT group_id FROM groups") as cursor:
            return [row[0] for row in await cursor.fetchall()]
