from database import create_book, search_book, get_books,create_favorites, get_favorites, create_reading_history, get_reading_history, get_downloads, create_download, track_activity, delete_upload, get_teacher_analytics
from permissions import has_grade_access, teacher_qualified
from validation import safe_int
import os
import subprocess
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import shutil



def display_books(user):
    """Displays all available books to the user"""

    books = get_books()
    subjects = []

    if len(books) == 0:
        print("No books available")
        return

    for book in books:
        if has_grade_access(user, book["grade"]):
            if book["subject"] not in subjects:
                subjects.append(book["subject"])

    print("\n ==== BOOK SUBJECTS ====")
    for i, subject in enumerate(subjects):
        print(str(i + 1) + ". " + subject)
    
    while True:
        try:
            choice = safe_int(input("\nSelect subject ID: "))
            if choice > len(subjects) or choice < 0:
                print("Invalid input")

            else:
                selected_subject = subjects[choice - 1]
                break

        except ValueError:
            print("Invalid subject")
            
    

    print("\n---AVAILABLE BOOKS---")

    
    for book in books:

        if book["subject"] == selected_subject:

            print( "\nID: "+ str(book["id"]) )
            print("Title: "+  book["title"])
            print("Author: "+ book["author"])
            print("Class: "+ str(book["grade"]))


def download_book(user):
    """Allows users to download books and save to their local device for offline use"""

    books = get_books()

    display_books(user)

    if len(books) == 0:
        return

    try: 
        book_id = safe_int(input("\nEnter the book ID you wish to download: "))

        for book in books:
            if book["id"] == book_id:
                success = create_download(user["username"],book["id"], book["title"], book["grade"], book["file_path"])
                
                if success:
                    print("Book downloaded successfully")
                    
                    track_activity(user["username"], "download") 
                    return
                        
                else:
                    print("Book already downloaded")
                    return
                
            
        print("Book not found")

    except ValueError:
        print("Invalid input")

def display_downloads(user):
    """Displays downloaded books to users"""

    downloads = get_downloads(user["username"])

    print("\n====DOWNLOADED BOOKS====")
    found = False

    for book in downloads:
        if book["username"] == user["username"]:
            print(str(book["book_id"]) + ". " + book["title"])
            found = True

    if found == False:
        print("You have no downloads")
        

def read_book(user):
    """Allows users to read the contents of their books"""

    books = get_downloads(user["username"])

    print("\n===READ BOOK===")

    if len(books) == 0:
        print("No downloaded books")
        return
    
    
    for book in books:

        for book in books:
            if book["username"] == user["username"]:
                print(str(book["id"]) + ". " + book["title"])

    try: 
        book_id = safe_int(input("\nEnter book ID to open: "))

        for book in books:
            if book["id"] == book_id:
                print("\n=== " +book["title"] + " ===")

                track_activity(user["username"], "read")    
                subprocess.run(["xdg-open", book["file_path"]])

                create_reading_history(user["username"], book["id"], book["title"])
                return
            
        print("Book not found.")

    except ValueError:
        print("Invalid input")

def continue_reading(user):
    """ALlows users to continue reading where they left off"""

    history = get_reading_history()
    print("\n====CONTINUE READING====")

    found = False

    reversed_history = history[::-1]

    shown_books = []

    for record in reversed_history:
        if record["username"] == user["username"]:
            if record["book_id"] not in shown_books:
                print(str(record["book_id"]) + ". " + record["title"])

                shown_books.append(record["book_id"])
                found = True

    if found == False:
        print("No reading history")

 
def upload_book(user):
    """Allows users to upload books to the app"""

    books = get_books()

    print("====UPLOAD BOOK====")

    try:
        title = input("Book Title: ")
        author = input("Book author: ")
        grade = user["grade"]
        subject = input("Subject: ")
        file_path = choose_file()
        if not os.path.exists(file_path):
            print("file not found")
            return
        
        filename = os.path.basename(file_path)

        destination_path = os.path.join("uploads", filename)

        
        shutil.copy(file_path, destination_path)
        
 
        create_book(subject, title, author, grade, user["username"],destination_path)
        print("Book uploaded successfully")

    except ValueError:
        print("Upload failed")
        print("Error")
        return



def view_uploads(user):
    """Allows users to view their book uploads"""

    uploads = get_books()
    print("\n==== MY UPLOADS ====")

    found = False

    for upload in uploads:
        if upload["uploaded_by"] == user["username"]:
            found = True

            print(str(upload["id"]) + ". " + upload["title"] + " | " + upload["subject"] + " | Grade: " + upload["grade"] )

    if found == False:
        print("No uploads")
        return False


def add_favorites(user):
    """Saves the favorite books of users"""

    books = get_books()


    print("\n====ADD FAVORITES====")
    
    for book in books:
        print(str(book["id"]) + ". " + book["title"])

    try:
        book_id = safe_int(input("\nEnter book ID: "))

        for book in books:
            if book_id == book["id"]:
                success = create_favorites(user["username"],
                                           book["id"],
                                           book["title"],
                                           book["subject"],book["grade"])
                
                if success:
                    print("Book added to favorites successfully")
                    return
                
                else:
                    print("Book already saved to favorites")
                    return
        
        print("Book not found")
    
    except ValueError:
        print("Invalid input")

def view_favorites(user):
    """Allows users view their favorite books"""

    favorites = get_favorites()

    print("\n==== FAVORITE BOOKS ====")

    found = False

    for favorite in favorites:
        if favorite["username"] == user["username"]:
            print(str(favorite["book_id"]) + ". " + favorite["title"])
            found = True 

    if found == False:
        print("No books in Favorites")
    

def recommend_books(user):
    """Recommends books to users based on their preferences"""

    books = get_books()
    favorites = get_favorites()

    print("\n=====RECOMMENDED BOOKS====")

    favorite_subjects = []

    for favorite in favorites:
        if favorite["username"] == user["username"]:
            if favorite["subject"] not in favorite_subjects:

                favorite_subjects.append(favorite["subject"])

    if len(favorite_subjects) == 0:
        print("No book found")
        return
    
    shown_books = []

    for book in books:
        if book["subject"] in favorite_subjects:
            if book["id"] not in shown_books:
                print("[" + book["subject"] + "] " + book["title"])
                shown_books.append(book["id"])


def delete_book(user):
    """Allows teachers to delete their uploads"""

    try: 

        if view_uploads(user) == False:
            return
        
        book_id = safe_int(input("\nEnter book ID to delete: "))

        if book_id == None:
            print("Invalid ID")
            return
        
        success = delete_upload(book_id, user["username"])

        if success:
            print("Book deleted successfully")

        else:
            print("Book not found")

    except ValueError as error:
        print(error)



def choose_file():
    root = Tk()
    root.withdraw()

    file_path = askopenfilename(title = "Select a book", filetypes = [("Supported File", "*.pdf *.txt. *.docx *.pptx"), ("All Files", "*.*")])

    root.destroy()
    return file_path    
        

def show_teacher_analytics(user):
    """Displays teacher analytics dashboard"""

    data = get_teacher_analytics(user["username"])

    print("\n==== TEACHER ANALYTICS ====")
    print("Books Uploaded: ", data["books_uploaded"])
    print("Quizzes Created: ", data["quizzes_uploaded"])
    print("Total Quiz Attempts: ", data["total_attempts"])
    print("Average Score: ",str(data["average_score"]) + "%")

    print("Best Performing Quiz: ", data["best_quiz"])
    print("Worst Peforming Quiz: ", data["worst_quiz"])
