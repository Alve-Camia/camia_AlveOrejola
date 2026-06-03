#db.py
import sqlite3
# ===================================
# SQLite Storage & Tables
db_name = "attendance.db"

def get_db():
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    # ===== v0.5.0 Tables =====
    
    # Student Accounts
    cur.execute("""
    CREATE TABLE IF NOT EXISTS student_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        given_name TEXT NOT NULL,
        surname TEXT NOT NULL,
        login_id TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role='Student'),
        grade_level INTEGER CHECK(grade_level BETWEEN 7 AND 12),
        section TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # Teacher Accounts
    cur.execute("""
    CREATE TABLE IF NOT EXISTS teacher_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        given_name TEXT NOT NULL,
        surname TEXT NOT NULL,
        login_id TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role='Teacher'),
        created_at TEXT NOT NULL
    )
    """)

    # Attendance Session
    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grade_level INTEGER NOT NULL CHECK(grade_level BETWEEN 7 AND 12),
        section TEXT NOT NULL,
        subject TEXT NOT NULL,
        period INTEGER NOT NULL,
        date TEXT NOT NULL,
        created_at TEXT NOT NULL,
        creator_id INTEGER NOT NULL REFERENCES teacher_accounts(id),
        UNIQUE(grade_level, section, subject, period, date)
    )
    """)

    # Attendance Records

    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL REFERENCES attendance_sessions(id) ON DELETE CASCADE,
        student_id INTEGER NOT NULL REFERENCES student_accounts(id) ON DELETE CASCADE,
        status TEXT COLLATE NOCASE NOT NULL CHECK(LOWER(status) IN ('present','tardy','absent','cutting')),
        minutes_late INTEGER DEFAULT 0 CHECK(minutes_late >= 0),
        minutes_cut INTEGER DEFAULT 0 CHECK(minutes_cut >= 0)
                
    )
    """)

    # Login Timpestamps
    cur.execute("""
    CREATE TABLE IF NOT EXISTS account_logins (
        given_name TEXT NOT NULL,
        surname TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
    """)
    
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sub_student_id ON attendance_records(student_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sub_session_id ON attendance_records(session_id)")
    conn.commit()
    conn.close()

# ===================================