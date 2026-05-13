import sqlite3
import pandas as pd
from . import db

# ========== Attendance Microservice ===========

# ===== Create Attendance =====
def check_duplicate_attendance(
        entered_attendance_grade, entered_attendance_section,
        entered_attendance_subject, entered_attendance_date,
        entered_attendance_period):
    
    with db.get_db() as conn:
        cur = conn.cursor()

        cur = conn.cursor()
        cur.execute(
        """
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
            attendance_grade_level, attendance_section, 
            attendance_subject, attendance_date, 
            attendance_period, current_user_id, 
            now
        ):
    with db.get_db() as conn:
        cur = conn.cursor()
        cur.execute(
        """
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

        conn.commit()

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

def insert_attendance_record(attendance_id, student_id):
    with db.get_db() as conn:
        cur = conn.cursor()
        cur.execute(
        """
        INSERT INTO attendance_records 
        (session_id, student_id, status)
        VALUES (?, ?, ?)    
        """,
        (attendance_id, student_id, 'Present'))

# ==== Attendance Marking =====
def get_dashboard_table_info(creator_id):
    with db.get_db() as conn:
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


def get_authenticated_attendance_records(attendance_id, attendance_grade, attendance_section):
    with db.get_db() as conn:
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


def check_attendance_record(selected_student_id, attendance_id):
    with db.get_db() as conn:
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
            attendance_punctuality, tardy_minutes, 
            cutting_minutes, attendance_id, 
            selected_student_id):
    
    with db.get_db() as conn:
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

# ===== Student Attendances =====
def search_student_attendance_info(student_id):
    with db.get_db() as conn:
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

# ===== Export Attendance Data =====
def export_dashboard_csv(teacher_id, current_datetime):

    try:
        with db.get_db() as conn:
            data = db.export_attendance_data(conn, teacher_id)
    except sqlite3.IntegrityError as error_message:
        return "Database Error", f"Integrity Error: {str(error_message)}\nPlease try again later."
    except sqlite3.OperationalError as error_message:
        return "Databse Error", f"Operational Error: {str(error_message)}\nPlease try again later."
    
    if not data:
        return "Export Error", "No data available."

    columns = [
        "Session ID",
        "Date",
        "First Name",
        "Surname",
        "Grade",
        "Section",
        "Subject",
        "Period",
        "Status",
        "Minutes Cut",
        "Minutes Late"
    ]

    df = pd.DataFrame(data, columns=columns)
    df.to_csv(f"attendance_export - {current_datetime}.csv", index=False)

    return None, None

# ===== Attendance Settings =====
def delete_all_attendances_made(conn, teacher_id):
    with db.get_db() as conn:
        cur = conn.cursor()
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