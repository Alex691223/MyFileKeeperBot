import sqlite3, random, string
from config import DB_PATH
from utils.auth import activate_user

def generate_keys(n=1, created_by=0):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    keys = []
    for _ in range(n):
        key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        c.execute("INSERT INTO keys (key, created_by) VALUES (?, ?)", (key, created_by))
        keys.append(key)
    conn.commit()
    conn.close()
    return keys

def check_key(key, user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT used FROM keys WHERE key = ?", (key,))
    row = c.fetchone()
    if not row or row[0] == 1:
        conn.close()
        return False
    c.execute("UPDATE keys SET used = 1, used_by = ? WHERE key = ?", (user_id, key))
    c.execute("INSERT OR REPLACE INTO users (user_id, activated) VALUES (?, 1)", (user_id,))
    conn.commit()
    conn.close()
    return True

def get_keys_info():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT key, used, used_by FROM keys ORDER BY used DESC")
    result = c.fetchall()
    conn.close()
    return "\n".join([f"{k} — {'✅' if u else '❌'} (by {ub or 'N/A'})" for k, u, ub in result])
