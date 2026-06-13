#Home Screen Module

from books import display_books, display_downloads, download_book, read_book, upload_book, view_favorites, add_favorites, recommend_books,continue_reading, view_uploads,delete_book, show_teacher_analytics
from search import search_book
from stats import show_stats, parent_view_stats
from settings import settings_menu
from quiz import take_quiz, view_quiz_history, create_quiz_set,delete_quiz_set, view_quiz_results
from validation import validate_number
from permissions import get_children, parent_has_children
from database import link_parent_student


def home(user):
    """Routes users to the corrent dashboard based on roles"""

    role = user["role"]

    print("\n=== MAIN DASHBOARD ===")
    print("Welcome " + user["username"].upper() +" "+ user["role"].upper() )

    if role == "student":
        student_home(user)
    
    elif role == "teacher":
        teacher_home(user)

    elif role == "parent":
        parent_home(user)

    else:
        print("Unknown role")

def student_home(user):
    """Displays menu for student acccount holders"""

    while True: 

        print("\n=== STUDENT DASHBOARD ===")
        print("\n1. Library")
        print("2. Take quiz")
        print("3. Quiz History")
        print("4. Search Books")
        print("5. View Statistics")
        print("6. Settings")
        print("7. Back")

        choice = input("Select: ")
        if validate_number(choice) == False:
            print("Input should be a number")
    
        if choice == "1":
            while True:
                print("\n=== LIBRARY ===")
                print("1. View Available Books")
                print("2. Download Books")
                print("3. View Downloads")
                print("4. Read Book")
                print("5. Continue Reading")
                print("6. Add Favorite Book")
                print("7. View Favorite Books")
                print("8. Recommended Books")
                print("9. Back")


                option = input("Select: ")
                if validate_number(option) == False:
                    print("Input should be a number")
                    

                if option == "1":
                    display_books(user)

                elif option == "2":
                    download_book(user)
        
                elif option == "3":
                    display_downloads(user)
            
                elif option == "4":
                    read_book(user)
             
                elif option == "5":
                   continue_reading(user)

                elif option == "6":
                   add_favorites(user)

                elif option == "7":
                   view_favorites(user)
            
                elif option == "8":
                    recommend_books(user)
            
                elif option == "9":
                    break

                else: 
                    print("Invalid input")
                    
            
        elif choice == "2":
            take_quiz(user)
    
        elif choice == "3":
            view_quiz_history(user)
            
   
        elif choice == "4":
            search_book()

        elif choice == "5":
            show_stats(user)

        elif choice == "6":
            settings_menu(user)
        
        elif choice == "7":
            break

        else: 
            print("Invalid Input")


def teacher_home(user):
    """Displays menu for teacher account holders"""

    print("\n==== TEARCHER DASHBOARD ====")

    while True: 
        print("\n1. Upload Book")
        print("2. Create Quiz")
        print("3. Delete Quiz")
        print("4. Manage Classes")
        print("5. Library")
        print("6. Analytics")
        print("7. Back")

        choice = input("Select: ").strip()
        if validate_number(choice) == False:
            print("Input should be a number")
            
        
        if choice == "1":
            upload_book(user)

        elif choice == "2":
            create_quiz_set(user)
               
        elif choice == "3":
            delete_quiz_set(user)
            
        elif choice == "4":
            print("\n==== MANAGE CLASSES ====")
            view_quiz_results(user)   
        
        elif choice == "5":

            while True:
                print("\n==== LIBRARY ====")
                print("1. View uploads")
                print("2. Delete uploads")
                print("3. View Recommended books")
                print("4. Download books")
                print("5. View Downloads")
                print("6. Read book")
                print("7. Back")


                option = input("Select: ").strip()
                if validate_number(option) == False:
                    print("Input should be a number")
                    

                if option == "1":
                    view_uploads(user)

                elif option == "2":
                    delete_book(user)
        
                elif option == "3":
                    display_books(user)
            
                elif option == "4":
                   download_book(user)

                elif option == "5":
                    display_downloads(user)

                elif option == "6":
                    read_book(user)

                elif option == "7":
                    break

                else:
                    print("Invalid input")
            

        elif choice == "6":
            show_teacher_analytics(user)

        elif choice == "7":
            break

        else:
            print("Invalid input")
            

def parent_home(user):
    """Displays menu for Parent account holders"""

    while True:
        
        print("\n ====PARENT DASHBOARD ====")
        print("1. Link child account")
        print("2. View linked accounts")
        print("3. monitor child activity")
        print("4. View child scores")
        print("5. Settings")
        print("6. Back")

        choice = input("Select: ")
        if validate_number(choice) == False:
            print("Input should be a number")
        
        if choice == "1":
            print("==== LINK ACCOUNT ====")
            student_username = input("Enter the username of your ward: ").lower().strip()

            if parent_has_children(user["username"], student_username):
                print("Account already linked. ")
                
            
            else:
                success = link_parent_student(user["username"], student_username)
                if success:
                    print("Account linked successfully")
                    
            
                else:
                    link_parent_student(user["username"], student_username)
                    print("Student not found")
                    
                
    
        elif choice == "2":
            children = get_children(user["username"])
            
            print("\n==== LINKED ACCOUNTS ====")

            for i, child in enumerate(children):
                print(str(i +1) +  ". " + child)

        elif choice == "3":   
            parent_view_stats(user)
    
        elif choice == "4":
            print("\n==== CHILD SCORES ====")

        elif choice == "5":
            settings_menu(user)
        
        elif choice == "6":
            break

        else:
            print("Invalid option")


