#Login logic
from database import create_user, get_user, get_parent_students, link_parent_student
import bcrypt
from permissions import is_parent, is_student, is_teacher
from validation import validate_grade, validate_password, validate_role, validate_username, validate_number


def hash_password(password):
    """Converts passwords to hashes for secure storage"""

    password_bytes = password.encode()
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode()


def verify_password(entered_password, stored_hash):
    """Verifies the password the user enters with the stored hash"""

    entered_bytes = entered_password.encode()
    stored_bytes = stored_hash.encode()

    return bcrypt.checkpw(entered_bytes, stored_bytes)


def signup():
    """Allows users sign up and create an account"""

    print("\n===== SIGNUP ====")
    while True:
        username = input("Choose username: ").strip().lower()
        if validate_username(username) == False:
            print("Try again ")
        else:
            break
    
    while True:
        choice = input("Choose role \n1. Student\n2. Teacher\n3. Parent\nSelect: ").lower().strip()
        if validate_number(choice) == False:
            print("\nTry again")      
        else:
            if choice == "1":
                role = "student"
            elif choice == "2":
                role = "teacher"
            elif choice == "3":
                role = "parent"
            break

    
    grade = ""
    if role == "student" or role == "teacher":
        while True:
            grade = input("Enter your grade/class: ").strip().lower()
            if validate_grade(grade) == False:
                print("Invalid grade")
            else:
                break

    while True:
        password = input("Set password: ").strip()
        cpassword = input("Confirm password: ").strip()

        if validate_password(password,cpassword) == False:
            print("Make sure your password is at least 4 characters long and is the same in both fields")

    
        else:
            password = hash_password(password)
            create_user(username, password, role, grade)
            print("Sign up completed")
            break
            
    

def login():
    """Collects user credentials and checks if username and password match. If they do it returns user data to main programme"""

    username = input("Username: ")
    password = input("Password: ")
    user = get_user(username)

    if user == None:
        print("User not found")
        return None
    
    if verify_password(password, user["password"]) == False:
        print("Incorrect username or password")
        return None

    print("Login successful") 

    return user   
    

