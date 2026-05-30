from database import create_book, search_book, get_books,create_favorites, get_favorites, create_reading_history, get_reading_history, get_downloads, create_download, track_activity
from permissions import has_grade_access, teacher_qualified
from validation import safe_int


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

    try:
        choice = safe_int(input("\nSelect subject ID: "))
        selected_subject = subjects[choice - 1]

    except ValueError:
        print("Invalid subject")
        return
    

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
                success = create_download(user["username"],book["id"], book["title"], book["grade"], book["content"])
                
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

    downloads = get_downloads()

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

    books = get_downloads()

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
                print(book["content"])

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
        content = input("Book content: ")
        subject = input("Subject: ")
 
        create_book(subject, title, author, content, grade, user["username"])
        print("Book uploaded successfully")

    except ValueError:
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
    """Allows teachers to their uploads"""

    view_uploads(user)
    try: 
        book_id = safe_int(input("\nEnter book ID to delete: "))

        if book_id == None:
            print("Invalid ID")
            return
        
        success = delete_book(book_id, user["username"])

        if success:
            print("Book deleted successfully")

        else:
            print("Deletion failed")

    except ValueError as error:
        print(error)



            
        

