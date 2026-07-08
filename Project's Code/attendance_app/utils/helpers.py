# helpers.py

# ==============================
# Imports

# Standard Library
from dataclasses import dataclass, field
from datetime import datetime

# Third-party
import bcrypt

# Code Files
from . import constants

# ==============================
def hash_password(password):
    pw_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(pw_bytes, salt)
    return hashed_pw

def possible_input_error_looper(
        possible_field_input_errors: tuple[tuple[bool, str], ...]
    ) -> tuple[bool, str | None]:

    for error_status, corresponding_error_message in possible_field_input_errors:
        if error_status: 
            return True, corresponding_error_message
    
    return False, None

def error_response(error_type, error_message):
    return {
        "error_status": True,
        "error_type": error_type,
        "error_message": error_message,
        "data": None
    }

def check_entered_password(entered_password, authenticated_password):

    entered_password = entered_password.encode("utf-8")
    authenticated_password = authenticated_password.encode("utf-8")
    
    return bcrypt.checkpw(entered_password, authenticated_password)


@dataclass
class FieldValidation:
    success: bool
    error_title: str | None
    error_message: str | None

# ==== Authentication Dataclasses =====
@dataclass
class AccountRegistration:
    given_name: str
    surname: str
    identifier: str
    grade_level: str | None
    grade_section: str | None
    role: str
    password: str

@dataclass
class LoginSessionInfo:
    id: int
    given_name: str
    surname: str
    role: str


# ===== Attendance Dataclasses =====
@dataclass
class AttendanceSessionInfo:
    grade_level: str | int
    grade_section: str
    subject: str
    date: str | datetime
    period: str | int
    creator_id: int

    def parse_validated_attendance_session_info(self):
        self.grade_level = int(self.grade_level)
        self.period = int(self.grade_level)
        self.date = datetime.strptime(self.date, constants.DATE_FORMAT).date()


@dataclass
class SelectedAttendanceSessionInfo:
    id: int
    date: datetime
    grade_level: int
    grade_section: str
    subject: str
    period: int
    
@dataclass
class AttendanceMarkingInfo:
    student_id: str | int
    punctuality_status: str
    tardy_minutes: str | int
    cutting_minutes: str | int
    attendance_id: int

