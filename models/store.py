from models.product import Product
from database import get_connection

class Store:
    # Менеджер магазина — управляет товарами и базой."
    def __init__(self, name):
        self.name = name
        print(f"🛒 Магазин «{self.name}» запущен.")

    def add_product(self, name, price, quantity, category):
        try:
            product = Product(name, price, quantity, category)
            product.save_to_db()
        except ValueError as e:
            print("❌ Ошибка:", e)


    def show_catalog(self):
        products = Product.get_all()
        if not products:
            print("📭 В магазине пока нет товаров.")
            return
        print("\n=== КАТАЛОГ ТОВАРОВ ===")
        for p in products:
            print(f"ID:{p[0]} | {p[1]} | Цена: {p[2]} | Кол-во: {p[3]} | Категория: {p[4]}")


    def sell_product(self, product_id, count):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT quantity, name, price FROM products WHERE id = ?", (product_id,))
        row = cur.fetchone()

        if not row:
            print("❌ Товар не найден.")
            conn.close()
            return
        qty, name, price = row

        if qty < count:
            print("⚠️ Недостаточно товара на складе.")
            conn.close()
            return

        new_qty = qty - count
        cur.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_qty, product_id))
        conn.commit()
        conn.close()

        total = price * count
        print(f"✅ Продано {count} шт. '{name}'. Сумма: {total:.2f} руб.")


    def total_inventory_value(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT SUM(price * quantity) FROM products")
        total = cur.fetchone()[0]
        conn.close()
        print(f"💰 Общая стоимость товаров: {total:.2f} руб.")


    def search_by_category(self, category):
        items = Product.find_by_category(category)
        if not items:
            print("📭 Нет товаров в этой категории.")
            return
        print(f"\n=== Категория: {category} ===")
        for item in items:
            print(f"ID:{item[0]} | {item[1]} | Цена:{item[2]} | Кол-во:{item[3]}")
