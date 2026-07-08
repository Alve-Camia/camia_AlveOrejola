# ==============================
# Imports

# Standard Library

# Third-party

# Code Files
from ..db import attendance_repo
from ..utils import validators, constants, helpers
from datetime import datetime

# attendance_service.py

# ===== Attendance Logic =====



def process_attendance_creation(
        created_attendance_session: helpers.AttendanceSessionInfo
    ) -> helpers.FieldValidation:
    """TODO: Add a useful docstring for this function""" 
    validation_error, error_type, error_message = validators.attendance_creation_validator(created_attendance_session)

    if validation_error:
        return helpers.FieldValidation(False, error_type, error_message)

    now = datetime.now()
    # NOTE: Since user's input has been validated to have a happy path, it can now be safely parsed.
    created_attendance_session.parse_validated_attendance_session_info()
    
    duplicate_attendance_session = attendance_repo.check_duplicate_attendance(created_attendance_session)
    if duplicate_attendance_session:
        return helpers.FieldValidation(False, constants.INPUT_ERROR, constants.DUPLICATE_ATTENDANCE_ERROR_MESSAGE)

    stored_attendance_id, stored_student_ids = attendance_repo.insert_attendance_session(created_attendance_session, now)
    attendance_repo.insert_attendance_record(stored_attendance_id, stored_student_ids)

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
        attendance_marking_info: helpers.AttendanceMarkingInfo,
        attendance_id: int
    ) -> helpers.FieldValidation:

    attendance_marking_info.tardy_minutes, attendance_marking_info.cutting_minutes = attendance_punctuality_defaulter(attendance_marking_info)

    validator_error, validator_message = validators.validate_attendance_marking(attendance_marking_info)

    if validator_error:
        return helpers.FieldValidation(False, validator_error, validator_message)
    
    found_attendance_record = attendance_repo.check_attendance_record(attendance_marking_info, attendance_id)
        
    if not found_attendance_record:
        return helpers.FieldValidation(
            False, constants.INPUT_ERROR, 
            constants.STUDENT_ID_NOT_OF_ATTENDANCE
        )
        
    attendance_repo.update_attendance_record(attendance_marking_info, attendance_id)
    
    return helpers.FieldValidation(True, None, None)

def attendance_punctuality_defaulter(
        attendance_marking_info: helpers.AttendanceMarkingInfo
    ) -> tuple[int, int]:
    
    if attendance_marking_info.punctuality_status == constants.PRESENT_STATUS or attendance_marking_info.punctuality_status == constants.ABSENT_STATUS:
        attendance_marking_info.tardy_minutes = 0
        attendance_marking_info.cutting_minutes = 0

    return attendance_marking_info.tardy_minutes, attendance_marking_info.cutting_minutes



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