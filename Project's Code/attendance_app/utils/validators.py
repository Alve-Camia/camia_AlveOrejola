# =========================
# Imports

# Standard Library
from datetime import datetime
import re

# Third-Party

# Code Files
from . import constants, helpers
# =========================

# validators.py

# ========== Attendance Logic ==========
# Create Attendance

def attendance_creation_validator(
        created_attendance_info: helpers.AttendanceSessionInfo
    ) -> tuple[bool, str | None, str | None]:
    
    """
    TODO: There should be probably be consideration of Memorandum No.
    012, s. 2026 - Energy Conservation Measures
    """

    attendance_info_field_validators = [
        validate_attendance_grade_level,
        validate_attendance_grade_section,
        validate_attendance_subject,
        validate_attendance_period,
        validate_attendance_date,
        validate_attendance_creator_id
    ]

    for field_validator in attendance_info_field_validators:
        
        is_error, error_type, error_message = field_validator(created_attendance_info)

        if is_error:
            return True, error_type, error_message
        
    return False, None, None



def check_attendance_whitespace(
        created_attendance_info: helpers.AttendanceSessionInfo
    ) -> str | None:

    attendance_fields = (
        (created_attendance_info.grade_section, 
        constants.EMPTY_ATTENDANCE_GRADE_SECTION),

        (created_attendance_info.subject,
        constants.EMPTY_ATTENDANCE_SUBJECT),

        (created_attendance_info.date,
        constants.EMPTY_ATTENDANCE_DATE),

        (created_attendance_info.grade_level,
        constants.EMPTY_ATTENDANCE_GRADE_LEVEL),

        (created_attendance_info.period,
        constants.EMPTY_ATTENDANCE_PERIOD)
    )

    for field, empty_field_error_message in attendance_fields:
        if not str(field).strip():
            return empty_field_error_message
    
    return None


def validate_attendance_grade_level(
        created_attendance_info: helpers.AttendanceSessionInfo
    ) -> helpers.FieldValidation:

    if not str(created_attendance_info.grade_level).strip():
        return True, constants.INPUT_ERROR, constants.EMPTY_ATTENDANCE_GRADE_LEVEL

    if not created_attendance_info.grade_level.isdigit():
        return True, constants.INPUT_ERROR, constants.NON_DIGIT_ATTENDANCE_GRADE_LEVEL

    created_attendance_info.grade_level = int(created_attendance_info.grade_level)

    # This range is because of the school supporting junior and senior grade levels only.
    if not (7 <= created_attendance_info.grade_level <= 12):
        return True, constants.INPUT_ERROR, constants.OUT_OF_RANGE_ATTENDANCE_GRADE_LEVEL
    
    return False, None, None

def validate_attendance_grade_section(
        created_attendance_info: helpers.AttendanceSessionInfo
    ) -> helpers.FieldValidation:


    if not str(created_attendance_info.grade_section).strip():
        return True, constants.INPUT_ERROR, constants.EMPTY_ATTENDANCE_GRADE_SECTION

    # This is temporarily here
    if not str(created_attendance_info.grade_level).strip():
        return True, constants.INPUT_ERROR, constants.EMPTY_ATTENDANCE_GRADE_LEVEL
    
    if created_attendance_info.grade_section not in constants.POSSIBLE_GRADE_SECTIONS[int(created_attendance_info.grade_level)]:
        return True, constants.INPUT_ERROR, constants.NOT_GRADE_SECTION_MATCH_MESSAGE
    
    return False, None, None

def validate_attendance_subject(
        created_attendance_info: helpers.AttendanceSessionInfo
    ) -> helpers.FieldValidation:

    if not str(created_attendance_info.subject).strip():
        return True, constants.INPUT_ERROR, constants.EMPTY_ATTENDANCE_SUBJECT
    
    if created_attendance_info.subject not in constants.GRADE_SUBJECTS[created_attendance_info.grade_level]:
        return True, constants.INPUT_ERROR, constants.NOT_GRADE_SUBJECT_MATCH_MESSAGE
    
    return False, None, None

def validate_attendance_date(
        created_attendance_info: helpers.AttendanceSessionInfo
    ) -> tuple[bool, str | None, str | None]:

    if not str(created_attendance_info.date).strip():
        return True, constants.INPUT_ERROR, constants.EMPTY_ATTENDANCE_DATE

    try:
        parsed_attendance_date = datetime.strptime(created_attendance_info.date, constants.DATE_FORMAT).date()
        if parsed_attendance_date > datetime.now().date():
            return True, constants.INPUT_ERROR, constants.INVALID_FUTURE_ATTENDANCE_DATE_MESSAGE
    except ValueError:
        return True, constants.INPUT_ERROR, constants.INVALID_ATTENDANCE_DATE_FORMAT_MESSAGE
    
    if parsed_attendance_date.weekday() >= 5:
        return True, constants.INPUT_ERROR, constants.INVALID_ATTENDANCE_DATE_WEEKEND_MESSAGE
    
    is_grade_7_class = created_attendance_info.grade_level == 7
    is_grade_8_class = created_attendance_info.grade_level == 8
    is_grade_9_class = created_attendance_info.grade_level == 9
    is_grade_10_class = created_attendance_info.grade_level == 10

    if parsed_attendance_date.weekday() == 4 and (is_grade_7_class or is_grade_8_class):
        return True, constants.INPUT_ERROR, constants.ASYNCHRONUS_CLASSES_GRADE_7_8
    
    if parsed_attendance_date.weekday() == 4 and int(created_attendance_info.period) >= 6 and (is_grade_9_class or is_grade_10_class):
        return True, constants.INPUT_ERROR, constants.ASYNCHRONUS_CLASSES_GRADE_9_10


    return False, None, None

def validate_attendance_period(
        created_attendance_info: helpers.AttendanceSessionInfo
    ) -> tuple[bool, str | None, str | None]:

    if not str(created_attendance_info.period).strip():
        return True, constants.INPUT_ERROR, constants.EMPTY_ATTENDANCE_PERIOD
    
    if not str(created_attendance_info.period).isdigit():
        return True, constants.INPUT_ERROR, constants.NON_DIGIT_ATTENDANCE_PERIOD
    
    created_attendance_info.period = int(created_attendance_info.period)

    if not (1 <= created_attendance_info.period <= 10):
        return True, constants.INPUT_ERROR, constants.OUT_OF_RANGE_ATTENDANCE_PERIOD

    return False, None, None

def validate_attendance_creator_id(
        created_attendance_info: helpers.AttendanceSessionInfo
    ) -> helpers.FieldValidation:
    
    if not created_attendance_info.creator_id:
        return True, constants.AUTH_ERROR, constants.EMPTY_ATTENDANCE_ACCOUNT_ID

    return False, None, None
# =======================


# ===== Attendance Marking =====
def validate_attendance_marking(
        attendance_marking_info: helpers.AttendanceMarkingInfo
    ) -> tuple[str | None, str | None]:
    
    if not attendance_marking_info.student_id.strip():
        return constants.INPUT_ERROR, constants.EMPTY_SELECTED_STUDENT_ID
    
    if not attendance_marking_info.attendance_id:
        return constants.INPUT_ERROR, constants.EMPTY_ATTENDANCE_MARKING_ID

    if not attendance_marking_info.punctuality_status.strip():
        return constants.INPUT_ERROR, constants.EMPTY_SELECTED_STUDENT_PUNCTUALITY
    
    if attendance_marking_info.punctuality_status.lower() not in constants.POSSIBLE_ATTENDANCE_PUNCTUALITIES:
        return constants.INPUT_ERROR, constants.INVALID_ATTENDANCE_PUNCTUALITY_SELECTED

    is_selected_tardy_punctuality = (
        attendance_marking_info.punctuality_status.lower() == 
        constants.TARDY_STATUS.lower()
    )
    
    tardy_input_error, tardy_input_message = validate_tardy_input(
        is_selected_tardy_punctuality, attendance_marking_info
    )
    if tardy_input_error:
        return tardy_input_error, tardy_input_message


    is_selected_cutting_punctuality = (
        attendance_marking_info.punctuality_status.lower() == 
        constants.CUTTING_STATUS.lower()
    )

    cutting_input_error, cutting_input_message = validate_cutting_input(
        is_selected_cutting_punctuality, attendance_marking_info
    )
    if cutting_input_error:
        return cutting_input_error, cutting_input_message
    
    is_student_present_absent = is_assigned_present_absent(attendance_marking_info)
    is_alloted_truancy_minutes = tardy_cutting_occurence(attendance_marking_info)
    
    if is_student_present_absent and is_alloted_truancy_minutes:
        return constants.INPUT_ERROR, constants.NOT_PUNCTUALITY_TRUANCY_MINUTES_MATCH


    return None, None

def is_assigned_present_absent(
        attendance_marking_info: helpers.AttendanceMarkingInfo
    ) -> bool:

    # NOTE: The following docstringed LoC (lines of code) are for debugging purposes

    is_selected_student_present = attendance_marking_info.punctuality_status == constants.PRESENT_STATUS
    
    """
    print(f"Is alloted present punctuality ? : {is_selected_student_present}")
    """

    is_selected_student_absent = attendance_marking_info.punctuality_status == constants.ABSENT_STATUS
    
    """
    print(f"Is alloted absent punctualuty {is_selected_student_absent}")
    """

    is_expected_cutting_tardy_minutes = is_selected_student_present or is_selected_student_absent
    return is_expected_cutting_tardy_minutes


def tardy_cutting_occurence(
        attendance_marking_info: helpers.AttendanceMarkingInfo
    ) -> bool:
    # NOTE: The following docstringed LoC (lines of code) are for debugging purposes.

    
    is_inputted_tardy_minutes = attendance_marking_info.tardy_minutes != 0
    
    """
    print(f"Data type of tardy minutes: {type(attendance_marking_info.tardy_minutes)} ")
    print(f"What is the value of tardy minutes ? : {attendance_marking_info.tardy_minutes}")
    print(f"Is there alloted tardy minutes ? : {is_inputted_tardy_minutes} ")
    print()
    """
    is_inputted_cutting_minutes = attendance_marking_info.cutting_minutes != 0

    """
    print(f"Data type of cutting minutes: {type(attendance_marking_info.cutting_minutes)} ")
    print(f"What is the value of cutting minutes ? : {attendance_marking_info.cutting_minutes}")
    print(f"Is there alloted cutting minutes ? : {is_inputted_cutting_minutes} ")
    print()
    """

    return (is_inputted_tardy_minutes or is_inputted_cutting_minutes)


def validate_tardy_input(
        is_selected_tardy_punctuality: bool,
        attendance_marking_info: helpers.AttendanceMarkingInfo
    ) -> tuple[str | None, str | NotImplementedError]:
    
    if not is_selected_tardy_punctuality:
        return None, None
    
    if not attendance_marking_info.tardy_minutes:
        return constants.INPUT_ERROR,  constants.EMPTY_TARDY_MINUTES

    if not attendance_marking_info.tardy_minutes.isdigit():
        return constants.INPUT_ERROR, constants.NON_DIGIT_TARDY_MINUTES
    
    if not attendance_marking_info.cutting_minutes.isdigit():
        return constants.INPUT_ERROR, constants.NON_DIGIT_CUTTING_MINUTES
    
    if int(attendance_marking_info.cutting_minutes) != 0:
        return constants.INPUT_ERROR, constants.BOTH_TARDY_CUTTING_ENTRY_ERROR
    
    if not 0 < int(attendance_marking_info.tardy_minutes) <= 50:
        return constants.INPUT_ERROR, constants.INVALID_TARDY_MINUTES_RANGE
        
    return None, None


def validate_cutting_input(
        is_selected_cutting_punctuality: bool,
        attendance_marking_info: helpers.AttendanceMarkingInfo
    ) -> tuple[str | None, str | NotImplementedError]:
    
    if not is_selected_cutting_punctuality:
        return None, None

    if not attendance_marking_info.cutting_minutes:
        return constants.INPUT_ERROR, constants.EMPTY_CUTTING_MINUTES
    
    if not attendance_marking_info.cutting_minutes.isdigit():
        return constants.INPUT_ERROR, constants.NON_DIGIT_CUTTING_MINUTES

    if not attendance_marking_info.tardy_minutes.isdigit():
        return constants.INPUT_ERROR, constants.NON_DIGIT_TARDY_MINUTES

    if int(attendance_marking_info.tardy_minutes) != 0:
        return constants.INPUT_ERROR, constants.BOTH_TARDY_CUTTING_ENTRY_ERROR
    
    if not 0 < int(attendance_marking_info.cutting_minutes) <= 50:
        return constants.INPUT_ERROR, constants.INVALID_CUTTING_MINUTES_RANGE

    return None, None

# ========== Authentication Logic ==========

# Account Login
def check_login_entries(entered_password, entered_identifier):

    if not entered_identifier.strip():
        return constants.INPUT_ERROR, constants.EMPTY_USERNAME_MESSAGE
    if not entered_password.strip():
        return constants.INPUT_ERROR, constants.EMPTY_LOGIN_PASSWORD
    
    return None, None


# Account Creation
def validate_entered_account_info(
        registration_info: helpers.AccountRegistration
    ) -> tuple[str | None, str | None]:
    
    """
    TODO:
    Block nonsensical, malicious, or troll:
    - First Names
    - Surnames
    - Usernames
    """
    account_registration_field_validators = [
        validate_account_given_name,
        validate_account_surname,
        validate_account_username,
        validate_account_role,
        validate_account_grade_level_section,
        validate_account_password
    ]

    for field_validator in account_registration_field_validators:
        error_status, error_message = field_validator(registration_info)
        if error_status:
            return error_status, error_message

    return False, None

def validate_account_given_name(
    registration_info: helpers.AccountRegistration
) -> tuple[bool, str | None]:

    if not registration_info.given_name.strip():
        return True, constants.EMPTY_GIVEN_NAME_MESSAGE
    
    if not registration_info.given_name.strip() or not re.match(r"^[a-zA-Z\u00C0-\u017F\s\-']+$", registration_info.given_name):
        return True, constants.INVALID_FIRST_NAME_MESSAGE
    
    if not (2 <= len(registration_info.given_name) <= 70):
        return True, constants.GIVEN_NAME_LENGTH_OUT_OF_RANGE
    
    no_space_lowercased_given_name = registration_info.given_name.lower().replace(" ", "")
    
    for banned_account_word in constants.BANNED_ACCOUNT_WORDS:
        if banned_account_word in no_space_lowercased_given_name:
            return True, f"Entered given name has been flagged for being potentially nonsensical\nReason: Using '{banned_account_word}' in given name\n\nPlease change the entered given name to a more appropriate one."

    return False, None
    

def validate_account_surname(
    registration_info: helpers.AccountRegistration
) -> tuple[bool, str | None]:

    if not registration_info.surname.strip():
        return True, constants.EMPTY_SURNAME_MESSAGE

    if not registration_info.surname.strip() or not re.match(r"^[a-zA-Z\u00C0-\u017F\s\-']+$", registration_info.surname):
        return True, constants.INVALID_SURNAME_MESSAGE

    if not (2 <= len(registration_info.surname) <= 70):
        return True, constants.SURNAME_LENGTH_OUT_OF_RANGE
    
    no_space_lowercased_surname = registration_info.surname.lower().replace(" ", "")
    
    for banned_account_word in constants.BANNED_ACCOUNT_WORDS:
        if banned_account_word in no_space_lowercased_surname:
            return True, f"Entered surname has been flagged for being potentially nonsensical\nReason: Using '{banned_account_word}' in surname\n\nPlease change the entered surname to a more appropriate one."
    
    return False, None


def validate_account_username(
    registration_info: helpers.AccountRegistration
) -> tuple[bool, str | None]:

    if not registration_info.identifier.strip():
        return True, constants.EMPTY_USERNAME_MESSAGE
    
    if not (3 <= len(registration_info.identifier) <= 30):
        return True, constants.USERNAME_OUT_OF_RANGE
    
    no_space_lowercased_username = registration_info.identifier.lower().replace(" ", "")

    for banned_username_word in constants.BANNED_ACCOUNT_WORDS:
        if banned_username_word in no_space_lowercased_username:
            return True, f"Entered account username has been flagged for being inappropriate.\nReason: Using '{banned_username_word}' in the username.\n\nPlease change your username."
    
    return False, None

def validate_account_role(
    registration_info: helpers.AccountRegistration
) -> tuple[bool, str | None]:

    if not registration_info.role.strip():
        return True, constants.EMPTY_ROLE_MESSAGE
    
    if registration_info.role.strip().lower() not in constants.ALLOWED_ACCOUNT_ROLES:
        return True, constants.NOT_APPLICABLE_ROLE_ERROR
    
    return False, None

def validate_account_grade_level_section(
    registration_info: helpers.AccountRegistration
) -> tuple[bool, str | None]:
    
    is_registration_student_account = registration_info.role.strip().lower() == constants.STUDENT_ACCOUNT_STATUS
    
    if is_registration_student_account:
        account_grade_section_mismatch = registration_info.grade_section not in constants.POSSIBLE_GRADE_SECTIONS[int(registration_info.grade_level)]

    if is_registration_student_account and (not registration_info.grade_level.strip()):
        return True, constants.EMPTY_STUDENT_GRADE_LEVEL
    
    if is_registration_student_account and (not registration_info.grade_section.strip()):
        return True, constants.EMPTY_STUDENT_GRADE_SECTION
    
    if is_registration_student_account and account_grade_section_mismatch:
        return True, constants.NOT_GRADE_SECTION_MATCH_MESSAGE
    
    return False, None

def validate_account_password(
    registration_info: helpers.AccountRegistration
) -> tuple[bool, str | None]:
    
    if len(registration_info.password) < 10 or len(registration_info.password) > 100:
        return True, constants.INVALID_PASSWORD_LENGTH_MESSAGE
    
    return False, None