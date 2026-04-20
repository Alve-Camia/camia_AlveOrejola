import bcrypt

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