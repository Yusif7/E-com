from database import initialize_database,get_connection
from models.store import Store
from models.order import Order
from models.user import User, Admin, Cashier

def main():
    initialize_database()

    print("\n=== АВТОРИЗАЦИЯ ===")
    username = input("Логин: ")
    password = input("Пароль: ")

    user = User.login(username, password)
    if not user:
        print("🚫 Вход не выполнен.")
        return

    shop = Store("TechMarket")

    while True:
        print(f"\n=== МЕНЮ ({user.role.upper()}) ===")

        if user.can("add_product"):
            print("1. Добавить товар")
        if user.can("show_products"):
            print("2. Показать каталог")
        if user.can("sell_product"):
            print("3. Продать товар")
        if user.can("quantity_cost"):
            print("4. Стоимость склада")
        if user.can("category_filter"):
            print("5. Поиск по категории")
        if user.can("view_orders"):
            print("6. История заказов")
        if user.can("create_user"):
            print("7. Создание пользователя")
        print("0. Выход")


        choice = input("Выбор: ")

        if choice == "1" and user.can("add_product"):
            n = input("Название: ")
            p = float(input("Цена: "))
            q = int(input("Количество: "))
            c = input("Категория: ")
            shop.add_product(n, p, q, c)

        elif choice == "2":
            shop.show_catalog()

        elif choice == "3" and user.can("sell_product"):
            shop.show_catalog()
            pid = int(input("ID товара: "))
            cnt = int(input("Количество для покупки: "))
            shop.sell_product(pid, cnt)

        elif choice == "4" and user.can("quantity_cost"):
            shop.total_inventory_value()

        elif choice == "5" and user.can("category_filter"):
            cat = input("Категория: ")
            shop.search_by_category(cat)

        elif choice == "6" and user.can("view_orders"):
            orders = Order.get_all()
            if not orders:
                print("📭 Заказов пока нет.")
            else:
                print("\n=== ИСТОРИЯ ЗАКАЗОВ ===")
                for o in orders:
                    print(f"#{o[0]} | {o[1]} | {o[2]} шт | {o[3]:.2f} руб | {o[4]}")
                print(f"\n💰 Общая выручка: {Order.total_revenue():.2f} руб.")

        elif choice == "7" and user.can("create_user"):
            uname = input("Имя нового пользователя: ")
            pwd = input("Пароль: ")
            role = input("Роль (admin/cashier): ")
            u = User(uname, pwd, role)
            u.save_to_db()

        elif choice == "0":
            print("👋 Выход.")
            break
        else:
            print("❌ Неверный выбор.")

if __name__ == "__main__":
    main()
