import aiosqlite

DB_PATH = "bot.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                accepted BOOLEAN DEFAULT 0
            );
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                group_id INTEGER PRIMARY KEY
            );
        """)
        await db.commit()

async def add_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?);", (user_id,))
        await db.commit()

async def accept_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET accepted = 1 WHERE user_id = ?;", (user_id,))
        await db.commit()

async def count_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM users;") as cursor:
            return (await cursor.fetchone())[0]

async def count_groups():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM groups;") as cursor:
            return (await cursor.fetchone())[0]
async def get_all_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT user_id FROM users") as cursor:
            return [row[0] for row in await cursor.fetchall()]


async def get_all_groups():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT group_id FROM groups") as cursor:
            return [row[0] for row in await cursor.fetchall()]
