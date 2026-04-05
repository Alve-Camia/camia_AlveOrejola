# attendance_service.py

from attendance_app.db import user_repo, db
from attendance_app.db.db import get_db
from attendance_app.utils import validators, constants, helpers
from datetime import datetime
import bcrypt

db.init_db()

# ========== Attendance Logic ==========
# Create Attendance

def parse_attendance_dates(input_start_date, input_start_time, input_end_date, input_end_time):
    start_date = datetime.strptime(input_start_date, constants.DATE_FORMAT).date()
    start_time = datetime.strptime(input_start_time, constants.TIME_FORMAT).time()
    end_date = datetime.strptime(input_end_date, constants.DATE_FORMAT).date()
    end_time = datetime.strptime(input_end_time, constants.TIME_FORMAT).time()
    
    start_datetime = datetime.combine(start_date, start_time)
    end_datetime = datetime.combine(end_date, end_time)

    return start_datetime, end_datetime


def validate_create_input(attendance_name, input_start_date, input_start_time, input_end_date, input_end_time, attendance_password, minutes_late, user):
    
    if not user:
        return True, constants.AUTH_ERROR, "No account detected.\nPlease be logged in to create attendance.", None

    # Step 1: Check if user input follows prescribed format
    validator_error, validator_message = validators.create_validator_engine(
        attendance_name, 
        input_start_date, 
        input_start_time, 
        input_end_date, 
        input_end_time, 
        attendance_password, 
        minutes_late)
    
    if validator_error:
        return True, validator_error, validator_message, None
    
    if not minutes_late.isdigit():
        return True, "Input Error", "Grace period can neither be a non-digit nor a non-natural number\nPlease enter a grace period integer between 1-30 minutes.", None
    
    minutes_late = int(minutes_late)  
    
    # Step 2: Check if there are logical inconsistencies with timeframe of user input
    start_datetime, end_datetime = parse_attendance_dates(input_start_date, input_start_time, input_end_date, input_end_time)
    
    timeframe_attendance_error = validators.validate_timeframe(start_datetime, end_datetime)

    if timeframe_attendance_error:
        return True, "Input Error", timeframe_attendance_error, None
    
    attendance_info = {
        "name": attendance_name,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "attendance_password": attendance_password,
        "minutes_late": minutes_late,
        "user": user
    }

    return False, None, None, attendance_info

# Fillout Attendance
def validate_fillout_input(user, attendance_name, attendance_password):
    with get_db() as conn:

        # Check if attendance exists in data storage
        existing_attendance = db.check_attendance_existance(conn, attendance_name)
        if not existing_attendance:
            return helpers.error_response(
                "Input Error", 
                "Attendance name and password don't match.\nPlease recheck your attendance inputs, and try again."
            ) 
        
        # Check if user input matches with prescribed format
        fillout_error, fillout_message = validators.fillout_attendance_validator(user, attendance_name, attendance_password, existing_attendance)
        if fillout_error:
            return helpers.error_response(fillout_error, fillout_message)

        stored_name, start_datetime, end_datetime, minutes_late, stored_hash, countercheck, question, hashed_answer = existing_attendance

        # Check whehter attendance recording is on time
        now = datetime.now()
        if now > datetime.fromisoformat(end_datetime):
            return helpers.error_response(
                "Input Error",
                "The following attendance has closed and no longer accept entries\nRefer to your instructor if there is a mistake."
            )
        
        # Check if entered passwrod corresponds with attendance
        if not bcrypt.checkpw(attendance_password.encode(), stored_hash.encode()):
            return helpers.error_response(
                "Input Error",  
                "Attendance name and password don't match.\nPlease recheck your attendance inputs, and try again."
            )
        
        # Check if user has already submitted attendance
        if db.check_already_submmited(conn, attendance_name, user):
            return helpers.error_response(
                "Input Error", 
                "You have already filled out this attendance."
            )
    
    # Valid Input
    return {
        "error_status": False,
        "error_type": None,
        "error_message": None,
        "data": {
            "stored_name": stored_name,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
            "minutes_late": minutes_late,
            "stored_hash": stored_hash,
            "countercheck": countercheck,
            "question": question,
            "hashed_answer": hashed_answer
        }
    }

def validate_countercheck_input(response, hashed_answer):
    
    if not response or not response.strip():
        return helpers.error_response("Input Error", "Countercheck response can not be empty.\nPlease enter your response.")
            
    if hashed_answer and not bcrypt.checkpw(response.encode(), hashed_answer.encode()):
        return helpers.error_response("Input Error", "Countercheck response doesn't match with the answer.\nPlease try again.")
    
    return {
        "error_status": False,
        "error_type": None,
        "error_message": None,
        "data": None
    }