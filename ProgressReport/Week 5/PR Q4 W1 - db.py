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

    # Users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password_hash TEXT NOT NULL
    )
    """)

    # Attendance sessions
    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendances (
        name TEXT PRIMARY KEY,
        start_datetime TEXT,
        end_datetime TEXT,
        minutes_late INTEGER,
        password_hash TEXT,
        creator TEXT,
        countercheck INTEGER,
        question TEXT,
        answer TEXT
    )
    """)

    # Attendance submissions
    cur.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        attendance_name TEXT,
        user TEXT,
        login_time TEXT,
        status TEXT,
        late_minutes INTEGER,
        response TEXT,
        FOREIGN KEY (attendance_name) REFERENCES attendances(name) ON DELETE CASCADE,
        FOREIGN KEY (user) REFERENCES users(username) ON DELETE CASCADE,
        UNIQUE(attendance_name, user)
    )
    """)

    # Login logs
    cur.execute("""
    CREATE TABLE IF NOT EXISTS login_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        timestamp TEXT,
        FOREIGN KEY (user) REFERENCES users(username)
    )
    """)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_sub_user ON submissions(user)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sub_attendance ON submissions(attendance_name)")

    conn.commit()
    conn.close()

# ===================================


# ========== Authentication ==========
# ===== Login =====
def find_user(conn, username):
    cur = conn.cursor()
    cur.execute(
        "SELECT username, password_hash FROM users WHERE LOWER(username)=LOWER(?)",
        (username,)
    )

    row = cur.fetchone()
    return row

def timestamp(conn, username, login_time):
    cur = conn.cursor()
    cur.execute(
            "INSERT INTO login_logs (user, timestamp) VALUES (?, ?)",
            (username, login_time)
    )
    return
# ===== Signup =====
def check_duplicate_user(conn, username):
    cur = conn.cursor()

    cur.execute(
        "SELECT 1 FROM users WHERE LOWER(username)=LOWER(?)",
        (username,)
    )

    return cur.fetchone()

def add_user(conn, username, hashed):
    cur = conn.cursor()
    cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hashed)
    )
    return

# ========== Attendance ==========
# Create Attendance
def check_duplicate_attendance(conn, attendance_name):
    cur = conn.cursor()

    cur.execute(
        "SELECT 1 FROM attendances WHERE LOWER(name)=LOWER(?)",
        (attendance_name,)
    )

    return cur.fetchone()

def insert_attendance(
        conn, 
        attendance_name, 
        start_datetime, 
        end_datetime, 
        minutes_late, 
        hashed_attendance_password, 
        user, 
        required_countercheck, 
        question, 
        hashed_answer
    ):

    cur = conn.cursor()
    
    cur.execute("""
            INSERT INTO attendances
            (name, start_datetime, end_datetime, minutes_late, password_hash, creator,
            countercheck, question, answer)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                attendance_name,
                start_datetime.isoformat(),
                end_datetime.isoformat(),
                minutes_late,
                hashed_attendance_password,
                user,
                int(required_countercheck),
                question,
                hashed_answer
    ))
    
    return

# View Attendance
def get_creator_info(conn, user):
    """Gets info from attendances and submissions, and uses left join to get creator column info"""
    cur = conn.cursor()
    cur.execute("""
        SELECT a.name, s.user, s.login_time, s.status, s.late_minutes, s.response
        FROM attendances a
        LEFT JOIN submissions s ON a.name = s.attendance_name
        WHERE a.creator=?
    """, (user,))
    return cur.fetchall()

def participant_info(conn, user):
    cur = conn.cursor()
    cur.execute("""
        SELECT attendance_name, status, login_time, user, response
        FROM submissions
        WHERE user=?
    """, (user,))
    
    return cur.fetchall()

# Fillout Attendance
def check_attendance_existance(conn, attendance_name):
    cur = conn.cursor()

    cur.execute("""
        SELECT name, start_datetime, end_datetime, minutes_late,
            password_hash, countercheck, question, answer
        FROM attendances
        WHERE LOWER(name)=LOWER(?)
    """, (attendance_name,))
    return cur.fetchone()

def check_already_submmited(conn, attendance_name, user):
    cur = conn.cursor()
    cur.execute("""
        SELECT 1 FROM submissions
        WHERE LOWER(attendance_name)=LOWER(?) AND user=(?)
    """, (attendance_name, user))
    return cur.fetchone()

def record_submission(conn, stored_name, user, display_format, status, late_minutes, response):
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO submissions
        (attendance_name, user, login_time, status, late_minutes, response)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        stored_name,
        user,
        display_format,
        status,
        late_minutes,
        response
    ))
    return
