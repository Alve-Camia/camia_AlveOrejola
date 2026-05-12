# attendance_service.py
from typing import Callable, Optional
from ..db import attendance_repo
from ..utils import validators, constants, helpers
from datetime import datetime

# ===== Attendance Logic =====

def process_attendance_creation(
        entered_attendance_grade: str, 
        entered_attendance_section: str,
        entered_attendance_subject: str, 
        entered_attendance_date: str,
        entered_attendance_period: str, 
        current_user_id: int) -> helpers.FieldValidation:
    
    """TODO - Improve Current function Docstring"""
    """Creates attendances sessions and records based on user input"""

    has_attendance_error, error_title, error_message = validators.attendance_creation_validator( 
        entered_attendance_grade, entered_attendance_section,
        entered_attendance_subject, entered_attendance_date,
        entered_attendance_period)

    if has_attendance_error:
        return helpers.FieldValidation(False, error_title, error_message)
    
    now = datetime.now()
    entered_attendance_grade = int(entered_attendance_grade)
    entered_attendance_period = int(entered_attendance_period)
    entered_attendance_date = datetime.strptime(entered_attendance_date, constants.DATE_FORMAT).date()

    duplicate_attendance_record = attendance_repo.check_duplicate_attendance(
        entered_attendance_grade, entered_attendance_section,
        entered_attendance_subject, entered_attendance_date,
        entered_attendance_period
    )
    
    if duplicate_attendance_record:
        return helpers.FieldValidation(
            False,
            "Input Error",
            "A duplicate attendance session has already been made.\nIf this is a mistake, recheck the entered attendance info, and try again."
        )

    stored_attendance_id, stored_student_ids = attendance_repo.insert_attendance_session(
        entered_attendance_grade, entered_attendance_section, 
        entered_attendance_subject, entered_attendance_date, 
        entered_attendance_period, current_user_id, 
        now
    )

    for stored_id in stored_student_ids:
        attendance_id = stored_attendance_id
        student_id = stored_id[0]

        attendance_repo.insert_attendance_record(attendance_id, student_id)

    return helpers.FieldValidation(True, None, None)

# ===== Attendance Marking =====
def fetch_attendance_marking_info(
        attendance_id: int, 
        attendance_grade: int, 
        attendance_section: str
    ) -> tuple:

    return attendance_repo.get_authenticated_attendance_records(
        attendance_id, attendance_grade, 
        attendance_section)

def process_attendance_marking(
        selected_student_id: str, 
        attendance_punctuality: str, 
        tardy_minutes: str, 
        cutting_minutes: str, 
        attendance_id: int
    ) -> helpers.FieldValidation:

    if attendance_punctuality == "Present" or attendance_punctuality == "Absent":
        tardy_minutes = 0
        cutting_minutes = 0

    validator_error, validator_message = validators.validate_attendance_marking(
        selected_student_id, attendance_punctuality, 
        tardy_minutes, cutting_minutes
    )

    if validator_error:
        return helpers.FieldValidation(False, validator_error, validator_message)
    
    found_attendance_record = attendance_repo.check_attendance_record(selected_student_id, attendance_id)
        
    if not found_attendance_record:
        return helpers.FieldValidation(
            False, constants.INPUT_ERROR, 
            "The entered student ID is not part of the following attendance.\nPlease enter a student ID that is part of the attendance."
        )
        
    attendance_repo.update_attendance_record(
        attendance_punctuality, tardy_minutes, 
        cutting_minutes, attendance_id, 
        selected_student_id)
    
    return helpers.FieldValidation(True, None, None)
    
def lookup_creator_attendances(
        creator_id: int
    ) -> tuple:
    return attendance_repo.get_dashboard_table_info(creator_id)


# ===== Student Attendances =====
def fetch_student_attendances(
        student_id: int
    ) -> tuple:
    return attendance_repo.search_student_attendance_info(student_id)

# ===== Attendance Export =====
def process_attendance_export(
        teacher_id: int, 
        current_datetime: str
    ) -> helpers.FieldValidation:
    
    attendance_export_error, attendance_export_message = attendance_repo.export_dashboard_csv(teacher_id, current_datetime)
    if attendance_export_error:
        return helpers.FieldValidation(False, attendance_export_error, attendance_export_message)
    
    return helpers.FieldValidation(True, None, None)

# ===== Attendance Deletion =====
def process_attendace_deletion(
        teacher_id: int
    ):
    attendance_repo.delete_all_attendances_made(teacher_id)