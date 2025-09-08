# Настройки подключения к базе данных
DB_CONFIG = {
    "driver": "postgresql",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": "5432",
    "database": "QAMyFirstBase"
}
# Полный URL для SQLAlchemy
DB_URL = "{driver}://{user}:{password}@{host}:{port}/{database}".format(**DB_CONFIG)