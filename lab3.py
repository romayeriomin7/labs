from typing import Dict, Tuple, List, Any
#лямбда функції

# 1. Форматування ціни у формат ххх.ххгрн
format_price = lambda price: f"{float(price):.2f}грн"

# 2. Розрахунок загальної вартості кошика
calculate_total = lambda cart_dict: sum(
    data['item']['price'] * data['qty'] for data in cart_dict.values()
)


#функції з анотаціями

def print_log(*args: Any, prefix: str = "[INFO]", **kwargs: Any) -> None:
    """
    Демонстрація *args та **kwargs.
    Приймає довільну кількість аргументів для виводу повідомлень.
    """
    print(f"{prefix}", *args, **kwargs)


def get_catalog() -> Dict[int, Dict[str, Any]]:
    """Повертає початковий словник товарів."""
    return {
        1: {"id": 1, "name": "Ноутбук", "price": 25000.0, "stock": 5},
        2: {"id": 2, "name": "Мишка бездротова", "price": 450.5, "stock": 12},
        3: {"id": 3, "name": "Клавіатура", "price": 1200.0, "stock": 8},
        4: {"id": 4, "name": "Навушники", "price": 890.99, "stock": 15},
        5: {"id": 5, "name": "Монітор 27\"", "price": 7500.0, "stock": 4},
    }


def show_catalog(catalog: Dict[int, Dict[str, Any]]) -> None:
    """Відображає доступні товари з використанням лямбда-фільтрації."""
    print_log("КАТАЛОГ ТОВАРІВ", prefix="\n===")

    # Лямбда для відбору товарів у наявності
    available = list(filter(lambda item: item['stock'] > 0, catalog.values()))

    if not available:
        print("На жаль, усі товари розпродані!")
        return

    for item in available:
        print(f"[{item['id']}] {item['name']} - {format_price(item['price'])} (Залишок: {item['stock']} шт.)")


def add_to_cart(catalog: Dict[int, Dict[str, Any]], cart: Dict[int, Dict[str, Any]]) -> None:
    """Додає товар у кошик."""
    show_catalog(catalog)
    try:
        item_id: int = int(input("\nВведіть ID товару: "))
        if item_id not in catalog:
            print_log("Товару з таким ID не існує.", prefix="❌")
            return

        item: Dict[str, Any] = catalog[item_id]
        if item['stock'] <= 0:
            print_log("Цього товару немає в наявності.", prefix="❌")
            return

        qty: int = int(input(f"Введіть кількість (доступно {item['stock']}): "))
        if qty <= 0:
            print_log("Кількість має бути більше 0.", prefix="❌")
            return

        current_in_cart: int = cart.get(item_id, {}).get('qty', 0)
        if current_in_cart + qty > item['stock']:
            print_log(f"Недостатньо на складі! У кошику вже є {current_in_cart} шт.", prefix="❌")
            return

        cart[item_id] = {
            "item": item,
            "qty": current_in_cart + qty
        }
        print_log(f"Додано {qty} шт. '{item['name']}' до кошика.", prefix="✅")

    except ValueError:
        print_log("Введіть коректне число!", prefix="❌")


def show_cart(cart: Dict[int, Dict[str, Any]]) -> bool:
    """Відображає вміст кошика та повертає True, якщо він не порожній."""
    print_log("ВАШ КОШИК", prefix="\n===")
    if not cart:
        print("Кошик порожній.")
        return False

    for item_id, data in cart.items():
        item = data['item']
        qty = data['qty']
        subtotal = item['price'] * qty
        print(f"[{item_id}] {item['name']} | {qty} шт. x {format_price(item['price'])} = {format_price(subtotal)}")

    total: float = calculate_total(cart)
    print("-" * 35)
    print(f"Загальна сума до сплати: {format_price(total)}")
    return True


def remove_from_cart(cart: Dict[int, Dict[str, Any]]) -> None:
    """Видаляє товар з кошика."""
    if not show_cart(cart):
        return

    try:
        item_id: int = int(input("\nВведіть ID товару для видалення: "))
        if item_id in cart:
            removed = cart.pop(item_id)
            print_log(f"Товар '{removed['item']['name']}' видалено з кошика.", prefix="✅")
        else:
            print_log("Цього товару немає у кошику.", prefix="❌")
    except ValueError:
        print_log("Введіть коректне число!", prefix="❌")


def checkout(catalog: Dict[int, Dict[str, Any]], cart: Dict[int, Dict[str, Any]]) -> None:
    """Списує товари зі складу та оформлює покупку."""
    if not cart:
        print_log("Кошик порожній. Немає чого купувати.", prefix="❌")
        return

    show_cart(cart)
    confirm: str = input("\nПідтвердити купівлю? (так/ні): ").strip().lower()

    if confirm in ['так', 'yes', 'y']:
        for item_id, data in cart.items():
            catalog[item_id]['stock'] -= data['qty']

        total: float = calculate_total(cart)
        cart.clear()
        print_log(f"Дякуємо за покупку! Оплачено: {format_price(total)}", prefix="🎉")
    else:
        print("Покупку скасовано.")


def admin_panel(catalog: Dict[int, Dict[str, Any]], admin_pass: str = "admin123") -> None:
    """Панель адміністратора для перегляду залишків."""
    entered_pass: str = input("\nВведіть пароль адміністратора: ")
    if entered_pass != admin_pass:
        print_log("Невірний пароль!", prefix="❌")
        return

    while True:
        print_log("ПАНЕЛЬ АДМІНІСТРАТОРА", prefix="\n===")
        print("1. Переглянути залишки товарів на складі")
        print("2. Змінити кількість товару")
        print("0. Вийти з панелі адміна")

        choice: str = input("Оберіть дію: ").strip()

        if choice == "1":
            print_log("ЗАЛИШКИ НА СКЛАДІ", prefix="\n---")
            # Використання лямбда-функції для сортування за залишком
            sorted_items = sorted(catalog.values(), key=lambda x: x['stock'])
            for item in sorted_items:
                status = "🔴 КРИТИЧНО" if item['stock'] < 3 else "🟢 OK"
                print(
                    f"ID: {item['id']:<2} | {item['name']:<20} | Ціна: {format_price(item['price']):<12} | Залишок: {item['stock']:<3} шт. [{status}]")

        elif choice == "2":
            try:
                item_id: int = int(input("Введіть ID товару: "))
                if item_id in catalog:
                    new_stock: int = int(input(f"Новий залишок для '{catalog[item_id]['name']}': "))
                    if new_stock >= 0:
                        catalog[item_id]['stock'] = new_stock
                        print_log("Залишок успішно оновлено.", prefix="✅")
                    else:
                        print_log("Залишок не може бути від'ємним.", prefix="❌")
                else:
                    print_log("Товар не знайдено.", prefix="❌")
            except ValueError:
                print_log("Введіть коректне число!", prefix="❌")

        elif choice == "0":
            print("Вихід з панелі адміністратора...")
            break
        else:
            print_log("Невірний вибір.", prefix="❌")


def run_app() -> None:
    """Головний цикл роботи магазину."""
    catalog: Dict[int, Dict[str, Any]] = get_catalog()
    cart: Dict[int, Dict[str, Any]] = {}

    while True:
        print("\n==========================")
        print("   ГОЛОВНЕ МЕНЮ МАГАЗИНУ  ")
        print("==========================")
        print("1. Переглянути каталог")
        print("2. Переглянути кошик")
        print("3. Додати товар у кошик")
        print("4. Видалити товар з кошика")
        print("5. Оформити покупку")
        print("9. Вхід для Адміністратора")
        print("0. Вихід з програми")

        choice: str = input("\nОберіть пункт меню: ").strip()

        if choice == "1":
            show_catalog(catalog)
        elif choice == "2":
            show_cart(cart)
        elif choice == "3":
            add_to_cart(catalog, cart)
        elif choice == "4":
            remove_from_cart(cart)
        elif choice == "5":
            checkout(catalog, cart)
        elif choice == "9":
            admin_panel(catalog)
        elif choice == "0":
            print_log("Дякуємо, що завітали! До побачення.", prefix="\n👋")
            break
        else:
            print_log("Невірний вибір, спробуйте ще раз.", prefix="❌")


#точка входу в програму
if __name__ == "__main__":
    run_app()