from database import get_logs
from database import link_parent_student
from permissions import get_children

def show_stats(user):
    """Allows users to view their stats on the app"""

    activities = get_logs()

    book_downloads = 0
    books_read = 0

    for activity in activities:

        #checks the records for only the current user
        if activity["username"] == user["username"]:

            if activity["activity"] == "download":
                book_downloads += 1

            elif activity["activity"] == "read":
                books_read += 1
    

    print("\n===LEARNING STATISTICS===")
    print("Books Downloaded: "+ str(book_downloads))
    print("Books read: "+ str(books_read))


def parent_view_stats(user):
    """Allows parents view the stats of their wards"""

    progress = get_logs()
    
    children = get_children(user["username"])

    if len(children) == 0:
        print("Link account of child to view their stats.")
        return

    print("\n ==== CHILD MONITOR ====")

    child_username = input("Enter child username: ").lower().strip()

    book_downloads = 0
    books_read = 0

    for activity in progress:
        if activity["username"] == child_username:

            if activity["activity"] == "downloads":
                book_downloads = book_downloads + 1

            elif activity["activity"] == "read":
                books_read = books_read + 1

    print("\n ==== CHILD STATISTICS ====")

    print("Child Username: "+ child_username)
    print("Books Downloaded: "+ str(book_downloads))
    print("Books read: "+ str(books_read))

    





