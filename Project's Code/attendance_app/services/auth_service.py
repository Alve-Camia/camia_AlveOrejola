#auth_service.py

# ========== Imports ==========

# Standard Library
from datetime import datetime

# Third Party


# Code Files
from ..utils import validators, helpers, constants
from ..db import user_repo

# =============================

# ========== Reworked Authentication ==========
# ===== Account Creation =====
def account_registration_processer(registration_info: helpers.AccountRegistration) -> helpers.FieldValidation:
    
    validator_error_status, validator_error_message = validators.validate_entered_account_info(registration_info)
    

    if validator_error_status:
        return helpers.FieldValidation(False, constants.INPUT_ERROR, validator_error_message)

    registration_info.grade_level, registration_info.grade_section = grade_section_defaulter(
        registration_info.grade_level, 
        registration_info.grade_section
    )
        
    duplicate_account = user_repo.has_duplicate_account(registration_info)
        
    if duplicate_account:
        return helpers.FieldValidation(
            False, constants.INPUT_ERROR,
            constants.DUPLICATE_ACCOUNT_ERROR_MESSAGE)
    
    
    registration_info.password = helpers.hash_password(registration_info.password).decode("utf-8")
    user_repo.add_account(registration_info, datetime.now())

    return helpers.FieldValidation(True, None, None)

def grade_section_defaulter(grade_level, grade_section):
    
    if not (grade_level and grade_section):
        grade_level = None
        grade_section = None
    
    return grade_level, grade_section


# ===== Login =====
def process_account_login(
        entered_password, 
        entered_identifier
    ) -> tuple[helpers.FieldValidation, helpers.LoginSessionInfo | None]:
    
    error_type, error_message = validators.check_login_entries(entered_password, entered_identifier)
    if error_type:
        return helpers.FieldValidation(False, error_type, error_message), None
    
    found_account = user_repo.find_account(entered_identifier)
    if not found_account:
        return helpers.FieldValidation(
            False,
            constants.INPUT_ERROR,
            constants.NOT_PASSWORD_MATCH_ERROR_MESSAGE
        ), None
        
    authenticated_given_name = found_account[0]
    authenticated_surname = found_account[1]
    authenticated_password = found_account[2]
    authenticated_role = found_account[3]
    authenticated_id = found_account[4]

    if not helpers.check_entered_password(entered_password, authenticated_password):
        
        return helpers.FieldValidation(
            False,
            constants.INPUT_ERROR,
            constants.NOT_PASSWORD_MATCH_ERROR_MESSAGE
        ), None


    now = datetime.now()
    user_repo.time_stamp_login(authenticated_given_name, authenticated_surname, now)
    
    # Track User's Session Info
    authenticated_account_info = helpers.LoginSessionInfo(
        authenticated_id, authenticated_given_name,
        authenticated_surname, authenticated_role    
    )

    return helpers.FieldValidation(True, None, None), authenticated_account_info