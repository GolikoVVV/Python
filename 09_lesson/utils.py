import random
import string
from sqlalchemy import text
from database import session


def generate_random_name():
    """Генерирует имя студента: Student_abc123"""
    return "Student_" + "".join(random.choices(string.ascii_letters, k=8))


def generate_random_subject_name():
    """Генерирует имя предмета: Subject_ABC123"""
    return "Subject_" + "".join(random.choices(string.ascii_uppercase, k=6))


def cleanup_student(student_id):
    """Жёстко удаляет студента по ID"""
    session.execute(text("DELETE FROM students WHERE id = :id"), 
                    {"id": student_id})
    session.commit()


def cleanup_subject(subject_id):
    """Жёстко удаляет предмет по ID"""
    session.execute(text("DELETE FROM subjects WHERE id = :id"), 
                    {"id": subject_id})
    session.commit()