import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS memory (user_id INT, text TEXT)")
conn.commit()

def save_memory(uid, text):
    cur.execute("INSERT INTO memory VALUES (?,?)", (uid, text))
    conn.commit()

def get_memory(uid):
    cur.execute("SELECT text FROM memory WHERE user_id=? ORDER BY ROWID DESC LIMIT 5", (uid,))
    return [x[0] for x in cur.fetchall()]