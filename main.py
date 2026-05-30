from auth import login, signup
from home import home
from database import initialize_database
from validation import validate_number

initialize_database()

def main():
    print("\n===== PAKA'S LEARNING APP =====")

    while True:
        print("\n1. Login\n2. Signup\n3. Exit")

        options = input("Select: ").strip()
        if validate_number(options) == False:
            print("Input should be a number")
            

        if options == "1":
            user = login()

            if user:
                break

        elif options == "2":
            signup()

        elif options == "3":
            return
        else:
            print("Invalid input")
        
    
    while True:

        print("\n=== MAIN MENU ===")
        print("1. Dashboard")
        print("2. Logout")

        choice = input("Select: ").strip()
        if validate_number(choice) == False:
            print("Input should be a number")
            

        if choice == "1":
            home(user)

        elif choice == "2":
            print("Logging Out")
            break 
        else:
            print("Invalid option")


main()