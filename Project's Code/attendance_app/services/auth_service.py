#auth_service.py

# ========== Imports ==========
from attendance_app.utils import validators, helpers
from attendance_app.db import user_repo, db
from attendance_app.db.db import get_db
import bcrypt
from datetime import datetime
# =============================


db.init_db()

# ========== Authentication ==========
# Sign up
def check_and_add_user(username, password):
    signup_error, signup_message = validators.validate_signup_input(username, password)
    if signup_error:
        return True, signup_error, signup_message

    with get_db() as conn: 

        if user_repo.check_duplicate_user(conn, username):
            return True, "Input Error", "The entered username is not available.\nPlease choose another username."

        hashed = helpers.hash_password(password).decode("utf-8")

        user_repo.add_user(conn, username, hashed)
        conn.commit()
    
    return False, "Success", "Sign Up Successful"

# 
def process_login(username, password):
    
    login_input_error, login_input_message = validators.validate_login_input(username, password)
    if login_input_error:
        return True, login_input_error, login_input_message, None
        
    with get_db() as conn:
        
        row = user_repo.find_user(conn, username)

        if not row:
            return True, "Input Error", "Invalid username or password.""\nPlease try again.", None

        stored_username, stored_hash = row

        stored_hash = stored_hash.encode("utf-8")

        if not bcrypt.checkpw(password.encode("utf-8"), stored_hash):
            return True, "Error", "Invalid username or password.\nPlease try again.", None

        # Log login
        now = datetime.now()
        user_repo.timestamp(conn, username, now)
        conn.commit()
    
    return False, "", "", stored_username