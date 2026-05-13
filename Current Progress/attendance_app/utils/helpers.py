import bcrypt
from dataclasses import dataclass
from typing import Dict, Tuple

def hash_password(password):
    pw_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(pw_bytes, salt)
    return hashed_pw

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

@dataclass
class AccountRegistration:
    given_name: str
    surname: str
    identifier: str
    grade_level: str | None
    grade_section: str
    role: str
    password: str