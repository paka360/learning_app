from database import create_question, create_quiz, get_quiz_results, get_quizzes, get_questions, create_quiz_results, delete_quiz, get_teacher_quizzes, get_quiz_results_teacher
from validation import validate_number,safe_int


def view_quiz_history(user):
    """Allows users view results of previous quizzes"""

    results = get_quiz_results()

    print("\n==== QUIZ HISTORY ====")

    found = False

    for result in results:

        if result["username"] == user["username"]:
            print(result["quiz_title"] + "| Score: " + str(result["score"]) + "/" +str(result["total"]))

            found = True
            
    if found == False:
        print("You have no quiz history")


def take_quiz(user):
    """Main function which runs the quiz logic"""

    display_quizzes(user)


    try:
        while True:
            quiz_id = input("\nEnter quiz ID: ")
            if validate_number(quiz_id) == False:
                print("Input should be a number")
            
            else:
                break

        questions = get_questions(quiz_id)

        if len(questions) == 0:
            print("Quiz not found")
            return
        
        score = 0
        total = 0

        print("\n==== START QUIZ ====")
        for question in questions:
            print("\n" + question["question"])
            print("A. " + question["option1"])
            print("B. " + question["option2"])
            print("C. " + question["option3"])
            print("D. " + question["option4"])

            answer = input("\nAnswer: ")

            total += 1

            if answer.lower().strip() == question["answer"].lower().strip():
                print("Correct")
                score += 1

            else:
                print("Wrong. Correct answer is " + question["answer"])


        score_percent = (score/total) * 100
        print("\nFinal score: " + str(score_percent) + "%" )

        quizzes = get_quizzes()
        quiz_title = "Unknown"

        for quiz in quizzes:
            if quiz_id == str(quiz["id"]):
                quiz_title = quiz["title"]
        
        create_quiz_results(user["username"], quiz_title, score, total)


    except Exception as error:
        print(error)


def create_quiz_set(user):
    """Allows users to create quizzes """

    print("\n==== CREATE QUIZ ====")

    subject = input("Subject: ")
    grade = user["grade"]
    title = input("Quiz title: ")
    uploaded_by = user["username"]
    quiz_id = create_quiz(subject, title, grade, uploaded_by)

    print("\nADD QUESTION")
    while True:
        print("New Question ")
        question = input("Question: ")
        option1 = input("Option 1: ")
        option2 = input("Option 2: ")
        option3 = input("Option 3: ")
        option4 = input("Option 4: ")
        answer = input("Correct answer: ")

        create_question(quiz_id,question, option1 , option2, option3, option4, answer)

        again = input("\nAdd another question? (Y/N): ").lower().strip()
        if again != "y":
            break
    
    print("Quiz created successfully")


def display_quizzes(user):
    """Shows the list of available quizzes"""

    quizzes = get_quizzes()

    print("==== AVAILABLE QUIZZES ====")

    for quiz in quizzes:
        if quiz["grade"] == user["grade"]:
            print(str(quiz["id"]) + ". " + quiz["title"] + " (" + quiz["subject"] + ")")

    return quizzes



def delete_quiz_set(user):
    """Allows teachers to delete their quiz uploads"""

    quizzes = get_quizzes()

    if len(quizzes) == 0:
        print("\nNo quizzes have been uploaded")
        return
    
    display_quizzes(user)

    try: 
        while True:
            quiz_id = safe_int(input("\nEnter quiz ID to delete: "))

            if quiz_id == None:
                print("Invalid ID")

            elif quiz_id < 0:
                print("Invalid ID")

            else:
                success = delete_quiz(quiz_id, user["username"])

                if success:
                    print("Quiz deleted successfully")
                    break

                else:
                    print("Quiz not found")
                    break


    except ValueError as error:
        print(error)


def view_quiz_results(user):
    """Allows teachers view the results of their quizzes"""

    quizzes = get_teacher_quizzes(user["username"])

    if len(quizzes) == 0:
        print("You have not uploaded any quizzes")
        return
    
    print("\n==== MY QUIZZES ====")
    for quiz in quizzes:
        print(str(quiz["id"]) + ". " + quiz["title"])
    
    quiz_id = safe_int(input("\nEnter QUiz ID: "))

    selected_quiz = None

    for quiz in quizzes:
        if quiz_id == quiz["id"]:
            selected_quiz = quiz
            break

    if selected_quiz is None:
        print("Quiz not found")
        return
    
    results = get_quiz_results_teacher(selected_quiz["title"])

    if len(results) == 0:
        print("No attempts yet.")
        return
    
    print("\n=== QUIZ RESULTS ====")
    
    for result in results:
        print("Student: " + result["username"].title())
        print("Score: " + str(result["score"])+ "/" +str(result["total"]))

