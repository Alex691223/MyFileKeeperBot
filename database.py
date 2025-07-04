import sqlite3

def init_db():
    conn = sqlite3.connect("files.db")
    cur = conn.cursor()

    # Таблица файлов
    cur.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            file_id TEXT,
            file_type TEXT,
            caption TEXT,
            category TEXT,
            created_at TEXT
        )
    ''')

    # Таблица пользовательских категорий
    cur.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT
        )
    ''')

    # Таблица пользователей и статистики
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            avatar_file_id TEXT,
            join_date TEXT,
            message_count INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()
