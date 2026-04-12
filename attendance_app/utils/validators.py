from datetime import datetime
from . import constants

# validators.py

DATE_FORMAT = "%m-%d-%Y"
TIME_FORMAT = "%H:%M"

# ========== Attendance Logic ==========
# Create Attendance

def attendance_creation_validator(
        entered_attendance_grade, entered_attendance_section,
        entered_attendance_subject, entered_attendance_date,
        entered_attendance_period, creator_given_name,
        creator_surname):
    
    possible_grade_sections = {
        7: ("Emerald", "Diamond", "Ruby"),
        8: ("Camia", "Jasmine", "Sampaguita"),
        9: ("Potassium", "Rubidium", "Sodium"),
        10: ("Electron", "Neutron", "Proton"),
        11: ("A", "B", "C"),
        12: ("A", "B", "C")
    }

    
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

    if not (7 < int(entered_attendance_grade) < 12):
        return True, "Input Error", "Entered attendance grade cannot be less than 7 or greater than 12.\nPlease enter an assigned attendance grade level that is an integer from 7 to 12."    
    
    # === The entered attendance section and subject must be applicable for the entered grade level. ===
    if entered_attendance_section not in possible_grade_sections[entered_attendance_grade]:
        return True, "Input Error", "Entered grade level and section do not match.", "Please ensure that the entered section is under the entered grade level, and try again."
    
    if entered_attendance_subject not in constants.GRADE_SUBJECTS[entered_attendance_grade]:
        return True, "Input Error", "The following entered subject is not under the current grade level chosen.\nPlease choose a subject that is under the chosen grade level."

    # === The enterted attendance date needs to follow MM-DD-YYYY format (for parsing purposes). ===
    if not entered_attendance_date:
        return True, "Input Error", "The assigned attendance date can not be empty\nPlease enter the date of the attendance in MM-DD-YYYY format."

    try:
        entered_attendance_date = datetime.strptime(entered_attendance_date, DATE_FORMAT).date()
        if entered_attendance_date > datetime.now().date():
            return True, "Input Error", "The entered attendance date cannot be past todays date.\nPlease enter an attendance date that is today or from a past date"
    except ValueError:
        return True, "Input Error", "The entered date Please enter start date in MM-DD-YYYY format\n(e.g, 10-01-2025 for October 1, 2025)."

    if not entered_attendance_period.isdigit():
        return True, "Input Error", "The attendance period cannot be a non-digit.\nPlease enter an attendance period that is an integer from 1 to 10."
    
    entered_attendance_period = int(entered_attendance_period)

    if not creator_given_name or not creator_surname:
        return True, constants.AUTH_ERROR, "There was no account detected when you logged in to the app. Please log out of the app and log back in to further continue."


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
        if not value.strip():
            return key

    if not entered_attendance_grade:
        return "The assigned grade level for the attendance can not be empty.\nPlease assign a grade level for the attendance."

    if not entered_attendance_period:
        return "Please assign the relevant attendance period for this attendance."

    return None

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

    if tardy_minutes != 0:
        return "Input Error", "Cutting status cannot have both tardy and cutting minutes.\nPlease set tardy minutes to zero."
        
    if not 0 < int(cutting_minutes) <= 50:
        return "Input Error", "Cutting minutes can neither be under 0 minutes, nor can it be more than 50 minutes.\nPlease enter cutting minutes between 0-50 minutes."


    return None, None

# v0.4.0


def validate_timeframe(start_datetime, end_datetime):
    if start_datetime > end_datetime:
        return "End datetime can not start earlier than start datetime\nPlease ensure that start datetime is earlier than end datettime."
    if start_datetime == end_datetime:
        return "Start datetime and end datetime cannot happen simultaneously.\nPlease ensure that start datetime happens earlier than end datetime."
    if datetime.now() > end_datetime:
        return f"The current date, {datetime.now().strftime('%B %d, %Y')}, should not be past the end datetime.\nPlease enter a end datetime not already passed."
    return None

def check_attendance_dates(input_start_date, input_start_time, input_end_date, input_end_time, minutes_late):

    try:
        input_start_date = datetime.strptime(input_start_date, DATE_FORMAT).date()
    except ValueError:
        return "Input Error", "Please enter start date in MM-DD-YYYY format\n(e.g, 10-01-2025 for October 1, 2025)."
    
    try:
        input_start_time = datetime.strptime(input_start_time, TIME_FORMAT).time()
    except ValueError:
        return "Input Error", "Please enter start time in HH:MM in 24-Hour Format\n(e.g, 14:50 for 2:50 PM)."
        
    
    try:
        input_end_date = datetime.strptime(input_end_date, DATE_FORMAT).date()
    except ValueError:
        return "Input Error", "Please enter end date in MM-DD-YYYY\n(e.g, 10-02-2025 for October 2, 2025)."
    
    try:
        input_end_time = datetime.strptime(input_end_time, TIME_FORMAT).time()
    except ValueError:
        return "Input Error", "Please enter end time in HH:MM in 24-Hour Format\n(e.g, 15:40 for 3:40 PM)."

    try:
        minutes_late = int(minutes_late)
        if minutes_late < 0:
            return "Input Error", "Grace period can not be a negative number.\nPlease enter grace period between 1-30 minutes."
    except ValueError:
        return "Input Error", "Grace period can not be a non-number.\nPlease enter a numeric grace period between 1-30 minutes."

    return None, None

def validate_create_attendance_inputs(attendance_name, input_start_date, input_start_time, input_end_date, input_end_time, attendance_password, minutes_late):
    fields = {
        "Attendance Name cannot be empty."
        "\nPlease enter a name for attendance (3-30 characters).": 
        attendance_name,
        
        "Start Date can not be empty."
        "\nPlease enter start date in MM-DD-YYYY (10-01-2025 for October 1, 2025).": 
        input_start_date,
        
        "Start Time can not be empty."
        "\n Please entry start time 24 hour format (e.g, 14:50 for 2:50 PM).": 
        input_start_time,
        
        "End Date can not be empty."
        "\nPlease enter end date in MM-DD-YYYY (10-02-2025 for October 2, 2025).": 
        input_end_date,
        
        "End Time can not be empty."
        "\n Please enter end time 24 hour format (e.g, 15:40 for 3:40 PM).": 
        input_end_time,

        "Attendance Password can not be empty."
        "\nPlease enter an attendace password with 10-100 Characters.": 
        attendance_password,
        
        "Grace Period can not be empty."
        "\nPlease enter a grace period between 1-30 minutes.": 
        minutes_late,
    }

    for key, value in fields.items():
        if not value.strip():
            return "Input Error", key
        
    
    if len(attendance_name) < 3 or len(attendance_name) > 30:
        return "Input Error", "Please make attendance name 3-30 characters long."

    
    if len(attendance_password) < 10 or len(attendance_password) > 100:
        return "Input Error", "Please make password between 10-100 characters long."

    if not minutes_late.isdigit():
        return "Input Error", "Please enter minutes as a whole number."

    
    if int(minutes_late) < 1 or int(minutes_late) > 30:
        return "Input Error", "Please enter grace period between 1-30 minutes."

    return None, None

def create_validator_engine(
        attendance_name, 
        input_start_date, 
        input_start_time, 
        input_end_date, 
        input_end_time, 
        attendance_password, 
        minutes_late):
    
    create_attendance_error, create_attendnace_message = validate_create_attendance_inputs(
        attendance_name, 
        input_start_date, 
        input_start_time, 
        input_end_date, 
        input_end_time, 
        attendance_password, 
        minutes_late,
        )
    
    if create_attendance_error:
        return create_attendance_error, create_attendnace_message
    
    possible_date_error, possible_date_message = check_attendance_dates(
        input_start_date, 
        input_start_time, 
        input_end_date, 
        input_end_time, 
        minutes_late
    )

    if possible_date_error:
        return possible_date_error, possible_date_message

    return None, None

# Fillout Attendance
def fillout_attendance_validator(user, attendance_name, attendance_password, existing_attendance):
    
    if not user:
        return "Error", "Please be logged in to fillout an attendance."
             
    if not attendance_name.strip():
        return "Input Error", "Entered attendance name can not be empty.\nPlease enter attendance name."

    if not attendance_password.strip():
        return "Input Error", "Attendance password can not be empty.\nPlease enter the attendance password."
    
    if not existing_attendance:
        return "Input Error", "Attendance name and password don't match.\nPlease try again."
    
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
        entered_given_name, entered_surname, 
         entered_password, selected_account_role,
         selected_grade_level, selected_grade_section, entered_identifier
    ):
    
    possible_grade_sections = {
        7: ("Emerald", "Diamond", "Ruby"),
        8: ("Camia", "Jasmine", "Sampaguita"),
        9: ("Potassium", "Rubidium", "Sodium"),
        10: ("Electron", "Neutron", "Proton"),
        11: ("A", "B", "C"),
        12: ("A", "B", "C")
    }
    # Given Name
    if not entered_given_name.strip():
        return "Input Error", "Given name cannot be empty.\nPlease enter given name."
    
    if not entered_given_name.strip() or not all(c.isalpha() or c.isspace() for c in entered_given_name):
        return "Input Error", "Given name can not contain non-letters or non-spaces.\nPlease enter a given name with only letters and spaces."

    # Surname
    if not entered_surname.strip():
        return "Input Error", "Surname cannot be empty.\nPlease enter surname."
    
    if not entered_surname.strip() or not all(c.isalpha() or c.isspace() for c in entered_surname):
        return "Input Error", "Surname can not contain non-letters or non-spaces.\nPlease enter a surname with only letters and spaces."

    # Password
    if len(entered_password) < 10 or len(entered_password) > 100:
        return "Input Error", "Password has too few/little characters.\nPlease enter a password with 10-100 characters."

    # Selected Account role
    if not selected_account_role or selected_account_role.strip().lower() not in ("student", "teacher"):
        return "Input Error", "Selected account role cannot be empty.\nPlease select an account role."
    
    if not entered_identifier.strip():
        return "Input Error", "Entered Account Identifier cannot be empty\nPlease enter an account identifier\nNote: This can function as a 'username'."

    # Grade Level and Section
    if selected_grade_level and selected_grade_section:
        if selected_grade_section not in possible_grade_sections[int(selected_grade_level)]:
            return "Input Error", "Selected grade level and section do not match.\nPlease ensure that selected grade level and section match, and try again."

    return None, None





# v0.4.0

# Login
def validate_login_input(username, password):
    if not username.strip():
        return "Input Error", "Entered username can not be empty.\nPlease enter username."
    if not password:
        return "Input Error", "Entered password can not be empty.\nPlease enter password."
    return None, None

# Signup
def validate_signup_input(username, password):
    if not username.strip():
        return "Input Error", "Username cannot be empty.\nPlease enter a username."

    if not username.strip() or not all(c.isalpha() or c.isspace() for c in username):
        return "Input Error", "Username can not contain non-letters or non-spaces.\nPlease enter a username with only letters and spaces."

    if len(password) < 10 or len(password) > 100:
        return "Input Error", "Password has too few/little characters.\nPlease enter a password with 10-100 characters."
    
    return None, None
# ========== Settings ==========
def validate_password_change_entry(user, old_password, new_password):
    fields = {
        "Current password can not be empty."
        "\nPlease enter the current password of your account":
        old_password,

        "New password can not be empty."
        "\nPlease enter the new password for your account":
        new_password,
    }
    for key, value in fields.items():
        if not value.strip():
            return "Input Error", key
    
    if old_password == new_password:
        return "Input Error", "New password can not be the same as current password\nPlease make new password different from current password."
    
    if len(new_password) < 10 or len(new_password) > 100:
        return "Input Error", "New Password has too few or too many characters.\nPlease enter a new password between 10-100 characters."
    
    if not user:
        return "Authentication Error", "You currently do not have an account.\nPlease be logged in to change password."
    
    return None, None