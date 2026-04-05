
# ========== Authentication ==========
# ===== v0.5.0 =====
# Account Creation
def has_duplicate_account(conn, entered_given_name, entered_surname, selected_account_role):
    if selected_account_role == "Student":
        cur = conn.cursor()
        cur.execute("""
            SELECT given_name, surname 
            FROM student_accounts 
            WHERE LOWER(given_name)=LOWER(?) AND LOWER(surname)=LOWER(?)
        """, (entered_given_name, entered_surname))
        
        row = cur.fetchone()
        return row

    if selected_account_role == "Teacher":
        cur.execute("""
            SELECT given_name, surname 
            FROM teacher_accounts 
            WHERE LOWER(given_name)=LOWER(?) AND LOWER(surname)=LOWER(?)
        """, (entered_given_name, entered_surname))
        
        row = cur.fetchone()
        return row


def add_account(
        conn, given_name, 
        surname, hashed_password, 
        account_role, grade_level, 
        grade_section, now):
    cur = conn.cursor()

    if account_role == "Student":
        cur.execute("""
            INSERT INTO student_accounts
            (given_name, surname, password_hash, role, grade_level, section, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            given_name,
            surname,
            hashed_password,
            account_role,
            grade_level,
            grade_section,
            now
        ))

    else:
        cur.execute("""
            INSERT INTO teacher_accounts
            (given_name, surname, password_hash, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            given_name,
            surname,
            hashed_password,
            account_role,
            now
        ))

# Login Account
def find_account(conn, entered_given_name, entered_surname):
    cur = conn.cursor()
    cur.execute("""
        SELECT given_name, surname, password_hash, role
        FROM student_accounts 
        WHERE LOWER(given_name)=LOWER(?) AND LOWER(surname)=LOWER(?)
    """, (entered_given_name, entered_surname))

    row = cur.fetchone()
    return row


# ===== v0.4.0 =====
def time_stamp_login(conn, authenticated_given_name, authenticated_surname, now):
    cur = conn.cursor()
    cur.execute(
            "INSERT INTO account_logins (given_name, surname, timestamp) VALUES (?, ?, ?)",
            (authenticated_given_name, authenticated_surname, now)
    )
    return


# ===== Login =====
def timestamp(conn, username, login_time):
    cur = conn.cursor()
    cur.execute(
            "INSERT INTO login_logs (user, timestamp) VALUES (?, ?)",
            (username, login_time.isoformat())
    )
    return

def find_user(conn, username):
    cur = conn.cursor()
    cur.execute(
        "SELECT username, password_hash FROM users WHERE username=?",
        (username,)
    )

    row = cur.fetchone()
    return row

# ===== Signup =====
def check_duplicate_user(conn, username):
    cur = conn.cursor()

    cur.execute(
        "SELECT 1 FROM users WHERE username=?",
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
