from database import initialize_database
from models.store import Store

def main():
    initialize_database()
    shop = Store("TechMarket")

    while True:
        print("\n=== МЕНЮ МАГАЗИНА ===")
        print("1. Добавить товар")
        print("2. Показать каталог")
        print("3. Купить товар")
        print("4. Стоимость склада")
        print("5. Поиск по категории")
        print("0. Выйти")
        choice = input("Выбор: ")

        if choice == "1":
            n = input("Название: ")
            p = float(input("Цена: "))
            q = int(input("Количество: "))
            c = input("Категория: ")
            shop.add_product(n, p, q, c)

        elif choice == "2":
            shop.show_catalog()

        elif choice == "3":
            pid = int(input("ID товара: "))
            cnt = int(input("Количество для покупки: "))
            shop.sell_product(pid, cnt)

        elif choice == "4":
            shop.total_inventory_value()

        elif choice == "5":
            cat = input("Категория: ")
            shop.search_by_category(cat)

        elif choice == "0":
            print("👋 Выход.")
            break
        else:
            print("❌ Неверный выбор.")

if __name__ == "__main__":
    main()
