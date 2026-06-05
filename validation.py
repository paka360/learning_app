#This file centralizes input validation rules
from database import get_user

def validate_username(username):
    """Validates the username entered by the user"""

    username = username.strip().lower()

    if len(username) < 3:
        print("Username should be more than 3 characters")
        return False
    
    if len(username) > 20:
        print("Username should be less than 20 characters")
        return False
    
    user = get_user(username)
    if user:
        print("Username already exists")
        return False
    
    return True

def validate_password(password, cpassword):
    """Validates the password users set for their accounts"""

    if len(password) < 4:
        return False
    
    if password != cpassword:
        return False

    return True


def validate_role(role):
    """Validates the roles users input"""

    valid_roles = ["student", "teacher", "parent"]

    return role in valid_roles


def validate_grade(grade):
    """Validates the grades users input"""

    grade = grade.strip().lower()

    if grade == "":
        return False
    
    if len(grade) > 20:
        return False
    
    return True

def validate_number(value):
    """Validates the numeric menu input"""

    return value.isdigit()

def safe_int(value):
    """Helps with error handling by returning None when no input is entered"""

    try:
        return int(value)
    
    except ValueError:
        return None

