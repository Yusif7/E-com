import sqlite3

DB_NAME = "store.db"

def get_connection():
    # Создаёт подключение к базе SQLite.
    conn = sqlite3.connect(DB_NAME)
    return conn


def initialize_database():
    # Создаёт таблицу товаров, если её ещё нет.
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL CHECK(price >= 0),
            quantity INTEGER NOT NULL CHECK(quantity >= 0),
            category TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Таблица 'products' инициализирована.")
