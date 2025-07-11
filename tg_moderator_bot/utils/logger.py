import sqlite3
from config import DB_PATH

def log_action(user_id, action, chat_id=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO logs (user_id, action, chat_id) VALUES (?, ?, ?)", (user_id, action, chat_id))
    conn.commit()
    conn.close()
