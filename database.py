import sqlite3
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mindmate.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password, salt="mindmate_secret_salt_123!"):
    salted = password + salt
    return hashlib.sha256(salted.encode('utf-8')).hexdigest()

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # Chat sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    # Message logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT NOT NULL,
            sender TEXT NOT NULL, -- 'user' or 'bot'
            text TEXT NOT NULL,
            mood TEXT, -- Only for user messages
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chat_id) REFERENCES chats (id) ON DELETE CASCADE
        )
    ''')
    
    # Chat tip cards table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_tips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT NOT NULL,
            title TEXT NOT NULL,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chat_id) REFERENCES chats (id) ON DELETE CASCADE
        )
    ''')
    
    # Mood tracker history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mood_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            mood TEXT NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    # Study planner tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0, -- 0 = incomplete, 1 = completed
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

# --- User operations ---

def create_user(first_name, last_name, email, password):
    pwd_hash = hash_password(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (first_name, last_name, email, password_hash) VALUES (?, ?, ?, ?)",
            (first_name, last_name, email, pwd_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return {"id": user_id, "first_name": first_name, "last_name": last_name, "email": email}
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def verify_user(email, password):
    pwd_hash = hash_password(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    row = cursor.execute(
        "SELECT id, first_name, last_name, email FROM users WHERE email = ? AND password_hash = ?",
        (email, pwd_hash)
    ).fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    row = cursor.execute(
        "SELECT id, first_name, last_name, email FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

# --- Chat operations ---

def create_chat(chat_id, user_id, title):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chats (id, user_id, title) VALUES (?, ?, ?)",
        (chat_id, user_id, title)
    )
    conn.commit()
    conn.close()
    return {"id": chat_id, "user_id": user_id, "title": title}

def get_chats_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        "SELECT id, title, created_at FROM chats WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_chat(chat_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    row = cursor.execute(
        "SELECT id, user_id, title, created_at FROM chats WHERE id = ?",
        (chat_id,)
    ).fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def update_chat_title(chat_id, user_id, title):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE chats SET title = ? WHERE id = ? AND user_id = ?",
        (title, chat_id, user_id)
    )
    conn.commit()
    conn.close()
    return {"id": chat_id, "user_id": user_id, "title": title}


def delete_chat(chat_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chats WHERE id = ? AND user_id = ?", (chat_id, user_id))
    conn.commit()
    conn.close()

# --- Message operations ---

def add_message(chat_id, sender, text, mood=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (chat_id, sender, text, mood) VALUES (?, ?, ?, ?)",
        (chat_id, sender, text, mood)
    )
    conn.commit()
    msg_id = cursor.lastrowid
    conn.close()
    return {"id": msg_id, "chat_id": chat_id, "sender": sender, "text": text, "mood": mood}

def get_messages_by_chat(chat_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        "SELECT sender, text, mood, created_at FROM messages WHERE chat_id = ? ORDER BY created_at ASC",
        (chat_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_chat_tips(chat_id, tips):
    conn = get_db_connection()
    cursor = conn.cursor()
    for tip in tips:
        cursor.execute(
            "INSERT INTO chat_tips (chat_id, title, text) VALUES (?, ?, ?)",
            (chat_id, tip.get("title", ""), tip.get("text", ""))
        )
    conn.commit()
    conn.close()

def get_tips_by_chat(chat_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        "SELECT title, text, created_at FROM chat_tips WHERE chat_id = ? ORDER BY created_at ASC",
        (chat_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_chat_tips(chat_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_tips WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()

# --- Mood Log operations ---

def add_mood_log(user_id, mood, notes=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO mood_logs (user_id, mood, notes) VALUES (?, ?, ?)",
        (user_id, mood, notes)
    )
    conn.commit()
    log_id = cursor.lastrowid
    conn.close()
    return {"id": log_id, "user_id": user_id, "mood": mood, "notes": notes}

def get_mood_history(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        "SELECT id, mood, notes, created_at FROM mood_logs WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- Study Planner Task operations ---

def create_task(user_id, title):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (user_id, title, completed) VALUES (?, ?, 0)",
        (user_id, title)
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return {"id": task_id, "user_id": user_id, "title": title, "completed": 0}

def get_tasks_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        "SELECT id, title, completed, created_at FROM tasks WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def toggle_task(task_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    row = cursor.execute("SELECT completed FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id)).fetchone()
    if row:
        new_status = 1 if row["completed"] == 0 else 0
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ? AND user_id = ?", (new_status, task_id, user_id))
        conn.commit()
        status = {"id": task_id, "completed": new_status}
    else:
        status = None
    conn.close()
    return status

def delete_task(task_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
    conn.commit()
    conn.close()

# Initialize on import
init_db()
