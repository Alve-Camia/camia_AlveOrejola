#auth_service.py

# ========== Imports ==========
from datetime import datetime
from typing import Callable, Optional

from ..utils import validators, helpers
from ..db import user_repo, db
from ..db.db import get_db


# =============================

# ========== Reworked Authentication ==========
# Account Creation
def account_registration_processer(registration_info: helpers.AccountRegistration) -> helpers.FieldValidation:
    
    error_type, error_message = validators.validate_entered_account_info(registration_info)
    
    if error_type:
        return helpers.FieldValidation(False, error_type, error_message)

    registration_info.grade_level, registration_info.grade_section = grade_section_defaulter(
        registration_info.grade_level, 
        registration_info.grade_section
    )
        
    duplicate_account = user_repo.has_duplicate_account(registration_info)
        
    if duplicate_account:
        return helpers.FieldValidation(
            False, "Input Error", 
            "You cannot register a duplicate account.\nPlease recheck your entered account info, and try again.\nNote: This could come from either a duplicate first name, surname, or identifer.")
    
    registration_info.password = helpers.hash_password(registration_info.password).decode("utf-8")
    user_repo.add_account(registration_info, datetime.now())

    return helpers.FieldValidation(True, None, None)

def grade_section_defaulter(grade_level, grade_section):
    if not (grade_level and grade_section):
        grade_level = None
        grade_section = None
    
    return grade_level, grade_section
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
        
        authenticated_given_name = found_account[0]
        authenticated_surname = found_account[1]
        authenticated_password = found_account[2]
        authenticated_role = found_account[3]
        authenticated_id = found_account[4]


        if not helpers.check_entered_password(entered_password, authenticated_password):
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
            "role": authenticated_role,
            "id": authenticated_id
        }
    }