from datetime import datetime
from . import constants

# validators.py

DATE_FORMAT = "%m-%d-%Y"
TIME_FORMAT = "%H:%M"

# ========== Attendance Logic ==========
# Create Attendance

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

# Account Login
def check_login_entries(entered_given_name, entered_surname, entered_password):
    if not entered_given_name.strip():
        return "Input Error", "Entered given name can not be empty.\nPlease enter given name."
    if not entered_surname.strip():
        return "Input Error", "Entered surname can not be empty.\nPlease enter surname."
    if not entered_password.strip():
        return "Input Error", "Entered password can not be empty\nPlease enter password."
    return None, None


# Account Creation
def validate_entered_account_info(
        entered_given_name, entered_surname, 
         entered_password, selected_account_role,
         selected_grade_level, selected_grade_section
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
    
    if selected_grade_level and selected_grade_section:
        if selected_grade_section not in possible_grade_sections[int(selected_grade_level)]:
            return "Input Error", "Selected grade level and section do not match.\nPlease ensure that selected grade level and section match, and try again."

    return None, None









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