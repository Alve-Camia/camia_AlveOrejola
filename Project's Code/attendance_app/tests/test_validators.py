

# ====================
# Imports

# Third-Party Imports
import pytest
from unittest.mock import patch

# Code Files
from ..utils import validators, helpers, constants
from ..services import attendance_service


# Validators' Unit tests

# =============== Attendance Creation Validator ===============
attendance_creation_validator_test_cases = [
    # =============== Happy Path - Attendance Creation Validator ===============
    pytest.param(
        "9", "Sodium", "Computer Science 3", "03-24-2026", "9", 1, 
        (False, None, None), 
        id="happy_path_attendance_creation"
    ),

    # =============== Edge Cases - Attendance Creation Validator ===============
    pytest.param(
        "7", "Ruby", "PEHM 1", "03-24-2026", "5", 1, 
        (False, None, None), 
        id="edge_grade_7_lower_boundary"
    ),
    pytest.param(
        "12", "A", "Agriculture 1", "02-20-2026", "5", 1, 
        (False, None, None), 
        id="edge_grade_12_upper_boundary"
    ),

    pytest.param(
        "12", "A", "Agriculture 1", "02-20-2026", "1", 1, 
        (False, None, None), 
        id="edge_class_period_1"
    ),

    pytest.param(
        "12", "A", "Agriculture 1", "02-20-2026", "10", 1, 
        (False, None, None), 
        id="edge_class_period_10"
    ),

    pytest.param(
        "12", "A", "Agriculture 1", "05-04-2026", "1", 1, 
        (False, None, None), 
        id="edge_monday_class"
    ),

    pytest.param(
        "12", "A", "Agriculture 1", "05-08-2026", "1", 1, 
        (False, None, None), 
        id="edge_friday_classes"
    ),

    # ========== Sad Paths - Attendance Creation Validator ==========

    # ===== Sad Paths - Attendance Creator ID =====
    pytest.param(
        "7", "Ruby", "PEHM 1", "04-23-2026", "1", None, 
        (True, constants.AUTH_ERROR, constants.EMPTY_ATTENDANCE_ACCOUNT_ID), 
        id="sad_missing_account_id"
    ),

    # ===== Sad Paths - Attendance Grade Level =====
    pytest.param(
        "2", "Ruby", "PEHM 1", "04-23-2026", "1", 1, 
        (True, constants.INPUT_ERROR, constants.OUT_OF_RANGE_ATTENDANCE_GRADE_LEVEL), 
        id="sad_low_grade_level"
    ),

    pytest.param(
        " ", "Ruby", "PEHM 1", "04-23-2026", "1", 1, 
        (True, constants.INPUT_ERROR, constants.EMPTY_ATTENDANCE_GRADE_LEVEL), 
        id="sad_empty_grade_level"
    ),

    pytest.param(
        "9", "Lithium - A nonexistent grade 9 section name", "PEHM 3", "04-23-2026", "1", 1, 
        (True, constants.INPUT_ERROR, constants.NOT_GRADE_SECTION_MATCH_MESSAGE), 
        id="nonexistent_grade_level"
    ),

    # ===== Sad Paths - Attendance Grade Section =====
    pytest.param(
        "7", "", "PEHM 1", "04-23-2026", "1", 1, 
        (True, constants.INPUT_ERROR, constants.EMPTY_ATTENDANCE_GRADE_SECTION), 
        id="sad_empty_section"
    ),

    # ====== Sad Paths - Attendance Period =====
    pytest.param(
        "7", "Ruby", "PEHM 1", "04-23-2026", "11", 1, 
        (True, constants.INPUT_ERROR, constants.OUT_OF_RANGE_ATTENDANCE_PERIOD), 
        id="sad_too_high_attendance_period"
    ),
    pytest.param(
        "7", "Ruby", "PEHM 1", "04-23-2026", "0", 1, 
        (True, constants.INPUT_ERROR, constants.OUT_OF_RANGE_ATTENDANCE_PERIOD), 
        id="sad_too_low_attendance_period"
    ),

    pytest.param(
        "7", "Ruby", "PEHM 1", "04-23-2026", "", 1, 
        (True, constants.INPUT_ERROR, constants.EMPTY_ATTENDANCE_PERIOD), 
        id="sad_empty_attendance_period"
    ),

    # ===== Sad Paths - Attendance Subject =====

    pytest.param(
        "7", "Ruby", "", "04-23-2026", "1", 1, 
        (True, constants.INPUT_ERROR, constants.EMPTY_ATTENDANCE_SUBJECT), 
        id="sad_empty_subject"
    ),

    # ===== Sad Paths - Attendance Date =====
    
    pytest.param(
        "7", "Ruby", "PEHM 1", "This is a sentence, not a date.", "1", 1, 
        (True, constants.INPUT_ERROR, constants.INVALID_ATTENDANCE_DATE_FORMAT_MESSAGE), 
        id="invalid_attendance_date_format"
    ),

    pytest.param(
        "7", "Ruby", "PEHM 1", " ", "1", 1, 
        (True, constants.INPUT_ERROR, constants.EMPTY_ATTENDANCE_DATE), 
        id="sad_missing_attendance_date"
    ),

    # 
    pytest.param(
        "7", "Ruby", "PEHM 1", "05-09-2026", "1", 1, 
        (True, constants.INPUT_ERROR, constants.INVALID_ATTENDANCE_DATE_WEEKEND_MESSAGE), 
        id="sad_saturday_class"
    ),

    pytest.param(
        "7", "Ruby", "PEHM 1", "05-10-2026", "1", 1, 
        (True, constants.INPUT_ERROR, constants.INVALID_ATTENDANCE_DATE_WEEKEND_MESSAGE), 
        id="sad_sunday_class"
    ),

]

@pytest.mark.parametrize(
    "grade_level, grade_section, subject, date, period, creator_id, expected", 
    attendance_creation_validator_test_cases
)
def test_attendance_creation_validator(
    grade_level, grade_section, 
    subject, date, 
    period, creator_id, 
    expected
):
    attendance_creation_input = (grade_level, grade_section, subject, date, period, creator_id)
    attendance_session_info = helpers.AttendanceSessionInfo(*attendance_creation_input)
    

    assert validators.attendance_creation_validator(attendance_session_info) == expected

# =============== Attendance Marking Validator ===============
attendance_marking_test_cases = [

    # =============== Happy Path - Attendance Marking Validator ===============
    pytest.param(
        "5", "Absent", 0, 0, 1, 
        (None, None), 
        id="happy_path_attendance_marking"
    ),

    # =============== Edge Cases - Attendance Marking Validator ===============
    pytest.param(
        "1", "Tardy", "1", "0", 1, 
        (None, None), 
        id="edge_minimum_tardy_minutes"
    ),

    pytest.param(
        "1", "Tardy", "50", "0", 1, 
        (None, None), 
        id="edge_maximum_tardy_minutes"
    ),

    pytest.param(
        "1", "Cutting", "0", "1", 1, 
        (None, None), 
        id="edge_minimum_cutting_minutes"
    ),

    pytest.param(
        "1", "Cutting", "0", "50", 1, 
        (None, None), 
        id="edge_maximum_cutting_minutes"
    ),

    # =============== Sad Path - Attendance Marking Validator ===============

    # ===== Sad Paths - Student ID =====
    pytest.param(
        "", "Present", "0", "0", 1, 
        (constants.INPUT_ERROR, constants.EMPTY_SELECTED_STUDENT_ID), 
        id="sad_no_selected_student_id"
    ),

    # ===== Sad Paths - Attendance Punctuality =====

    pytest.param(
        "1", "", "0", "0", 1, 
        (constants.INPUT_ERROR, constants.EMPTY_SELECTED_STUDENT_PUNCTUALITY), 
        id="sad_no_selected_student_punctuality"
    ),

    pytest.param(
        "1", "Here", "0", "0", 1, 
        (constants.INPUT_ERROR, constants.INVALID_ATTENDANCE_PUNCTUALITY_SELECTED), 
        id="sad_not_applicable_attendance_punctuality"
    ),

    pytest.param(
        "1", "Present", "1", "0", 1, 
        (constants.INPUT_ERROR, constants.NOT_PUNCTUALITY_TRUANCY_MINUTES_MATCH), 
        id="sad_punctuality_tardy_cutting_minutes_mismatch_case_1"
    ),

    pytest.param(
        "1", "Present", "0", "1", 1, 
        (constants.INPUT_ERROR, constants.NOT_PUNCTUALITY_TRUANCY_MINUTES_MATCH), 
        id="sad_punctuality_tardy_cutting_minutes_mismatch_case_2"
    ),

    pytest.param(
        "1", "Absent", "1", "0", 1, 
        (constants.INPUT_ERROR, constants.NOT_PUNCTUALITY_TRUANCY_MINUTES_MATCH), 
        id="sad_punctuality_tardy_cutting_minutes_mismatch_case_3"
    ),

    pytest.param(
        "1", "Absent", "0", "1", 1, 
        (constants.INPUT_ERROR, constants.NOT_PUNCTUALITY_TRUANCY_MINUTES_MATCH), 
        id="sad_punctuality_tardy_cutting_minutes_mismatch_case_4"
    ),

    # ===== Sad Paths - Tardy Minutes =====

    pytest.param(
        "1", "Tardy", "", "0", 1, 
        (constants.INPUT_ERROR, constants.EMPTY_TARDY_MINUTES), 
        id="sad_empty_tardy_minutes"
    ),

    pytest.param(
        "1", "Tardy", "", "", 1, 
        (constants.INPUT_ERROR, constants.EMPTY_TARDY_MINUTES), 
        id="sad_tardy_status_both_empty_tardy_cutting_minutes"
    ),

    pytest.param(
        "1", "Cutting", "", "", 1, 
        (constants.INPUT_ERROR, constants.EMPTY_CUTTING_MINUTES), 
        id="sad_cutting_status_both_empty_tardy_cutting_minutes"
    ),

    pytest.param(
        "1", "Cutting", "0", "", 1, 
        (constants.INPUT_ERROR, constants.EMPTY_CUTTING_MINUTES), 
        id="sad_empty_cutting_minutes"
    ),

    pytest.param(
        "1", "Tardy", "This is a sentence, not a digit.", "0", 1, 
        (constants.INPUT_ERROR, constants.NON_DIGIT_TARDY_MINUTES), 
        id="sad_tardy_minutes_string"
    ),
    

    pytest.param(
        "1", "Tardy", "This is a sentence, not a digit.", "This is a sentence, not a digit. This shouldn't even be filled out.", 1, 
        (constants.INPUT_ERROR, constants.NON_DIGIT_TARDY_MINUTES), 
        id="sad_tardy_minutes_string"
    ),

    pytest.param(
        "1", "Tardy", "1", "This shouldn't even be filled out.", 1, 
        (constants.INPUT_ERROR, constants.NON_DIGIT_CUTTING_MINUTES), 
        id="sad_tardy_with_cutting_minutes_as_string"
    ),

    pytest.param(
        "1", "Tardy", "0", "0", 1, 
        (constants.INPUT_ERROR, constants.INVALID_TARDY_MINUTES_RANGE), 
        id="sad_too_low_tardy_minutes"
    ),

    pytest.param(
        "1", "Tardy", "51", "0", 1, 
        (constants.INPUT_ERROR, constants.INVALID_TARDY_MINUTES_RANGE), 
        id="sad_too_high_tardy_minutes"
    ),

    # ==== Sad Paths - Cutting Minutes =====

    pytest.param(
        "1", "Cutting", "0", "This is a sentence, not a digit.", 1, 
        (constants.INPUT_ERROR, constants.NON_DIGIT_CUTTING_MINUTES), 
        id="sad_tardy_minutes_string"
    ),

    pytest.param(
        "1", "Cutting", "0", "0", 1, 
        (constants.INPUT_ERROR, constants.INVALID_CUTTING_MINUTES_RANGE), 
        id="sad_too_low_cutting_minutes"
    ),

    pytest.param(
        "1", "Cutting", "0", "51", 1, 
        (constants.INPUT_ERROR, constants.INVALID_CUTTING_MINUTES_RANGE), 
        id="sad_too_high_cutting_minutes"
    ),

    pytest.param(
        "1", "Cutting", "This shouldn't even be filled out.", "1", 1, 
        (constants.INPUT_ERROR, constants.NON_DIGIT_TARDY_MINUTES), 
        id="sad_cutting_with_tardy_minutes_as_string"
    ),

    # ===== Sad Paths - Attendance ID =====
    pytest.param(
        "1", "Present", "0", "0", None, 
        (constants.INPUT_ERROR, constants.EMPTY_ATTENDANCE_MARKING_ID), 
        id="sad_no_attendance_marking_id"
    )
]

@pytest.mark.parametrize(
    "student_id, attendance_punctuality, tardy_minutes, cutting_minutes, attendance_id, expected", 
    attendance_marking_test_cases
)
def test_attendance_marking_validator(
    student_id, attendance_punctuality, 
    tardy_minutes, cutting_minutes, 
    attendance_id, expected):

    attendance_marking_info = helpers.AttendanceMarkingInfo(
        student_id, attendance_punctuality,
        tardy_minutes, cutting_minutes, 
        attendance_id
    )

    assert validators.validate_attendance_marking(attendance_marking_info) == expected


# =============== Account Registration Validator ===============
# NOTE: Please use placeholder names for the given name and surnames. Do not use a real name.

account_registration_test_cases = [

    # ========== Happy Path ==========
    pytest.param(
        "Joe", "Schmoe", "Average Joe", "8", "Camia", "Student", "Upon entering room A, do not, for some reason, expect 100 jars.",
        (False, None), 
        id="happy_path_student_account_registration"
    ),

    pytest.param(
        "Joe", "Schmoe", "Average Joe", None, None, "Teacher", "Upon entering room A, do not, for some reason, expect 100 jars.",
        (False, None), 
        id="happy_path_teacher_account_registration"
    ),

    # ========== Edge Cases ==========


    # ===== Edge Cases - Grade Level =====
    pytest.param(
        "Joe", "Schmoe", "Average Joe", "7", "Ruby", "Student", "Upon entering room A, do not, for some reason, expect 100 jars.",
        (False, None), 
        id="edge_grade_7_account"
    ),

    pytest.param(
        "Joe", "Schmoe", "Average Joe", "12", "A", "Student", "Upon entering room A, do not, for some reason, expect 100 jars.",
        (False, None), 
        id="edge_grade_12_account"
    ),

    # ===== Edge Cases - Given Name =====
    pytest.param(
        "Jo", "Schmoe", "Average Joe", "9", "Rubidium", "Student", "Upon entering room A, do not, for some reason, expect 100 jars.",
        (False, None), 
        id="edge_least_given_name_characters_possible"
    ),

    pytest.param(
        "Jojojojojo Jojojojojo Jojojojojo Jojojojojo Jojojojojo Jojojojojo Jojo", "Schmoe", "Average Joe", "9", "Rubidium", "Student", "Upon entering room A, do not, for some reason, expect 100 jars.",
        (False, None), 
        id="edge_most_given_name_characters_possible"
    ),

    pytest.param(
        "Joé", "Schmoe", "Average Joe", "9", "Rubidium", "Student", "Upon entering room A",
        (False, None), 
        id="edge_first_name_accent_letter"
    ),

    # ===== Edge Cases - Surname =====
    pytest.param(
        "Joe", "So", "Average Joe", "9", "Rubidium", "Student", "Upon entering room A",
        (False, None), 
        id="edge_least_surname_characters_possible"
    ),

    pytest.param(
        "Joe", "Jojojojojo Jojojojojo Jojojojojo Jojojojojo Jojojojojo Jojojojojo Jojo", "Average Joe", "9", "Rubidium", "Student", "Upon entering room A",
        (False, None), 
        id="edge_most_surname_characters_possible"
    ),

    pytest.param(
        "Joe", "Schmoé", "Average Joe", "9", "Rubidium", "Student", "Upon entering room A",
        (False, None), 
        id="edge_surname_name_accent_letter"
    ),

    # ===== Edge Cases - Account Password =====
    pytest.param(
        "Joe", "Schmoe", "Average Jo", "12", "A", "Student", "Speak word",
        (False, None), 
        id="edge_least_password_characters_possible"
    ),

    pytest.param(
        "Joe", "Schmoe", "Average Joe", "12", "A", "Student", "This is defenitely a long password. Hold up, let me add more characters to reach the edge case: Four",
        (False, None), 
        id="edge_most_password_characters_possible"
    ),

    # ========== Sad Paths ==========

    # ===== Sad Paths - Given Name =====

    pytest.param(
        "", "Schmoe", "Average Joe", "8", "Camia", "Student", "Upon entering room A, do not, for some reason, expect 100 jars.",
        (True, constants.EMPTY_GIVEN_NAME_MESSAGE), 
        id="sad_empty_given_name_case_1"
    ),

    pytest.param(
        " ", "Schmoe", "Average Joe", "8", "Camia", "Student", "Upon entering room A, do not, for some reason, expect 100 jars.",
        (True, constants.EMPTY_GIVEN_NAME_MESSAGE), 
        id="sad_empty_given_name_case_2"
    ),

    pytest.param(
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "Schmoe", "Average Joe", "8", "Camia", "Student", "Upon entering room A, do not, for some reason, expect 100 jars.",
        (True, constants.GIVEN_NAME_LENGTH_OUT_OF_RANGE), 
        id="sad_too_long_given_name"
    ),

    pytest.param(
        "J", "Schmoe", "Average Joe", "8", "Camia", "Student", "Upon entering room A, do not, for some reason, expect 100 jars.", 
        (True, constants.GIVEN_NAME_LENGTH_OUT_OF_RANGE), 
        id="sad_too_short_given_name"
    ),

    # ===== Sad Paths - Surname =====

    pytest.param(
        "Joe", "", "Average Joe", "8", "Camia", "Student", "Upon entering room A, do not, for some reason, expect 100 jars.",
        (True, constants.EMPTY_SURNAME_MESSAGE), 
        id="sad_empty_surname_case_1"
    ),

    pytest.param(
        "Joe", " ", "Average Joe", "8", "Camia", "Student", "Upon entering room A, do not, for some reason, expect 100 jars.", 
        (True, constants.EMPTY_SURNAME_MESSAGE), 
        id="sad_empty_surname_case_2"
    ),

    pytest.param(
        "Joe ", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "Average Joe", "8", "Camia", "Student", "Upon entering room A, do not, for some reason, expect 100 jars.",
        (True, constants.SURNAME_LENGTH_OUT_OF_RANGE), 
        id="sad_too_long_surname"
    ),

    pytest.param(
        "Joe", "S", "Average Joe", "8", "Camia", "Student", "Upon entering room A, do not, for some reason, expect 100 jars.",
        (True, constants.SURNAME_LENGTH_OUT_OF_RANGE), 
        id="sad_too_short_surname"
    ),

    # ===== Sad Paths - Username =====

    pytest.param(
        "Joe", "Schmoe", "", "8", "Camia", "Student", "Upon entering room A, do not, for some reason, expect 100 jars.", 
        (True, constants.EMPTY_USERNAME_MESSAGE), 
        id="sad_empty_username_case_1"
    ),

    pytest.param(
        "Joe", "Schmoe", " ", "8", "Camia", "Student", "Upon entering room A, do not, for some reason, expect 100 jars.",
        (True, constants.EMPTY_USERNAME_MESSAGE), 
        id="sad_empty_username_case_2"
    ),
    # ===== Sad Paths - Grade Level and Section =====

    # TODO:
    # [] Add Validation for whether the student account has a selected grade level and section
    # [] Throw error if the teacher account has an entry for grade level and section

    pytest.param(
        "Joe", "Schmoe", "Average Joe", "8", "Ruby", "Student", "Upon entering room A, do not, for some reason, expect 100 jars.",
        (True, constants.NOT_GRADE_SECTION_MATCH_MESSAGE), 
        id="sad_grade_section_account_mismatch"
    ),

    # ===== Sad Paths - Account Role =====

    pytest.param(
        "Joe", "Schmoe", "Average Joe", "8", "Camia", "", "Upon entering room A, do not, for some reason, expect 100 jars.",
        (True, constants.EMPTY_ROLE_MESSAGE), 
        id="sad_empty_role_case_1"
    ),

    pytest.param(
        "Joe", "Schmoe", "Average Joe", "8", "Camia", " ", "Upon entering room A, do not, for some reason, expect 100 jars.", 
        (True, constants.EMPTY_ROLE_MESSAGE), 
        id="sad_empty_role_case_2"
    ),
    
    pytest.param(
        "Joe", "Schmoe", "Average Joe", "8", "Camia", "Hi", "Upon entering room A, do not, for some reason, expect 100 jars.", 
        (True, constants.NOT_APPLICABLE_ROLE_ERROR), 
        id="sad_unapplicable_role"
    ),
    # ===== Sad Paths - Password =====
    
    pytest.param(
        "Joe", "Schmoe", "Average Joe", "8", "Camia", "Student", "wut",
        (True, constants.INVALID_PASSWORD_LENGTH_MESSAGE), 
        id="sad_account_password_too_short"
    ),

    pytest.param(
        "Joe", "Schmoe", "Average Joe", "8", "Camia", "Teacher", "I actually do not know what to insert here, so I'll make this sentence long enough to reach the limit",
        (True, constants.INVALID_PASSWORD_LENGTH_MESSAGE), 
        id="sad_account_password_too_long"
    )

]
@pytest.mark.parametrize(
    "account_given_name, account_surname, account_username, account_grade_level, account_grade_section, account_role, account_password, expected", 
    account_registration_test_cases
)
def test_account_registration_validator(
    account_given_name, account_surname, 
    account_username, account_grade_level, 
    account_grade_section, account_role, 
    account_password, expected
):
    
    entered_account_signup_info = helpers.AccountRegistration(
        account_given_name, account_surname,
        account_username, account_grade_level,
        account_grade_section, account_role,
        account_password
    )

    assert validators.validate_entered_account_info(entered_account_signup_info) == expected


"""
NOTE: This is a work in progress. Please do not overly focus on this part.
prcoess_attendance_creation_test_cases = [
    pytest.param(
        "9", "Sodium", "Computer Science 3", "03-24-2026", "9", 1,
        (8, "Camia", "Computer Science 2", 1, "2026-04-14" )
        (False, None, None), 
        id="happy_path_attendance_creation"
    ),
]


@pytest.mark.parametrize(
    "grade_level, grade_section, subject, date, period, creator_id, duplicate_attendance_results ,expected", 
    prcoess_attendance_creation_test_cases
)

def test_prcoess_attendance_creation(
    grade_level, grade_section, 
    subject, date, 
    period, creator_id, 
    expected, duplicate_attendance_results,
    mocker):

    mocked_duplicate_attendance_session = mocker.patch(
        "attendance_service.attendnace_repo.check_duplicate_attendance",
        return_value=duplicate_attendance_results)

    entered_attendance_session = helpers.AttendanceSessionInfo(
        grade_level, grade_section, 
        subject, date, 
        period, creator_id
    )
"""