from sqlalchemy import text
from database import session
from utils import (
    generate_random_name,
    generate_random_subject_name,
    cleanup_student,
    cleanup_subject,
)


def test_create_student():
    """Позитивный тест: добавление студента"""
    name = generate_random_name()
    email = f"{name.lower()}@example.com"

    result = session.execute(
        text(
            "INSERT INTO students (name, email, deleted_at) "
            "VALUES (:name, :email, NULL) RETURNING id"
        ),
        {"name": name, "email": email},
    )
    student_id = result.scalar()
    session.commit()

    try:
        fetched = session.execute(
            text("SELECT name, email FROM students WHERE id = :id"), {"id": student_id}
        ).fetchone()

        assert fetched is not None, "Студент не найден в БД"
        assert fetched.name == name
        assert fetched.email == email
        print(f"✅ Студент создан: {name} (ID: {student_id})")
    finally:
        cleanup_student(student_id)


def test_update_student():
    """Позитивный тест: изменение данных студента"""
    original_name = generate_random_name()
    original_email = f"{original_name.lower()}@example.com"

    result = session.execute(
        text(
            "INSERT INTO students (name, email, deleted_at) "
            "VALUES (:name, :email, NULL) RETURNING id"
        ),
        {"name": original_name, "email": original_email},
    )
    student_id = result.scalar()
    session.commit()

    try:
        new_name = original_name + "_Updated"
        new_email = f"updated_{original_name.lower()}@example.com"

        session.execute(
            text("UPDATE students SET name = :name, email = :email WHERE id = :id"),
            {"name": new_name, "email": new_email, "id": student_id},
        )
        session.commit()

        fetched = session.execute(
            text("SELECT name, "
            "email FROM students WHERE id = :id"), {"id": student_id}
        ).fetchone()

        assert fetched.name == new_name
        assert fetched.email == new_email
        print(f"✅ Студент обновлён: {new_name}")
    finally:
        cleanup_student(student_id)


def test_soft_delete_student():
    """Позитивный тест: мягкое удаление студента"""
    name = generate_random_name()
    email = f"{name.lower()}@example.com"

    result = session.execute(
        text(
            "INSERT INTO students (name, email, deleted_at) "
            "VALUES (:name, :email, NULL) RETURNING id"
        ),
        {"name": name, "email": email},
    )
    student_id = result.scalar()
    session.commit()

    try:
        active = session.execute(
            text("SELECT 1 FROM students WHERE id = :id AND deleted_at IS NULL"),
            {"id": student_id},
        ).fetchone()
        assert active is not None, "Студент не был создан"

        session.execute(
            text("UPDATE students SET deleted_at = NOW() WHERE id = :id"),
            {"id": student_id},
        )
        session.commit()

        is_deleted = session.execute(
            text("SELECT deleted_at FROM students WHERE id = :id"), 
            {"id": student_id}
        ).fetchone()

        assert is_deleted.deleted_at is not None
        print(f"✅ Студент помечен как удалённый: ID {student_id}")
    finally:
        cleanup_student(student_id)


def test_delete_subject():
    """Позитивный тест: мягкое удаление предмета"""
    subject_name = generate_random_subject_name()

    result = session.execute(
        text(
            "INSERT INTO subjects (name, deleted_at) "
            "VALUES (:name, NULL) RETURNING id"
        ),
        {"name": subject_name},
    )
    subject_id = result.scalar()
    session.commit()

    try:
        found = session.execute(
            text("SELECT 1 FROM subjects WHERE id = :id AND deleted_at IS NULL"),
            {"id": subject_id},
        ).fetchone()
        assert found is not None, "Предмет не был найден до удаления"

        session.execute(
            text("UPDATE subjects SET deleted_at = NOW() WHERE id = :id"),
            {"id": subject_id},
        )
        session.commit()

        deleted = session.execute(
            text("SELECT deleted_at FROM subjects WHERE id = :id"), 
            {"id": subject_id}
        ).fetchone()

        assert deleted.deleted_at is not None
        print(f"✅ Предмет помечен как удалённый: {subject_name}")
    finally:
        cleanup_subject(subject_id)
