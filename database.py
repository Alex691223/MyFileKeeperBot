import sqlite3
from contextlib import closing

DB_NAME = "chatbot.db"

def init_db():
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                avatar_file_id TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                user_id INTEGER PRIMARY KEY,
                partner_id INTEGER
            )
        ''')
        conn.commit()

def add_user(user_id, username):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        conn.commit()

def set_avatar(user_id, file_id):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute("UPDATE users SET avatar_file_id=? WHERE user_id=?", (file_id, user_id))
        conn.commit()

def get_avatar(user_id):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute("SELECT avatar_file_id FROM users WHERE user_id=?", (user_id,))
        row = c.fetchone()
        return row[0] if row else None

def set_chat(user_id, partner_id):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute("REPLACE INTO chats (user_id, partner_id) VALUES (?, ?)", (user_id, partner_id))
        conn.commit()

def remove_chat(user_id):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM chats WHERE user_id=?", (user_id,))
        conn.commit()

def get_partner(user_id):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute("SELECT partner_id FROM chats WHERE user_id=?", (user_id,))
        row = c.fetchone()
        return row[0] if row else None

def get_all_users():
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute("SELECT user_id, username FROM users")
        return c.fetchall()

def get_all_chats():
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute("SELECT user_id, partner_id FROM chats")
        return c.fetchall()
