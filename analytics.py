from database import get_student_intelligence, get_teacher_analytics


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

def show_student_intelligence(username):
    """
    Displays a student's academic intelligence profile.
    """

    data = get_student_intelligence(username)

    print("\n=== STUDENT PERFORMANCE PROFILE ===")

    # Overall performance
    print("Average Score:", str(data["average"]) + "%")

    print("Strongest Subject:", data["strongest_subject"])
    print("Weakest Subject:", data["weakest_subject"])

    print("\n--- SUBJECT BREAKDOWN ---")

    # Loop through each subject
    for subject, info in data["subject_breakdown"].items():

        avg = round((info["score"] / info["total"]) * 100, 2)

        print(f"\n{subject}")
        print("Attempts:", info["attempts"])
        print("Average:", str(avg) + "%")
