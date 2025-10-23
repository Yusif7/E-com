from database import initialize_database
from models.product import Product

def main():
    initialize_database()

    while True:
        print("\n=== МЕНЮ МАГАЗИНА ===")
        print("1. Добавить товар")
        print("2. Показать все товары")
        print("3. Удалить товар")
        print("4. Обновить цену")
        print("5. Найти по категории")
        print("0. Выйти")

        choice = input("Выбор: ")

        if choice == "1":
            name = input("Название: ")
            price = float(input("Цена: "))
            quantity = int(input("Количество: "))
            category = input("Категория: ")
            product = Product(name, price, quantity, category)
            product.save_to_db()

        elif choice == "2":
            for p in Product.get_all():
                print(p)

        elif choice == "3":
            pid = int(input("Введите ID товара для удаления: "))
            Product.delete_by_id(pid)

        elif choice == "4":
            pid = int(input("ID товара: "))
            new_price = float(input("Новая цена: "))
            Product.update_price(pid, new_price)

        elif choice == "5":
            cat = input("Введите категорию: ")
            for p in Product.find_by_category(cat):
                print(p)

        elif choice == "0":
            print("👋 Выход...")
            break

        else:
            print("❌ Неверный выбор.")

if __name__ == "__main__":
    main()
