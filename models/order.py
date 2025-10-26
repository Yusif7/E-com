from database import get_connection

class Order:
    # Класс описывает покупку товара.
    def __init__(self, product_id, quantity, total_price):
        self.product_id = product_id
        self.quantity = quantity
        self.total_price = total_price

    def save_to_db(self):
        """Сохраняет заказ в базу данных."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO orders (product_id, quantity, total_price) VALUES (?, ?, ?)",
            (self.product_id, self.quantity, self.total_price)
        )
        conn.commit()
        conn.close()
        print(f"💾 Заказ сохранён: товар #{self.product_id}, кол-во {self.quantity}, сумма {self.total_price}")

    @staticmethod
    def get_all():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT o.id, p.name, o.quantity, o.total_price, o.order_date
            FROM orders o
            JOIN products p ON o.product_id = p.id
            ORDER BY o.order_date DESC
        """)
        rows = cur.fetchall()
        conn.close()
        return rows

    @staticmethod
    def total_revenue():
        # Возвращает общую сумму продаж.
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT SUM(total_price) FROM orders")
        total = cur.fetchone()[0] or 0
        conn.close()
        return total
