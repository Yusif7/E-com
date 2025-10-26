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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            total_price REAL NOT NULL CHECK(total_price >= 0),
            order_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'cashier'))
            )
        """)

    conn.commit()
    conn.close()
