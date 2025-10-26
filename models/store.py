from models.product import Product
from database import get_connection
from models.order import Order


class Store:
    # Менеджер магазина — управляет товарами и базой.
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
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT quantity, name, price FROM products WHERE id = ?", (product_id,))
            row = cur.fetchone()

            if not row:
                raise ValueError("❌ Товар не найден.")
            qty, name, price = row

            if qty < count:
                raise ValueError("⚠️ Недостаточно товара на складе.")

            # Расчёт
            total = price * count
            new_qty = qty - count

            # Обновляем остаток
            cur.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_qty, product_id))
            conn.commit()
            conn.close()

            # Создаём заказ
            order = Order(product_id, count, total)
            order.save_to_db()

            print(f"✅ Продано {count} шт. '{name}' на сумму {total:.2f} руб.")

        except ValueError as e:
            print(e)
        except Exception as e:
            print("🚨 Ошибка при продаже:", e)


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
