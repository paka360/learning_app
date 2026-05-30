#This file handles access control logic

from database import get_parent_students

def is_student(user):
    """Checks if user is a student"""

    return user["role"] == "student"

def is_teacher(user):
    """Checks if user is a teacher"""

    return user["role"] == "teacher"

def is_parent(user):
    """Checks if user is a parent"""

    return user["role"] == "parent"


def has_grade_access(user, resource_grade):
    """Checks id user has grade access"""

    return user["grade"] == resource_grade

def parent_has_children(parent_username, student_username):
    """Checks if parents have registered wards on the platform"""

    relationships = get_parent_students()

    for relationship in relationships:
        if relationship["parent_username"] == parent_username and relationship["student_username"] == student_username:

            return True
        
    return False


def teacher_qualified(teacher, grade):
    """Checks if teacher is qualified to teach the grade"""

    if is_teacher(teacher) == False:
        return False
    
    return teacher["grade"] == grade

