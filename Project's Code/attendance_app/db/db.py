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
    # NOTE: Separate teacher and student accounts to make queries more efficient, and to segragate data

    
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


    # ===== v0.4.0 Tables =====
    # Users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY COLLATE NOCASE,
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
    
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sub_student_id ON attendance_records(student_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sub_session_id ON attendance_records(session_id)")
    conn.commit()
    conn.close()



# ===================================

# ========== Attendance ==========
# ===== Attendance Dashboard =====
def get_dashboard_table_info(conn, creator_id):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, date, grade_level, section, subject, period
        FROM attendance_sessions
        WHERE creator_id=?
        ORDER BY date
        """,
        (creator_id,)
    )
    return cur.fetchall()


def export_attendance_data(conn, teacher_id): 
    cur = conn.cursor() 
    cur.execute(
    """ 
    SELECT 
        s.id,
        s.date,
        st.given_name, 
        st.surname, 
        s.grade_level, 
        s.section, 
        s.subject, 
        s.period, 
        ar.status, 
        ar.minutes_cut, 
        ar.minutes_late 
    FROM attendance_sessions s 
    LEFT JOIN attendance_records ar 
        ON s.id = ar.session_id 
    LEFT JOIN student_accounts st 
        ON ar.student_id = st.id 
    WHERE s.creator_id = ? AND st.id IS NOT NULL
    ORDER BY s.id, st.surname 
    """, 
    (teacher_id,)) 
    
    return cur.fetchall()


# ===== Attendance Marking =====
def get_attendance_marking_info(conn, attendance_id, attendance_grade, attendance_section):
    cur = conn.cursor()
    cur.execute(
    """
    SELECT 
        sa.id,
        sa.given_name,
        sa.surname,
        COALESCE(ar.status, 'Present'),
        COALESCE(ar.minutes_late, 0),
        COALESCE(ar.minutes_cut, 0)
    FROM student_accounts sa
    LEFT JOIN attendance_records ar
        ON sa.id = ar.student_id
        AND ar.session_id = ?
    WHERE sa.grade_level = ?
    AND sa.section = ?
    """,
        (attendance_id, attendance_grade, attendance_section)
    )

    return cur.fetchall()

def check_attendance_record(conn, selected_student_id, attendance_id):
    cur = conn.cursor()
    cur.execute(
    """
    SELECT session_id, student_id
    FROM attendance_records
    WHERE session_id=? AND student_id=?
    """,
        (attendance_id, selected_student_id)
    )

    return cur.fetchone()


def update_attendance_record(
            conn, attendance_punctuality,
            tardy_minutes, cutting_minutes,
            attendance_id, selected_student_id):
    cur = conn.cursor()
    cur.execute(
    """
    UPDATE attendance_records
    SET status=?, minutes_late=?, minutes_cut=?
    WHERE session_id=? AND student_id=?
    """,
        (attendance_punctuality,
        tardy_minutes, 
        cutting_minutes,
        attendance_id, 
        selected_student_id)
    )
    conn.commit()



def search_student_attendance_info(conn, student_id):
    cur = conn.cursor()
    cur.execute(
    """
    SELECT 
    s.id AS session_id,
    s.date,
    s.subject,
    s.period,
    r.status
    FROM attendance_records r
    JOIN attendance_sessions s
        ON r.session_id = s.id
    WHERE r.student_id = ?
    ORDER BY s.date DESC
    """,
        (student_id,)
    )
    return cur.fetchall()


# ===== Settings =====
def delete_all_attendances_made(conn, teacher_id):
    cur = conn.cursor()
    cur.execute(
    """
    DELETE
    FROM attendance_sessions
    WHERE creator_id=?
    """,
        (teacher_id,)
    )
    conn.commit()
# =====         =====


# v0.4.0 

# Create Attendance
def check_duplicate_attendance(conn, attendance_name):
    cur = conn.cursor()

    cur.execute(
        "SELECT 1 FROM attendances WHERE name=?",
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
        WHERE LOWER(attendance_name)=LOWER(?) AND user=?
    """, (attendance_name, user))
    return cur.fetchone()

def record_submission(conn, stored_name, user, current_time, status, late_minutes, response):
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO submissions
        (attendance_name, user, login_time, status, late_minutes, response)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        stored_name,
        user,
        current_time.isoformat(),
        status,
        late_minutes,
        response
    ))
    return

# ========== Settings ==========
# Change Password
def find_current_account_password(conn, user):
    cur = conn.cursor()
    cur.execute("""
        SELECT username, password_hash FROM users
        WHERE username=?
    """, (user,))
    result = cur.fetchone()
    if result is None:
        return None
    return result

def change_account_password(conn, user, hashed_new_password):
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET password_hash=?
        WHERE username=?
    """, (hashed_new_password, user))

    return