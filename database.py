# ============ БАЗА ДАННЫХ ============
import sqlite3, time
from config import DB_PATH, ADMIN_IDS

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cur = conn.cursor()

def init_db():
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        balance INTEGER DEFAULT 100,
        level INTEGER DEFAULT 1,
        xp INTEGER DEFAULT 0,
        rank TEXT DEFAULT 'Новичок',
        wins INTEGER DEFAULT 0,
        losses INTEGER DEFAULT 0,
        last_seen INTEGER DEFAULT 0
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS games_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER, game TEXT, bet INTEGER, result INTEGER, ts INTEGER
    )""")
    conn.commit()

def init_admins():
    cur.execute("""CREATE TABLE IF NOT EXISTS admins (
        user_id INTEGER PRIMARY KEY,
        added_by INTEGER,
        added_at INTEGER
    )""")
    conn.commit()
    for uid in ADMIN_IDS:
        cur.execute("INSERT OR IGNORE INTO admins (user_id, added_by, added_at) VALUES (?,?,?)",
                    (uid, 0, int(time.time())))
    conn.commit()

def get_user(user_id):
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    if not row:
        cur.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        row = cur.fetchone()
    keys = ["user_id","balance","level","xp","rank","wins","losses","last_seen"]
    return dict(zip(keys, row))

def save_user(user):
    cur.execute("""UPDATE users SET balance=?, level=?, xp=?, rank=?,
                   wins=?, losses=?, last_seen=? WHERE user_id=?""",
                (user["balance"], user["level"], user["xp"], user["rank"],
                 user["wins"], user["losses"], user["last_seen"], user["user_id"]))
    conn.commit()

def log_game(user_id, game, bet, result):
    cur.execute("INSERT INTO games_log (user_id, game, bet, result, ts) VALUES (?,?,?,?,?)",
                (user_id, game, bet, result, int(time.time())))
    conn.commit()

def top_by_balance(limit=10):
    cur.execute("SELECT user_id, balance, level, rank FROM users ORDER BY balance DESC LIMIT ?", (limit,))
    return cur.fetchall()

def count_users():
    cur.execute("SELECT COUNT(*) FROM users")
    return cur.fetchone()[0]

def sum_balance():
    cur.execute("SELECT SUM(balance) FROM users")
    return cur.fetchone()[0] or 0

def active_today():
    cur.execute("SELECT COUNT(*) FROM users WHERE last_seen >= ?", (int(time.time()) - 86400,))
    return cur.fetchone()[0]

def most_popular_game():
    cur.execute("SELECT game, COUNT(*) c FROM games_log GROUP BY game ORDER BY c DESC LIMIT 1")
    row = cur.fetchone()
    return row[0] if row else "—"

def all_user_ids():
    cur.execute("SELECT user_id FROM users")
    return [r[0] for r in cur.fetchall()]

def set_field(user_id, field, value):
    assert field in ("balance","level","xp","rank","wins","losses")
    cur.execute(f"UPDATE users SET {field}=? WHERE user_id=?", (value, user_id))
    conn.commit()

def is_admin(user_id):
    cur.execute("SELECT 1 FROM admins WHERE user_id=?", (user_id,))
    return cur.fetchone() is not None

def add_admin(user_id, added_by):
    cur.execute("INSERT OR IGNORE INTO admins (user_id, added_by, added_at) VALUES (?,?,?)",
                (user_id, added_by, int(time.time())))
    conn.commit()
    return cur.rowcount > 0

def remove_admin(user_id):
    cur.execute("DELETE FROM admins WHERE user_id=?", (user_id,))
    conn.commit()
    return cur.rowcount > 0

def list_admins():
    cur.execute("SELECT user_id, added_by, added_at FROM admins ORDER BY added_at")
    return cur.fetchall()