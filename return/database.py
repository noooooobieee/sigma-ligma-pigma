# database.py
# Модуль для работы с базой данных

import sqlite3
import config

def init_db():
    """Инициализация базы данных."""
    conn = sqlite3.connect(config.DATABASE_FILE)
    cursor = conn.cursor()

    # Создание таблицы для хранения данных запросов пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            request_text TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def save_request(user_id, request_text):
    """Сохранение запроса пользователя в базу данных."""
    conn = sqlite3.connect(config.DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_requests (user_id, request_text) VALUES (?, ?)",
        (user_id, request_text)
    )
    conn.commit()
    conn.close()

# Инициализация базы данных при первом запуске
if __name__ == "__main__":
    init_db()
