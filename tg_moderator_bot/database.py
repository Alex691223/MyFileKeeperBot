import sqlite3

def init_db():
    conn = sqlite3.connect("database.sqlite")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        activated INTEGER DEFAULT 0,
        role TEXT DEFAULT 'user',
        language TEXT DEFAULT 'ru'
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS keys (
        key TEXT PRIMARY KEY,
        used INTEGER DEFAULT 0,
        used_by INTEGER,
        created_by INTEGER
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        chat_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")

    conn.commit()
    conn.close()
