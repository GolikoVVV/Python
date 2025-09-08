from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import DB_URL

# Создаём engine
engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

# Глобальная сессия (для простоты, в реальных проектах лучше использовать фикстуры)
session = SessionLocal()

def setup_tables():
    """Создаёт таблицы students и subjects, если их нет"""
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    deleted_at TIMESTAMP DEFAULT NULL
                );
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS subjects (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    deleted_at TIMESTAMP DEFAULT NULL
                );
            """))
    print("✅ Таблицы students и subjects созданы или уже существуют")

# Вызываем при импорте
setup_tables()