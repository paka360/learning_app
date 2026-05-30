from database import get_books

def search_book():
    """Allows users to search for books"""

    books = get_books()

    keyword = input("Search books: ")

    keyword = keyword.lower().strip()

    print("\n ===SEARCH RESULTS===")

    found = False

    for book in books:
        title = book["title"].lower().strip()
        author = book["author"].lower().strip()
        subject = book["subject"].lower().strip()

        if keyword in title or keyword in author or keyword in subject:
            print(str(book["ID"]) + ". " + book["title"] + " by " + book["author"])
            found = True

    if found == False:
        print("No match found")


