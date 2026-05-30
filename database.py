import sqlite3

DATABASE_NAME = "learning_app.db"

def connect_database():
    """Connects my database to the app"""

    connection = sqlite3.connect(DATABASE_NAME)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """Creates database tables"""

    connection = connect_database()

    cursor = connection.cursor()

    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS 
                   users 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   username TEXT UNIQUE,
                   password TEXT,
                   role TEXT,
                   grade TEXT)
                   """)
    
        cursor.execute(""" CREATE TABLE IF NOT EXISTS books (

            id INTEGER PRIMARY KEY AUTOINCREMENT,    
            grade TEXT,
            subject TEXT,
            title TEXT,
            author TEXT,
            content TEXT,
            uploaded_by TEXT)

    """)

        cursor.execute("""
                   CREATE TABLE IF NOT EXISTS favorites(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT,
                   book_id INTEGER,
                   title TEXT,
                   subject TEXT,
                   grade TEXT)
                   """)
    
        cursor.execute("""
                   CREATE TABLE IF NOT EXISTS reading_history
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT,
                   book_id INTEGER,
                   title TEXT)
                   """)
    
        cursor.execute("""
                   CREATE TABLE IF NOT EXISTS downloads 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT, 
                   book_id INTEGER,
                   title TEXT,
                   grade TEXT,
                   content TEXT,
                   UNIQUE(username, book_id) )
                   """)
    
        cursor.execute("""
                   CREATE TABLE IF NOT EXISTS quizzes(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   subject TEXT,
                   grade TEXT,
                   title TEXT)
                   """)
    
        cursor.execute("""CREATE TABLE IF NOT EXISTS questions (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   quiz_id INTEGER,
                   question TEXT,
                   option1 TEXT,
                   option2 TEXT,
                   option3 TEXT,
                   option4 TEXT,
                   answer TEXT)
                   """)
    
        cursor.execute("""
                   CREATE TABLE IF NOT EXISTS quiz_results(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT, 
                   quiz_title TEXT, 
                   score INTEGER, 
                   total INTEGER)
                   """)
    
   
        cursor.execute("""
                   CREATE TABLE IF NOT EXISTS parent_students (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   parent_username TEXT,
                   student_username TEXT)
                   """)
        
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS statistics (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT,
                       activity TEXT)
                       """)
    

        # Save changes
        connection.commit()

    except sqlite3.Error as error:
        print("Database error")
        print(error)

    finally:
        connection.close()

    print("Database initialized")

def create_user(username, password, role, grade):
    """Create new user using relational database"""

    connection = connect_database()
    cursor = connection.cursor()

    try:
        cursor.execute("""
                       INSERT INTO users
                       (username, password, role, grade)
                       VALUES(?,?,?,?)
                       """, (username, password, role, grade))
        
        connection.commit()
        connection.close()
        return True
    
    except sqlite3.IntegrityError:
        print("Username already exists")
        connection.close()
        return False

def get_user(username):
    """Finds user in database when user tries to login"""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
                   SELECT * FROM users
                   WHERE username = ?
                   """,(username,))
    
    user = cursor.fetchone()
    connection.close()
    return user

def create_book(subject, title, author, content,grade, uploaded_by):
    """Adds a new book to the database"""

    connection = connect_database()
    cursor = connection.cursor()

    try:
        cursor.execute("""
                   INSERT INTO books
                   (subject, title, author, content, grade, uploaded_by)
                   VALUES (?,?,?,?,?,?)
                   """, (subject, title, author, content, grade, uploaded_by))
    
        connection.commit()

    except sqlite3.Error as error:
        print("Database error")
        print(error)

    finally: 
        connection.close()

def get_books():
    """Loads all books"""

    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute("""
    
                   SELECT * FROM books
                   """)
    
    books = cursor.fetchall()
    connection.close()
    return books

def search_book(book_id):
    """Allows users search for books by ID"""

    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT * FROM books
                   WHERE id = ?
                   """, (book_id))

    book = cursor.fetchone()
    connection.close()
    return book


def create_favorites(username, book_id, title, subject,grade):
    """Adds favorite books to database"""

    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT * FROM favorites
                   WHERE username = ?
                   AND book_id = ?
                   """, (username, book_id))
    
    existing = cursor.fetchone()
    if existing != None:
        connection.close()
        return False
    

    try:
        cursor.execute("""
                   INSERT INTO favorites
                   (username, book_id, title, subject, grade)
                   VALUES (?,?,?,?,?)
                   """, (username, book_id, title, subject, grade))
    
        connection.commit()

    except sqlite3.Error as error:
        print("Database error")
        print(error)
        
    finally:
        connection.close()
        return True

def get_favorites():
    """Loads all favorite books of the user"""

    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT * FROM favorites
                   """)
    
    favorites = cursor.fetchall()
    connection.close()
    return favorites


def create_reading_history(username, book_id, title):
    """Saves reading acitivity of users in database"""

    connection = connect_database()
    cursor = connection.cursor()

    try:
        cursor.execute("""
                   INSERT INTO reading_history
                   (username, book_id, title)
                   VALUES (?,?,?)
                   """, (username, book_id, title))
    
        connection.commit()

    except sqlite3.Error as error:
        print("Database error")
        print(error)

    finally:
        connection.close()


def get_reading_history():
    """Accesses reading history of users from database"""

    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT * FROM reading_history
                   """)
    
    history = cursor.fetchall()
    connection.close()
    return history

def create_download(username, book_id, title, grade, content):
    """Saves downloaded books of users"""

    connection = connect_database()
    cursor = connection.cursor()

    try: 
        cursor.execute("""
                   SELECT * FROM downloads
                   WHERE username = ?
                   AND book_id = ?
                   """, (username, book_id))
    
        existing = cursor.fetchone()
        if existing != None:
            connection.close()
            return False
    
        cursor.execute("""
                   INSERT INTO downloads
                   (username, book_id, title, grade, content)
                   VALUES (?,?,?,?,?)
                   """, (username, book_id, title, grade, content))
        connection.commit()
        return True

    except sqlite3.Error as error:
        print("Database error")
        print(error)

    finally: 
        connection.close()


def get_downloads():
    """Loads the downloads of users from the database"""

    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT * FROM downloads
                   """)
    downloads = cursor.fetchall()
    connection.close()

    return downloads

def create_quiz(subject, title, grade):
    """Creates a quiz """

    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute("""
                   INSERT INTO quizzes
                   (subject, title, grade)
                   VALUES (?,?,?)
                   """,(subject, title, grade))
    connection.commit()
    quiz_id = cursor.lastrowid
    connection.close()
    return quiz_id


def create_question(quiz_id, question, option1, option2, option3, option4, answer):
    """Adds questions to quiz """

    connection = connect_database()
    cursor = connection.cursor()

    try:
        cursor.execute("""
                   INSERT INTO questions
                   (quiz_id, question, option1, option2, option3, option4, answer)
                   VALUES (?,?,?,?,?,?,?)
                   """, (quiz_id, question, option1, option2, option3, option4, answer))
    
        connection.commit()
    
    except sqlite3.Error as error:
        print("Database error")
        print(error)

    finally:
        connection.close()


def get_quizzes():
    """Loads the quizzes available"""

    connection = connect_database()
    cursor = connection.cursor()
    
    cursor.execute("""
                   SELECT * FROM quizzes
                   """)
    
    quizzes = cursor.fetchall()
    connection.close()
    return quizzes

def get_questions(quiz_id):
    """Loads the quizzes available"""

    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT * FROM questions
                   WHERE quiz_id = ?
                   """, (quiz_id))
    
    questions = cursor.fetchall()
    connection.close()
    return questions

def create_quiz_results(username, quiz_title, score, total):
    """Saves the quiz results"""

    connection = connect_database()
    cursor = connection.cursor()

    try: 
        cursor.execute("""
                   INSERT INTO quiz_results
                   (username, quiz_title, score, total)
                   VALUES (?,?,?,?)
                   """,(username, quiz_title, score, total))
    
        connection.commit()

    except sqlite3.Error as error:
        print("Database error")
        print(error)

    finally:
        connection.close()

def get_quiz_results():
    """Loads the quiz results available"""

    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT * FROM quiz_results
                   """)
    
    results = cursor.fetchall()
    connection.close()
    return results

def link_parent_student(parent_username, student_username):
    """Links parent accounts to student accounts"""

    connection = connect_database()
    cursor = connection.cursor()

    try:
        cursor.execute("""
                   SELECT * FROM parent_students
                   WHERE parent_username = ?
                   AND student_username = ?
                   """,(parent_username, student_username))
        
        existing = cursor.fetchone()
        if existing != None:
            connection.close()
            return False
        
        cursor.execute("""
                   INSERT INTO parent_students
                   (parent_username, student_username)
                   VALUES (?,?)
                   """, (parent_username, student_username))
        
        connection.commit()

    except sqlite3.Error as error:
        print("Database error")
        print(error)

    finally:
        connection.close()
        return True 
    

def get_parent_students():
    """Loads the linked accounts of parents and students"""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
                   SELECT * FROM parent_students
                   """)
    
    relationships = cursor.fetchall()
    connection.close()
    return relationships


def get_logs():
    """Loads the logs of users"""

    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT * FROM statistics
                   """)
    
    statistics = cursor.fetchall()
    connection.close()
    return statistics

def track_activity(username, activity):
    """Logs the actions of users on the app"""

    connection = connect_database()
    cursor = connection.cursor()

    try:
        cursor.execute("""
                   INSERT INTO statistics
                   (username, activity)
                   VALUES (?,?)
                   """, (username, activity))
    
        connection.commit()

    except sqlite3.Error as error:
        print("Database error")
        print(error)

    finally:
        connection.close()
    

def update_password(username, hashed_password):
    """Updates the password of the user"""

    connection = connect_database()
    cursor = connection.cursor()

    try:
        cursor.execute("""
                       UPDATE users
                       SET password = ?
                       WHERE username = ?
                       """, (hashed_password, username))
        
        connection.commit()
        return True
    
    except sqlite3.Error as error:
        print(error)
        return False
    
    finally:
        connection.close()

def delete_upload(book_id, username):
    """Allows users to delete their uploads"""

    connection = connect_database()
    cursor = connection.cursor()

    try:
        cursor.execute("""
                   DELETE FROM books
                   WHERE id = ?
                   AND uploaded_by = ?
                   """, (book_id, username))
        
        connection.commit()
        return True
    
    except sqlite3.Error as error:
        print(error)
        return False
    
    finally:
        connection.close()

def update_book(book_id, username, new_title, new_content):
    """Allows teachers to update the books they uploaded"""

    connection = connect_database()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
                       UPDATE books
                       SET title = ?
                       content = ?
                       WHERE id = ?
                       AND uploaded_by = ?
                       """, (new_title, new_content, book_id, username ))
        
        connection.commit()
        return True
    
    except sqlite3.Erroe as error:
        print(error)
        return False
    
    finally:
        connection.close()
