import sqlite3

def init_db():
    conn = sqlite3.connect("persona.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            language TEXT DEFAULT 'en',
            consent INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            persona TEXT PRIMARY KEY,
            uses INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def set_user_language(user_id, lang):
    conn = sqlite3.connect("persona.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO users (user_id, language) VALUES (?, ?)", (user_id, lang))
    conn.commit()
    conn.close()

def get_user_language(user_id):
    conn = sqlite3.connect("persona.db")
    cursor = conn.cursor()
    cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 'en'
