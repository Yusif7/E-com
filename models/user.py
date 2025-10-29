import hashlib
from database import get_connection

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = self._hash(password)
        self.role = role

    """
    text.encode(): Преобразует входную строку text в байтовую последовательность
    hashlib.sha256(...): Использует алгоритм SHA-256 из библиотеки hashlib,SHA-256 — это криптографический алгоритм, который генерирует уникальную строку
    .hexdigest(): Возвращает хэш в виде строки из 64 шестнадцатеричных символов (0–9, a–f).
    """
    def _hash(self, text):
        return hashlib.sha256(text.encode()).hexdigest()

    def save_to_db(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (self.username, self.password, self.role)
        )
        conn.commit()
        conn.close()
        print(f"👤 Пользователь {self.username} ({self.role}) создан.")

    @staticmethod
    def login(username, password):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username, password, role FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        conn.close()

        if not row:
            print("❌ Пользователь не найден.")
            return None

        stored_hash = row[2]
        role = row[3]
        if hashlib.sha256(password.encode()).hexdigest() == stored_hash:
            if role == "admin":
                return Admin(username, password)
            elif role == "cashier":
                return Cashier(username, password)
        else:
            print("❌ Неверный пароль.")
            return None

    def can(self, action):
        # Проверка прав доступа по действию.
        return action in self.get_permissions()


class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, "admin")

    def get_permissions(self):
        return ["add_product", "show_products", "sell_product", "quantity_cost", "category_filter", "view_orders", "create_user", "update_product_info"]

class Cashier(User):
    def __init__(self, username, password):
        super().__init__(username, password, "cashier")

    def get_permissions(self):
        return ["show_products", "sell_product", "quantity_cost", "category_filter", "view_orders"]

