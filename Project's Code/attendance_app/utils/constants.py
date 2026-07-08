# =========================
# Imports

# Standard Library

# Third-Party

# Code Files

# =========================

# constants.py

# ========== Account Details ==========

# ===== Account Roles =====
STUDENT_ACCOUNT_STATUS = "student"
TEACHER_ACCOUNT_STATUS = "teacher"

ADMIN_ACCOUNT_STATUS = "admin" # NOTE: This is currently not implemented yet.

ALLOWED_ACCOUNT_ROLES = ("student", "teacher")


# ==== Shortcut Keys =====
ENTER_KEY_SHORTCUT = '<Return>'

# ===== Banned words =====
BANNED_ACCOUNT_WORDS = [

    # Administrative/System Usernames
    "admin",
    "administrator",
    "root",
    "superuser",
    "system",
    "mod",
    "moderator",
    "support",
    "helpdesk",
    "contact",
    "billing",
    "info",
    "security",
    "null",
    "undefined",
    "system_user",
    "localhost",
    "script",
    "http",
    "guest",
    "test",
    "user",
    "temp",
    "anonymous",
    "official",
    "verified",
    "mod_verify",
    "myapp",
]
# ===== Time Parsing Constants =====
DATE_FORMAT = "%m-%d-%Y"
TIME_FORMAT = "%H:%M"
DISPLAY_FORMAT = "%m-%d-%Y %H:%M"

# ===== Attendance Marking Constants =====
PRESENT_STATUS = "Present"
ABSENT_STATUS = "Absent"
TARDY_STATUS = "Tardy"
CUTTING_STATUS = "Cutting"
POSSIBLE_ATTENDANCE_PUNCTUALITIES = ("present", "absent", "tardy", "cutting")

#  ===== UI Constants =====
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 680

BUTTON_NORMAL_STATE = "NORMAL"

BUTTON_FONT_SIZE = ("Montserrat", 12)
ENTRY_FONT_SIZE = ("Montserrat", 12)
LABEL_FONT_SIZE = ("Arial", 12)
SPINBOX_FONT_SIZE = ("Montserrat", 12)

DEFAULT_STYLE = {
    "foreground": "#0f0f0f",
    "background": "#f0f0f0"
}

DISABLED_SPINBOX_STYLE = {
    "foreground": "#0f0f0f",
    "background": "#0f0f0f",
    "fieldbackground": "#21222b"
}

# ===== Grade levels, sections, and subjects =====
GRADE_LEVELS = (7, 8, 9, 10, 11, 12)

POSSIBLE_GRADE_SECTIONS = {
    7: ("Emerald", "Diamond", "Ruby"),
    8: ("Camia", "Jasmine", "Sampaguita"),
    9: ("Potassium", "Rubidium", "Sodium"),
    10: ("Electron", "Neutron", "Proton"),
    11: ("A", "B", "C"),
    12: ("A", "B", "C")
}

GRADE_7_SUBJECTS = sorted((
    "Integrated Science 1", "Computer Science 1", 
    "Mathematics 1", "ADTech 1",
    "English 1", "Filipino 1",
    "Social Science 1", "PEHM 1",
    "Values Education 1"
))

GRADE_8_SUBJECTS = sorted((
    "Biology 1", "Chemistry 1",
    "Physics 1", "Computer Science 2",
    "Mathematics 2", "Mathematics 3",
    "ADTech 2", "English 2",
    "Filipino 2", "Social Science 2",
    "PEHM 2", "Values Education 2", 
    "Earth Science 1"
))

GRADE_9_SUBJECTS = sorted((
    "Biology 2", "Chemistry 2",
    "Physics 2", "Computer Science 3",
    "Mathematics 4", "Statistics 1",
    "ADTech 3", "English 3",
    "Filipino 3", "Social Science 3", 
    "PEHM 3", "Values Education 3"
))

GRADE_10_SUBJECTS = sorted((
    "Biology 3", "Chemistry 3",
    "Physics 3", "Computer Science 4",
    "Mathematics 5", "Statistics 2",
    "English 4", "Filipino 4",
    "Social Science 4", "PEHM 4",
    "Values Education 4", "Elective"
))

GRADE_11_SUBJECTS = sorted((
    "Biology 4", "Chemistry 4",
    "Physics 4", "Mathematics 6",
    "English 5", "Filipino 5",
    "Social Science 5", "Research 1",
    "Elective"
))

GRADE_12_SUBJECTS = sorted((
    "Biology 5", "Chemistry 5",
    "Physics 5", "Mathematics 8",
    "Computer Science 5", "Engineering 1",
    "Engineering 2", "Agriculture 1", 
    "Geology 1", "Climate Science",
    "Mathematics 7", "English 6",
    "Filipino 6", "Social Science 6",
    "Research 2", "Elective"
))


GRADE_SUBJECTS = {
    7: GRADE_7_SUBJECTS,
    8: GRADE_8_SUBJECTS,
    9: GRADE_9_SUBJECTS,
    10: GRADE_10_SUBJECTS,
    11: GRADE_11_SUBJECTS,
    12: GRADE_12_SUBJECTS
}


# ==================== Error Message Components ====================
# NOTE: Some of the error messages are used more than once at different functions.
# 
# ========== Error Types =========
AUTH_ERROR = "Authentication Error"
INPUT_ERROR = "Input Error"

# ========== auth_service Error Messages ==========

# ===== Signup function =====
EMPTY_GIVEN_NAME_MESSAGE = "Given name cannot be empty.\nPlease enter given name."
EMPTY_SURNAME_MESSAGE = "Surname cannot be empty.\nPlease enter surname."
EMPTY_USERNAME_MESSAGE = "Entered account username cannot be empty.\nPlease enter the account username."
EMPTY_ROLE_MESSAGE = "Selected account role cannot be empty.\nPlease select an account role."
EMPTY_STUDENT_GRADE_LEVEL =  "The selected grade level is empty.\nFor your student account, please enter your grade level."
EMPTY_STUDENT_GRADE_SECTION = "The selected grade section is empty.\nFor your student account, please enter your grade section."

INVALID_FIRST_NAME_MESSAGE = "Given name can only have letters, accented characters, speaces, and hyphens.\nPlease enter given name that only includes those."
INVALID_SURNAME_MESSAGE = "Surname can only have letters, accented characters, speaces, and hyphens.\nPlease enter given name that only includes those."
INVALID_PASSWORD_LENGTH_MESSAGE = "Password has too few/little characters.\nPlease enter a password with 10-100 characters."

NOT_GRADE_SECTION_MATCH_MESSAGE = "Entered grade level and section do not match.\nPlease ensure that selected section is under the selected grade level, and try again."
NOT_APPLICABLE_ROLE_ERROR = "The following entered role is not applicable.\nPlease select an account role that is applicable.\nFor this case, it is either Student or Teacher."
DUPLICATE_ACCOUNT_ERROR_MESSAGE = "You cannot register a duplicate account.\nPlease recheck your entered account info, and try again.\nNote: This could come from either a duplicate first name, surname, or identifer."

GIVEN_NAME_LENGTH_OUT_OF_RANGE = "The following entered given name has been flagged for being potentially nonsensical.\nReason: Too few or too many characters\n\nPlease enter the account's given name within 2-70 characters."
SURNAME_LENGTH_OUT_OF_RANGE = "The following entered surname has been flagged for being potentially nonsensical.\nReason: Too few or too many characters\n\nPlease enter the account's surname surname within 2-70 characters."
USERNAME_OUT_OF_RANGE = "The following entered username has been detected to be too long/short.\nPlease set your username to 3-30 characters."
# ===== Login Function =====
EMPTY_LOGIN_PASSWORD = "Entered password can not be empty\nPlease enter the account password."
NOT_PASSWORD_MATCH_ERROR_MESSAGE =  "The account name and password do not match.\nPlease recheck your entered inputs, and try again."
# ========== attendance_service Error Messages ==========

# ===== Attendance Creation Function =====
EMPTY_ATTENDANCE_GRADE_SECTION = "The assigned class section can not be empty.\nPlease assign a class section for the attendance."
EMPTY_ATTENDANCE_SUBJECT = "The assigned subject for an attendance can not be empty.\nPlease assign a subject for the attendance."
EMPTY_ATTENDANCE_DATE = "The assigned date of the attendance can not be empty.\nPlease assign the relevant attendance date."
EMPTY_ATTENDANCE_GRADE_LEVEL = "The assigned grade level for the attendance can not be empty.\nPlease assign a grade level for the attendance."
EMPTY_ATTENDANCE_PERIOD = "Please assign the relevant attendance period for this attendance."
EMPTY_ATTENDANCE_ACCOUNT_ID = "There was no account ID detected in your current session\nPlease log out and log back in, and try again."

NON_DIGIT_ATTENDANCE_GRADE_LEVEL = "Attendance grade level cannot be a non-digit.\nPlease enter an assigned attendance grade level that is an integer from 7 to 12." 
OUT_OF_RANGE_ATTENDANCE_GRADE_LEVEL = "Entered attendance grade cannot be less than 7 or greater than 12.\nPlease enter an assigned attendance grade level that is an integer from 7 to 12."
NOT_GRADE_SUBJECT_MATCH_MESSAGE = "The following entered subject is not under the current grade level chosen.\nPlease choose a subject that is under the chosen grade level."

INVALID_FUTURE_ATTENDANCE_DATE_MESSAGE = "The entered attendance date cannot be past today's date.\nPlease enter an attendance date that is today or from a past date."
INVALID_ATTENDANCE_DATE_FORMAT_MESSAGE = "The entered date Please enter start date in MM-DD-YYYY format\n(e.g, 10-01-2025 for October 1, 2025)."
INVALID_ATTENDANCE_DATE_WEEKEND_MESSAGE = "The entered date can not be a weekend.\nPlease enter an attendace date that is not a weekday."  
DUPLICATE_ATTENDANCE_ERROR_MESSAGE = "A duplicate attendance session has already been made.\nIf this is a mistake, recheck the entered attendance info, and try again."

ASYNCHRONUS_CLASSES_GRADE_7_8 = "Due to Memorandum No. 012, s. 2026: Energy Conservation Measures, grade 7 and 8 have asynchronus classes.\nThus, in this scenario, there is no need to create an attendance session."
ASYNCHRONUS_CLASSES_GRADE_9_10 = "Due to Memorandum No. 012, s. 2026: Energy Conservation Measures, grade 9 and 10 have asynchronus classes 12:00 PM and onward.\nThus, in this scenario, there is no need to create an attendance session."

NON_DIGIT_ATTENDANCE_PERIOD = "The attendance period cannot be a non-digit.\nPlease enter an attendance period that is an integer from 1 to 10."
OUT_OF_RANGE_ATTENDANCE_PERIOD = "The entered attendance period cannot be less than 1 or greater than 10\nPlease enter an attendance period between 1-10."
# ===== Attendance Marking Feature =====
EMPTY_SELECTED_STUDENT_ID = "Selected student ID cannot be empty.\nPlease select a student id to mark."
EMPTY_SELECTED_STUDENT_PUNCTUALITY = "Selected attendance punctuality for a student can not be empty.\nPlease assign a punctuality status."
EMPTY_TARDY_MINUTES = "Tardy status can not have empty tardy minutes\nPlease enter minutes for the tardy status."
EMPTY_CUTTING_MINUTES = "Cutting status can not have empty cutting minutes\nPlease enter minutes for the cutting status."
EMPTY_ATTENDANCE_MARKING_ID = "There was no attendance ID detected during your attendance marking session.\nPlease exit your current attendance marking session and try again."

NON_DIGIT_TARDY_MINUTES = "Entered tardy minutes for tardy status can not be a non-digit.\nPlease assign the number of minutes for tardy status."
NON_DIGIT_CUTTING_MINUTES = "Entered cutting minutes for cutting status can not be a non-digit.\nPlease assign the number of minutes for cutting status."
BOTH_TARDY_CUTTING_ENTRY_ERROR = "The selected student punctuality cannot have an entry for both tardy and cutting minutes. Please set either tardy or cutting minutes to zero, dependening on the chosen attendance punctuality."

INVALID_ATTENDANCE_PUNCTUALITY_SELECTED = "The selected punctuality does not match with either of the applicable attendance punctualties\n.Please select an applicable attendance punctuality."
INVALID_TARDY_MINUTES_RANGE = "Tardy minutes can neither be under 0 minutes, nor can it be more than 50 minutes.\nPlease enter tardy minutes between 0-50 minutes."
INVALID_CUTTING_MINUTES_RANGE = "Cutting minutes can neither be under 0 minutes, nor can it be more than 50 minutes.\nPlease enter cutting minutes between 0-50 minutes."

STUDENT_ID_NOT_OF_ATTENDANCE = "The entered student ID is not part of the following attendance.\nPlease enter a student ID that is part of the attendance."

NOT_PUNCTUALITY_TRUANCY_MINUTES_MATCH = "Present and absent punctualities can neither have tardy nor cutting minutes.\nPlease assign the selected punctuality with no tardy and cutting minutes."