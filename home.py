#Home Screen Module

from books import display_books, display_downloads, download_book, read_book, upload_book, view_favorites, add_favorites, recommend_books,continue_reading, view_uploads
from search import search_book
from stats import show_stats, parent_view_stats
from settings import settings_menu
from quiz import take_quiz, view_quiz_history, create_quiz_set
from validation import validate_number



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
        parent_home()

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
                    break
            

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
        print("3. Manage Classes")
        print("4. Library")
        print("5. Back")

        choice = input("Select: ").strip()
        if validate_number(choice) == False:
            print("Input should be a number")
            
        
        if choice == "1":
            upload_book(user)

        elif choice == "2":
            create_quiz_set(user)
        
        elif choice == "3":
            print("\n==== MANAGE CLASSES ====")

        elif choice == "4":

            while True:
                print("\n==== LIBRARY ====")
                print("1. View uploaded books")
                print("2. View Recommended books")
                print("3. Download books")
                print("4. View Downloads")
                print("5. Read book")
                print("6. Back")


                option = input("Select: ").strip()
                if validate_number(option) == False:
                    print("Input should be a number")
                    

                if option == "1":
                    view_uploads(user)

                elif option == "2":
                    display_books(user)
        
                elif option == "3":
                    download_book(user)
            
                elif option == "4":
                   display_downloads(user)

                elif option == "5":
                    read_book(user)

                elif option == "6":
                    break

                else:
                    print("Invalid input")
        
        elif choice == "5":
            break

        else:
            print("Invalid input")
            

def parent_home():
    """Displays menu for Parent account holders"""

    while True:
        
        print("\n ====PARENT DASHBOARD ====")
        print("1. monitor child activity")
        print("2. View child scores")
        print("3. Settings")
        print("4. Back")

        choice = input("Select: ")
        if validate_number(choice) == False:
            print("Input should be a number")
            

        if choice == "1":   
            parent_view_stats()
    
        elif choice == "2":
            print("\n==== CHILD SCORES ====")

        elif choice == "3":
            settings_menu()
        
        elif choice == "4":
            break

        else:
            print("Invalid option")


