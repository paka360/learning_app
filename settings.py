from database import get_user, create_user, link_parent_student, get_parent_students, update_password
from validation import validate_number, validate_password
from auth import verify_password, hash_password


def view_profile(user):
    """Allows users to view their profile"""

    print("\n====PROFILE====")

    print("Username: "+ user["username"].title())
    print("Role: "+ user["role"].title())

def change_password(user):
    """Allows users to change their password"""

    saved_user = get_user(user["username"])

    current_password = input("Enter Current password: ")

    if verify_password(current_password, saved_user["password"]) == False:
        print("Incorrect password")
        return 
    
    else: 
        new_password = input("Enter new password: ")

        if validate_password(new_password) == False:
            print("Weak password. Please try again")
            return
        
        hashed_password = hash_password(new_password)

    success = update_password(user["username"], hashed_password)

    if success:
        print("Password updated successfully")


    
def settings_menu(user):
    """Allows users to make changes to their account"""

    while True:

        print("\n=== SETTINGS ===")

        print("1. View Profile")
        print("2. Change Password")
        print("3. Back")

        choice = input("Select: ")
        if validate_number(choice) == False:
            print("Input should be a number")
            return

        if choice == "1":
            view_profile(user)

        elif choice == "2":
            change_password(user)

        elif choice == "3":
            break

        else:
            print("Invalid Input")

def link_child(parent):
    """Allows parent users to link child accounts"""

    users = get_user()
    print("\n==== LINK CHILD ====")

    for user in users:
        if user["role"] == "student":
            print(user["username"] + " | " + user["grade"])

    student_username = input("\nEnter student username: ").lower().strip()
    success = link_parent_student(parent["username"], student_username)

    if success:
        print("Child account linked successfully")

    else:
        print("Child account already linked")


def get_parent_wards(parent_username):
    """Allows parents get access to the linked accounts of their children"""

    relationships = get_parent_students()
    children = []

    for relationship in relationships:
        if relationship["parent_username"] == parent_username:
            children.append(relationship["student_username"])

    return children




