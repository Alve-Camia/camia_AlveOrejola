from datetime import datetime

from typing import Callable, Optional
from . import constants, helpers

# validators.py

DATE_FORMAT = "%m-%d-%Y"
TIME_FORMAT = "%H:%M"

# ========== Attendance Logic ==========
# Create Attendance

def attendance_creation_validator(
        entered_attendance_grade, entered_attendance_section,
        entered_attendance_subject, entered_attendance_date,
        entered_attendance_period):
    
    attendance_whitespace_error = check_attendance_whitespace(
        entered_attendance_grade, entered_attendance_section,
        entered_attendance_subject, entered_attendance_date,
        entered_attendance_period)
    
    if attendance_whitespace_error:
        return True, "Input Error", attendance_whitespace_error

    # === Attendance grade needs to be an integer from grade seven to grade twelve. Reason: Grade levels in the school are intergers from 7 - 12 ===
    if not entered_attendance_grade.isdigit():
        return True, "Input Error", "Attendance grade level cannot be a non-digit.\nPlease enter an assigned attendance grade level that is an integer from 7 to 12."

    # Once entered attendance grade level is confimed to be a digit
    entered_attendance_grade = int(entered_attendance_grade)

    if not (7 <= entered_attendance_grade <= 12):
        return True, "Input Error", "Entered attendance grade cannot be less than 7 or greater than 12.\nPlease enter an assigned attendance grade level that is an integer from 7 to 12."    
    
    # === The entered attendance section and subject must be applicable for the entered grade level. ===
    if entered_attendance_section not in constants.POSSIBLE_GRADE_SECTIONS[entered_attendance_grade]:
        return True, "Input Error", "Entered grade level and section do not match.\nPlease ensure that the entered section is under the entered grade level, and try again."
    
    if entered_attendance_subject not in constants.GRADE_SUBJECTS[entered_attendance_grade]:
        return True, "Input Error", "The following entered subject is not under the current grade level chosen.\nPlease choose a subject that is under the chosen grade level."

    # === The enterted attendance date needs to follow MM-DD-YYYY format (for parsing purposes). ===
    if not entered_attendance_date:
        return True, "Input Error", "The assigned attendance date can not be empty\nPlease enter the date of the attendance in MM-DD-YYYY format."

    try:
        entered_attendance_date = datetime.strptime(entered_attendance_date, DATE_FORMAT).date()
        if entered_attendance_date > datetime.now().date():
            return True, "Input Error", "The entered attendance date cannot be past todays date.\nPlease enter an attendance date that is today or from a past date."
    except ValueError:
        return True, "Input Error", "The entered date Please enter start date in MM-DD-YYYY format\n(e.g, 10-01-2025 for October 1, 2025)."

    
    if entered_attendance_date.weekday() >= 5:
        return True, "Input Error", "The entered date can not be a weekend.\nPlease enter an attendace date that is not a weekday."
     
    if not str(entered_attendance_period).isdigit():
        return True, "Input Error", "The attendance period cannot be a non-digit.\nPlease enter an attendance period that is an integer from 1 to 10."
    
    entered_attendance_period = int(entered_attendance_period)

    return False, None, None

def check_attendance_whitespace(entered_attendance_grade, entered_attendance_section,
        entered_attendance_subject, entered_attendance_date,
        entered_attendance_period):

    attendance_fields = {
        "The assigned class section can not be empty.\nPlease assign a class section for the attendance.":
        entered_attendance_section,

        "The assigned subject for an attendance can not be empty.\nPlease assign a subject for the attendance.":
        entered_attendance_subject,

        "The assigned date of the attendance can not be empty.\nPlease assign the relevant attendance date.":
        entered_attendance_date,
    }

    for key, value in attendance_fields.items():
        if not str(value).strip():
            return key

    if not entered_attendance_grade:
        return "The assigned grade level for the attendance can not be empty.\nPlease assign a grade level for the attendance."

    if not entered_attendance_period:
        return "Please assign the relevant attendance period for this attendance."

    return None

# ===== Attendance Marking =====
def validate_attendance_marking(
        selected_student_id, attendance_punctuality, 
        tardy_minutes, cutting_minutes):
    
    if not selected_student_id:
        return "Input Error", "Selected student id cannot be empty\nPlease select a student id to mark."
    
    if not attendance_punctuality:
        return "Input Error", "Selected attendance punctuality for a student can not be empty.\nPlease assign a punctuality status."
    
    
    if attendance_punctuality == "Tardy":
        tardy_input_error, tardy_input_message = validate_tardy_input(tardy_minutes, cutting_minutes)
        if tardy_input_error:
            return tardy_input_error, tardy_input_message


    if attendance_punctuality == "Cutting":
        cutting_input_error, cutting_input_message = validate_cutting_input(tardy_minutes, cutting_minutes)
        if cutting_input_error:
            return cutting_input_error, cutting_input_message
        
    return None, None


def validate_tardy_input(tardy_minutes, cutting_minutes):
    
    if not tardy_minutes:
        return "Input Error", "Tardy status can not have empty tardy minutes\nPlease enter minutes for the tardy status."
    
    if not tardy_minutes.isdigit():
        return "Input Error", "Entered tardy minutes for tardy status can not be a non-digit.\nPlease assign the number of minutes for tardy status."
        
    if int(cutting_minutes) != 0:
        return "Input Error", "Tardy status cannot have both tardy and cutting minutes.\nPlease set cutting minutes to zero."
        
    if not 0 < int(tardy_minutes) <= 50:
        return "Input Error", "Tardy minutes can neither be under 0 minutes, nor can it be more than 50 minutes.\nPlease enter tardy minutes between 0-50 minutes."
    

    return None, None


def validate_cutting_input(tardy_minutes, cutting_minutes):
    
    if not cutting_minutes:
        return "Input Error", "Cutting status can not have empty cutting minutes\nPlease enter minutes for the cutting status."
    
    if not cutting_minutes.isdigit():
        return "Input Error", "Entered cutting minutes for cutting status can not be a non-digit.\nPlease assign the number of minutes for cutting status."

    if int(tardy_minutes) != 0:
        return "Input Error", "Cutting status cannot have both tardy and cutting minutes.\nPlease set tardy minutes to zero."
     
    if not 0 < int(cutting_minutes) <= 50:
        return "Input Error", "Cutting minutes can neither be under 0 minutes, nor can it be more than 50 minutes.\nPlease enter cutting minutes between 0-50 minutes."


    return None, None

# ========== Authentication Logic ==========

#v0.5.0 

# Account Login
def check_login_entries(entered_password, entered_identifier):
    if not entered_password.strip():
        return "Input Error", "Entered password can not be empty\nPlease enter password."
    if not entered_identifier.strip():
        return "Input Error", "Entered identifier can not be empty\nPlease enter your account identifier."
    return None, None


# Account Creation
def validate_entered_account_info(
        registration_info: helpers.AccountRegistration
    ) -> tuple[str | None, str | None]:
    
    # Given Name
    if not registration_info.given_name.strip():
        return "Input Error", "Given name cannot be empty.\nPlease enter given name."
    
    if not registration_info.given_name.strip() or not all(c.isalpha() or c.isspace() for c in registration_info.given_name):
        return "Input Error", "Given name can not contain non-letters or non-spaces.\nPlease enter a given name with only letters and spaces."

    # Surname
    if not registration_info.surname.strip():
        return "Input Error", "Surname cannot be empty.\nPlease enter surname."
    
    if not registration_info.surname.strip() or not all(c.isalpha() or c.isspace() for c in registration_info.surname):
        return "Input Error", "Surname can not contain non-letters or non-spaces.\nPlease enter a surname with only letters and spaces."

    # Password
    if len(registration_info.password) < 10 or len(registration_info.password) > 100:
        return "Input Error", "Password has too few/little characters.\nPlease enter a password with 10-100 characters."

    # Selected Account role
    if not registration_info.role or registration_info.role.strip().lower() not in ("student", "teacher"):
        return "Input Error", "Selected account role cannot be empty.\nPlease select an account role."
    
    if not registration_info.identifier.strip():
        return "Input Error", "Entered Account username cannot be empty\nPlease enter an account username."

    # Grade Level and Section
    if registration_info.grade_level and registration_info.grade_section:
        if registration_info.grade_section not in constants.POSSIBLE_GRADE_SECTIONS[int(registration_info.grade_level)]:
            return "Input Error", "Selected grade level and section do not match.\nPlease ensure that selected grade level and section match, and try again."

    return None, None



