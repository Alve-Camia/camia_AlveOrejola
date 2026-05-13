from typing import Callable, Optional
from datetime import datetime

from . import db
from ..utils import helpers
# ========== Authentication ==========
# ===== v0.5.0 =====
# Account Creation
def has_duplicate_account(registration_info: helpers.AccountRegistration) -> tuple | None:
    
    with db.get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT given_name, surname, login_id
            FROM student_accounts 
            WHERE LOWER(given_name)=LOWER(?) AND LOWER(surname)=LOWER(?) AND LOWER(login_id)=LOWER(?)
        """, (
        registration_info.given_name, 
        registration_info.surname, 
        registration_info.identifier
        ))
        
        row = cur.fetchone()
        if row:
            return row

        cur.execute("""
            SELECT given_name, surname 
            FROM teacher_accounts 
            WHERE LOWER(given_name)=LOWER(?) AND LOWER(surname)=LOWER(?) AND LOWER(login_id)=LOWER(?)
        """, (
        registration_info.given_name, 
        registration_info.surname, 
        registration_info.identifier
        ))
        
        row = cur.fetchone()
        if row:        
            return row


def add_account(
        registration_info: helpers.AccountRegistration,
        now: datetime) -> None:
    
    with db.get_db() as conn:
        cur = conn.cursor()

        if registration_info.role == "Student":
            cur.execute(
            """
            INSERT INTO student_accounts
            (given_name, surname, login_id, password_hash, role, grade_level, section, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, 
            (
            registration_info.given_name,
            registration_info.surname,
            registration_info.identifier,
            registration_info.password,
            registration_info.role,
            registration_info.grade_level,
            registration_info.grade_section,
            now
            ))

        else:
            cur.execute(
            """
            INSERT INTO teacher_accounts
            (given_name, surname, login_id, password_hash, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
            registration_info.given_name,
            registration_info.surname,
            registration_info.identifier,
            registration_info.password,
            registration_info.role,
            now
            ))

# Login Account
def find_account(conn, entered_identifier):
    cur = conn.cursor()
    cur.execute("""
        SELECT given_name, surname, password_hash, role, id
        FROM student_accounts 
        WHERE LOWER(login_id)=LOWER(?)
    """, (entered_identifier,))

    row = cur.fetchone()
    if row:
        return row

    cur.execute("""
        SELECT given_name, surname, password_hash, role, id
        FROM teacher_accounts 
        WHERE LOWER(login_id)=LOWER(?)
    """, (entered_identifier,))
    
    row = cur.fetchone()
    if row:
        return row

def time_stamp_login(conn, authenticated_given_name, authenticated_surname, now):
    cur = conn.cursor()
    cur.execute(
            "INSERT INTO account_logins (given_name, surname, timestamp) VALUES (?, ?, ?)",
            (authenticated_given_name, authenticated_surname, now)
    )
    return
