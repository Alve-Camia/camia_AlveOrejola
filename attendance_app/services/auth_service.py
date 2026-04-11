#auth_service.py

# ========== Imports ==========
from attendance_app.utils import validators, helpers
from attendance_app.db import user_repo, db
from attendance_app.db.db import get_db
import bcrypt
from datetime import datetime
# =============================


db.init_db()

# ========== Reworked Authentication ==========
# Account Creation
def process_account(
        entered_given_name, entered_surname, 
         entered_password, selected_account_role, 
         selected_grade_level, selected_grade_section, entered_identifier
    ):
    
    error_type, error_message = validators.validate_entered_account_info(
        entered_given_name, entered_surname, 
         entered_password, selected_account_role, 
         selected_grade_level, selected_grade_section, entered_identifier
        )
    
    if error_type:
        return helpers.error_response(error_type, error_message)
    

    if not (selected_grade_level and selected_grade_section):
        selected_grade_level = None
        selected_grade_section = None

    with get_db() as conn:
        
        duplicate_account = user_repo.has_duplicate_account(
            conn, entered_given_name, 
             entered_surname, entered_identifier)
        
        if duplicate_account:
            return helpers.error_response(
                "Input Error", 
                "You cannot register a duplicate account.\nPlease recheck your entered account info, and try again.\nNote: This could come from either a duplicate first name, surname, or identifer.")

        hashed = helpers.hash_password(entered_password).decode("utf-8")
        user_repo.add_account(
            conn, entered_given_name, 
             entered_surname, entered_identifier, hashed,
             selected_account_role, selected_grade_level, 
             selected_grade_section, datetime.now())
        conn.commit()

    return {
        "error_status": False,
        "error_type": "Info",
        "error_message": "Account has been created.\n",
        "data": None
    }

# Login
def process_account_login(entered_password, entered_identifier):
    error_type, error_message = validators.check_login_entries(
        entered_password, entered_identifier
    )
    if error_type:
        return helpers.error_response(error_type, error_message)
    
    with get_db() as conn:
        found_account = user_repo.find_account(conn, entered_identifier)
        if not found_account:
            return helpers.error_response(
                "Input Error",
                "The account name and password do not match.\nPlease recheck your entered inputs, and try again."
            )
        
        authenticated_given_name, authenticated_surname, authenticated_password, authenticated_role = found_account

        authenticated_password = authenticated_password.encode("utf-8")

        if not bcrypt.checkpw(entered_password.encode("utf-8"), authenticated_password):
            return helpers.error_response(
                "Input Error",
                "The account name and password do not match.\nPlease recheck your entered inputs, and try again."
            )
        
        # Log Login
        now = datetime.now()
        user_repo.time_stamp_login(conn, authenticated_given_name, authenticated_surname, now)
        conn.commit()
    return {
        "error_status": False,
        "error_type": None,
        "error_message": None,
        "data": {
            "given_name": authenticated_given_name,
            "surname": authenticated_surname,
            "role": authenticated_role
        }
    }




# v0.4.0 Code
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