import sqlite3
from datetime import datetime, timedelta
from config import DB_PATH

def get_cairo_now():
    """الحصول على توقيت وتاريخ مصر الفعلي (UTC+3)"""
    return datetime.utcnow() + timedelta(hours=3)

def init_db():
    """تهيئة قاعدة البيانات (تشمل المحادثات، المنبهات، العادات، والاشتراكات)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            date TEXT,
            role TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scheduled_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            task_title TEXT NOT NULL,
            start_time TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            notified INTEGER DEFAULT 0,
            created_date TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_habits (
            user_id TEXT PRIMARY KEY,
            habits_text TEXT NOT NULL,
            updated_date TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            user_id TEXT PRIMARY KEY,
            plan_name TEXT DEFAULT 'Pro',
            expiry_date TEXT NOT NULL,
            activated_date TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def save_message(user_id: str, role: str, message: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    today = get_cairo_now().strftime("%Y-%m-%d")
    cursor.execute(
        "INSERT INTO daily_logs (user_id, date, role, message) VALUES (?, ?, ?, ?)",
        (str(user_id), today, role, str(message))
    )
    conn.commit()
    conn.close()

def get_recent_history(user_id: str, limit: int = 8) -> str:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT date, role, message FROM daily_logs
            WHERE user_id = ?
            ORDER BY id DESC LIMIT ?
            """,
            (str(user_id), limit)
        )
        rows = cursor.fetchall()
        conn.close()
        if not rows:
            return "لا يوجد سجل محادثات سابق للمستخدم."
        return "\n".join([f"[{r[0]}] {r[1]}: {r[2]}" for r in reversed(rows)])
    except Exception:
        return "لا يوجد سجل محادثات سابق للمستخدم."

def add_scheduled_task(user_id: str, task_title: str, start_time: str) -> int:
    today = get_cairo_now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO scheduled_tasks (user_id, task_title, start_time, created_date) VALUES (?, ?, ?, ?)",
        (str(user_id), task_title.strip(), start_time.strip(), today)
    )
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id

def get_due_tasks_for_alert(target_time_str: str):
    now_cairo = get_cairo_now()
    today = now_cairo.strftime("%Y-%m-%d")
    valid_times = [
        (now_cairo + timedelta(minutes=m)).strftime("%H:%M")
        for m in range(-1, 6)
    ]
    placeholders = ",".join(["?"] * len(valid_times))
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT id, user_id, task_title, start_time 
        FROM scheduled_tasks 
        WHERE start_time IN ({placeholders}) AND status = 'pending' AND notified = 0 AND created_date = ?
        """,
        (*valid_times, today)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

def mark_task_notified(task_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE scheduled_tasks SET notified = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def update_task_status(task_id: int, new_status: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE scheduled_tasks SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()
    conn.close()

def postpone_task_time(task_id: int, new_time_str: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE scheduled_tasks SET start_time = ?, notified = 0, status = 'pending' WHERE id = ?",
        (new_time_str, task_id)
    )
    conn.commit()
    conn.close()

def get_today_tasks(user_id: str):
    today = get_cairo_now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, task_title, start_time, status FROM scheduled_tasks WHERE user_id = ? AND created_date = ? ORDER BY start_time ASC",
        (str(user_id), today)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_active_users_today():
    today = get_cairo_now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT user_id FROM scheduled_tasks WHERE created_date = ?", (today,))
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users

def save_user_habits(user_id: str, habits_text: str):
    init_db()
    today = get_cairo_now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO user_habits (user_id, habits_text, updated_date) VALUES (?, ?, ?)",
        (str(user_id), habits_text.strip(), today)
    )
    conn.commit()
    conn.close()

def get_user_habits(user_id: str) -> str:
    try:
        init_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT habits_text FROM user_habits WHERE user_id = ?", (str(user_id),))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else ""
    except Exception:
        return ""

def clear_user_habits(user_id: str):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_habits WHERE user_id = ?", (str(user_id),))
    conn.commit()
    conn.close()

def get_weekly_tasks_summary(user_id: str):
    init_db()
    now_cairo = get_cairo_now()
    start_date = (now_cairo - timedelta(days=6)).strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT created_date, status, COUNT(*) 
        FROM scheduled_tasks 
        WHERE user_id = ? AND created_date >= ?
        GROUP BY created_date, status
        ORDER BY created_date ASC
        """,
        (str(user_id), start_date)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

def activate_user_pro(user_id: str, days: int = 30, plan_name: str = "Pro"):
    init_db()
    now_cairo = get_cairo_now()
    activated = now_cairo.strftime("%Y-%m-%d")
    expiry = (now_cairo + timedelta(days=days)).strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO subscriptions (user_id, plan_name, expiry_date, activated_date) VALUES (?, ?, ?, ?)",
        (str(user_id), plan_name, expiry, activated)
    )
    conn.commit()
    conn.close()
    return expiry

def get_user_subscription(user_id: str):
    try:
        init_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT plan_name, expiry_date FROM subscriptions WHERE user_id = ?", (str(user_id),))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return {"is_pro": False, "plan": "الباقة المجانية", "expiry": "غير مفعل"}
        today = get_cairo_now().strftime("%Y-%m-%d")
        is_active = row[1] >= today
        return {
            "is_pro": is_active,
            "plan": f"باقة {row[0]} الاحترافية 💎" if is_active else "منتهية",
            "expiry": row[1]
        }
    except Exception:
        return {"is_pro": False, "plan": "الباقة المجانية", "expiry": "غير مفعل"}
