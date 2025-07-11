import sqlite3
from config import DB_PATH, SUPERADMIN_ID

def is_activated(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT activated FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row and row[0] == 1

def activate_user(user_id, username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (user_id, username, activated) VALUES (?, ?, 1)", (user_id, username))
    conn.commit()
    conn.close()

def is_superadmin(user_id):
    return user_id == SUPERADMIN_ID

def get_user_role(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else "user"
