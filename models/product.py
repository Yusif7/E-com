from database import get_connection

class Product:
    def __init__(self, name, price, quantity, category):
        if price < 0 or quantity < 0:
            raise ValueError("Цена и количество не могут быть отрицательными!")
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

    # Сохраняет товар в базу данных.
    def save_to_db(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, price, quantity, category) VALUES (?, ?, ?, ?)",
            (self.name, self.price, self.quantity, self.category)
        )
        conn.commit()
        conn.close()
        print(f"💾 Товар '{self.name}' добавлен в базу.")

    @staticmethod
    def get_all():
        # Возвращает список всех товаров из базы.
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, quantity, category FROM products")
        products = cursor.fetchall()
        conn.close()
        return products

    @staticmethod
    def delete_by_id(product_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()
        print(f"🗑️ Товар с ID {product_id} удалён.")

    @staticmethod
    def update_price(product_id, new_price):
        if new_price < 0:
            raise ValueError("Цена не может быть отрицательной.")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET price = ? WHERE id = ?", (new_price, product_id))
        conn.commit()
        conn.close()
        print(f"💰 Цена товара ID {product_id} обновлена на {new_price}.")

    @staticmethod
    def find_by_category(category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE category = ?", (category,))
        result = cursor.fetchall()
        conn.close()
        return result
