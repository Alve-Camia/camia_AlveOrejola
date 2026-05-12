from utils import validators
import pytest
# Validators' Unit test Practice


# Attendance Creation Validator
@pytest.mark.parametrize(
    "grade_level, grade_section, subject,  date, period, expected", [
    ("9", "Sodium", "Computer Science 3", "03-24-2026", 9, (False, None, None)),

    ("7", "Ruby", "PEHM 1", "03-24-2026", 1, (False, None, None)),
    ("12", "A", "Agriculture 1", "02-20-2026", 10, (False, None, None)),

    ("2", "Ruby", "PEHM 1", "04-23-2026", 1, (True, "Input Error", "Entered attendance grade cannot be less than 7 or greater than 12.\nPlease enter an assigned attendance grade level that is an integer from 7 to 12.")),
    ("7", "", "PEHM 1", "04-23-2026", 1, (True, "Input Error", "The assigned class section can not be empty.\nPlease assign a class section for the attendance."))
])

def test_attendance_creation_validator(grade_level, grade_section, subject, date, period, expected):
    assert validators.attendance_creation_validator(grade_level, grade_section, subject, date, period) == expected