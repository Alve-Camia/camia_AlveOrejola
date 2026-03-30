# ========== Authentication ==========
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