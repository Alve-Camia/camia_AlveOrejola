from . import db

db.init_db()

# ===== Attendance Microservice ======
# Create Attendance
def check_duplicate_attendance(
        entered_attendance_grade, entered_attendance_section,
        entered_attendance_subject, entered_attendance_date,
        entered_attendance_period, conn):
    
    cur = conn.cursor()

    cur = conn.cursor()
    cur.execute("""
        SELECT grade_level, section, subject, period, date
        FROM attendance_sessions
        WHERE grade_level=? AND LOWER(section)=LOWER(?) AND LOWER(subject)=LOWER(?) AND date=? AND period=?
    """, 
    (entered_attendance_grade, 
    entered_attendance_section, 
    entered_attendance_subject, 
    entered_attendance_date,
    entered_attendance_period))
        
    row = cur.fetchone()
    if row:
        return row
    
def insert_attendance_session(
            conn, attendance_grade_level, 
            attendance_section, attendance_subject,
            attendance_date, attendance_period,
            current_user_id, now
        ):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO attendance_sessions 
        (grade_level, section, subject, period, date, created_at, creator_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    
    """, 
    (attendance_grade_level,
     attendance_section,
     attendance_subject,
     attendance_period,
     attendance_date,
     now,
     current_user_id
    ))

    cur.execute("""
        SELECT id
        FROM attendance_sessions
        WHERE grade_level=? 
        AND LOWER(section)=LOWER(?) 
        AND LOWER(subject)=LOWER(?) 
        AND period=? 
        AND date=? 
    """,
    (attendance_grade_level, attendance_section, 
    attendance_subject, attendance_period, 
    attendance_date))

    attendance_id = cur.fetchone()[0]
    
    cur.execute("""
        SELECT id
        FROM student_accounts
        WHERE grade_level=? AND LOWER(section)=LOWER(?)
    """,
    (attendance_grade_level, attendance_section,))
    
    student_ids = cur.fetchall()

    return attendance_id, student_ids

def insert_attendance_record(conn, attendance_id, student_id):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO attendance_records 
        (session_id, student_id, status)
        VALUES (?, ?, ?)
        
    """,
    (attendance_id, student_id, 'Present'))