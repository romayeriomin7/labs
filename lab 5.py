import random

MAX_POTION_SLOTS = 10
MAX_POTION_STACK = 10

MAX_INGREDIENT_SLOTS = 25
MAX_INGREDIENT_STACK = 25


# ==================== 1. ПУЛИ ІНГРЕДІЄНТІВ ТА ЗІЛЬ ====================

def create_ingredients_pool():
    """Створює пул із 200 різних інгредієнтів."""
    try:
        bases = [
            "Корінь", "Лист", "Пил", "Сльоза", "Кристал",
            "Мох", "Пелюстка", "Смола", "Іскра", "Роса"
        ]
        modifiers = [
            "Місячний", "Сонячний", "Тіньовий", "Лісовий", "Гірський",
            "Крижаний", "Вогняний", "Штормовий", "Древній", "Дикий",
            "Срібний", "Золотий", "Туманний", "Болотний", "Зоряний",
            "Грозовий", "Сутінковий", "Квітковий", "Скляний", "Морський"
        ]

        pool = []
        for mod in modifiers:
            for base in bases:
                pool.append(f"{mod} {base}")

        if len(pool) < 200:
            raise ValueError("Недостатньо інгредієнтів у пулі!")

        return pool[:200]
    except Exception as error:
        print(f"[Помилка створення пулу інгредієнтів]: {error}")
        return ["Базова трава", "Чиста вода"]


def create_potions_pool(ingredients):
    """Створює пул із 50 зіль, кожне потребує 2 інгредієнти."""
    try:
        effects = [
            "Зцілення", "Мани", "Сили", "Швидкості", "Невидимості",
            "Захисту", "Вогню", "Морозу", "Яснобачення", "Удачі"
        ]
        tiers = [
            "Слабке зілля", "Звичайне зілля", "Міцне зілля",
            "Велике зілля", "Еліксир"
        ]

        potions = {}
        idx = 0
        for tier in tiers:
            for effect in effects:
                if idx >= 50:
                    break
                potion_name = f"{tier} {effect.lower()}"
                ing1 = ingredients[(idx * 2) % len(ingredients)]
                ing2 = ingredients[(idx * 2 + 1) % len(ingredients)]
                price = 20 + idx * 5
                potions[potion_name] = {
                    "ingredients": [ing1, ing2],
                    "price": price
                }
                idx += 1

        if len(potions) < 50:
            raise ValueError("Недостатньо зіль у пулі!")

        return potions
    except Exception as error:
        print(f"[Помилка створення пулу зіль]: {error}")
        return {
            "Слабке зілля зцілення": {
                "ingredients": [ingredients[0], ingredients[1]],
                "price": 25
            }
        }


# ==================== 2. РОБОТА З ІНВЕНТАРЕМ ====================

def add_ingredient(ing_slots, ingredient_name, amount=1):
    """Додає інгредієнти у слоти (стак до 25, всього до 25 слотів)."""
    try:
        if amount <= 0:
            return False

        remaining = amount

        for slot in ing_slots:
            if slot["name"] == ingredient_name and slot["count"] < MAX_INGREDIENT_STACK:
                free_space = MAX_INGREDIENT_STACK - slot["count"]
                to_add = min(free_space, remaining)
                slot["count"] += to_add
                remaining -= to_add
                if remaining == 0:
                    return True

        while remaining > 0:
            if len(ing_slots) >= MAX_INGREDIENT_SLOTS:
                print(f"[Інвентар інгредієнтів повний] Не вдалося помістити: {ingredient_name} (x{remaining})")
                return False

            to_add = min(MAX_INGREDIENT_STACK, remaining)
            ing_slots.append({"name": ingredient_name, "count": to_add})
            remaining -= to_add

        return True
    except Exception as error:
        print(f"[Помилка додавання інгредієнта]: {error}")
        return False


def remove_ingredient(ing_slots, ingredient_name, amount=1):
    """Списує інгредієнти з інвентаря. Повертає True, якщо вистачило."""
    try:
        total = sum(s["count"] for s in ing_slots if s["name"] == ingredient_name)
        if total < amount:
            return False

        needed = amount
        for slot in ing_slots:
            if slot["name"] == ingredient_name:
                if slot["count"] >= needed:
                    slot["count"] -= needed
                    needed = 0
                    break
                else:
                    needed -= slot["count"]
                    slot["count"] = 0

        ing_slots[:] = [s for s in ing_slots if s["count"] > 0]
        return True
    except Exception as error:
        print(f"[Помилка списання інгредієнта]: {error}")
        return False


def add_potion(potion_slots, potion_name, amount=1):
    """Додає зілля у слоти (стак до 10, всього до 10 слотів)."""
    try:
        if amount <= 0:
            return False

        remaining = amount

        for slot in potion_slots:
            if slot["name"] == potion_name and slot["count"] < MAX_POTION_STACK:
                free_space = MAX_POTION_STACK - slot["count"]
                to_add = min(free_space, remaining)
                slot["count"] += to_add
                remaining -= to_add
                if remaining == 0:
                    return True

        while remaining > 0:
            if len(potion_slots) >= MAX_POTION_SLOTS:
                print(f"[Інвентар зіль повний] Не вдалося помістити: {potion_name} (x{remaining})")
                return False

            to_add = min(MAX_POTION_STACK, remaining)
            potion_slots.append({"name": potion_name, "count": to_add})
            remaining -= to_add

        return True
    except Exception as error:
        print(f"[Помилка додавання зілля]: {error}")
        return False


def show_inventory(ing_slots, potion_slots, gold, target_gold, day, max_days):
    """Виводить поточний стан гравця та обох інвентарів."""
    try:
        print("\n" + "=" * 50)
        print(f"ДЕНЬ {day}/{max_days} | ЗОЛОТО: {gold}/{target_gold}")
        print("-" * 50)
        print(f"ІНГРЕДІЄНТИ (Слотів: {len(ing_slots)}/{MAX_INGREDIENT_SLOTS}, стак до {MAX_INGREDIENT_STACK}):")
        if not ing_slots:
            print("  [Порожньо]")
        else:
            for i, slot in enumerate(ing_slots, 1):
                print(f"  {i}. {slot['name']} — {slot['count']}/{MAX_INGREDIENT_STACK}")

        print("-" * 50)
        print(f"ЗІЛЛЯ (Слотів: {len(potion_slots)}/{MAX_POTION_SLOTS}, стак до {MAX_POTION_STACK}):")
        if not potion_slots:
            print("  [Порожньо]")
        else:
            for i, slot in enumerate(potion_slots, 1):
                print(f"  {i}. {slot['name']} — {slot['count']}/{MAX_POTION_STACK}")
        print("=" * 50)
    except Exception as error:
        print(f"[Помилка виводу інвентаря]: {error}")


# ==================== 3. ІГРОВА ЛОГІКА ====================

def grant_daily_ingredients(ing_slots, ingredients_pool, potions_pool):
    """Видає 5 інгредієнтів на початку нового ігрового дня."""
    try:
        print("\n[Новий день] Гільдія видає вам 5 інгредієнтів:")
        recipe_ingredients = []
        for data in potions_pool.values():
            recipe_ingredients.extend(data["ingredients"])

        for num in range(1, 6):
            if num <= 3 and recipe_ingredients:
                chosen = random.choice(recipe_ingredients)
            else:
                chosen = random.choice(ingredients_pool)

            added = add_ingredient(ing_slots, chosen, 1)
            status = "додано" if added else "не влізло (немає слотів)"
            print(f"  {num}) {chosen} -> {status}")
    except Exception as error:
        print(f"[Помилка видачі щоденних інгредієнтів]: {error}")


def craft_potion(ing_slots, potion_slots, potions_pool):
    """Дозволяє обрати зілля з пулу (50 видів) та зварити його."""
    try:
        potion_names = list(potions_pool.keys())
        print("\nДоступні рецепти (перші 15 для зручності, або введіть номер 1..50):")
        for idx in range(1, 16):
            name = potion_names[idx - 1]
            req = potions_pool[name]["ingredients"]
            price = potions_pool[name]["price"]
            print(f"  {idx}. {name} [{req[0]} + {req[1]}] -> ціна {price} зол.")

        raw_choice = input("Введіть номер зілля (1-50) або 0 для виходу: ").strip()
        choice = int(raw_choice)

        if choice == 0:
            return
        if choice < 1 or choice > len(potion_names):
            print("[Увага] Невірний номер рецепта.")
            return

        selected_potion = potion_names[choice - 1]
        req_ings = potions_pool[selected_potion]["ingredients"]

        counts = {}
        for ing in req_ings:
            counts[ing] = sum(s["count"] for s in ing_slots if s["name"] == ing)

        if req_ings[0] == req_ings[1]:
            if counts[req_ings[0]] < 2:
                print(f"[Не вистачає інгредієнтів] Потрібно 2x {req_ings[0]}.")
                return
        else:
            if counts[req_ings[0]] < 1 or counts[req_ings[1]] < 1:
                print(f"[Не вистачає інгредієнтів] Потрібно: {req_ings[0]} та {req_ings[1]}.")
                return

        has_free_slot = len(potion_slots) < MAX_POTION_SLOTS or any(
            s["name"] == selected_potion and s["count"] < MAX_POTION_STACK for s in potion_slots
        )
        if not has_free_slot:
            print("[Немає місця] Інвентар зіль повний (максимум 10 слотів).")
            return

        for ing in req_ings:
            remove_ingredient(ing_slots, ing, 1)

        if add_potion(potion_slots, selected_potion, 1):
            print(f"[Успіх] Зварено: {selected_potion}!")
    except ValueError:
        print("[Помилка вводу] Потрібно ввести ціле число.")
    except Exception as error:
        print(f"[Помилка під час варіння зілля]: {error}")


def sell_potions_end_of_day(potion_slots, potions_pool, gold):
    """Продаж зіль у кінці дня. Повертає оновлене золото."""
    try:
        if not potion_slots:
            print("\n[Кінець дня] У вас немає зіль для продажу.")
            return gold

        print("\n[Кінець дня] Торговець готовий купити ваші зілля:")
        for i, slot in enumerate(potion_slots, 1):
            unit_price = potions_pool.get(slot["name"], {}).get("price", 20)
            print(f"  {i}. {slot['name']} (x{slot['count']}) — {unit_price} зол./шт.")

        print("  A. Продати ВСІ зілля")
        print("  0. Нічого не продавати (залишити до наступного дня)")

        choice = input("Ваш вибір: ").strip().upper()

        if choice == "0":
            print("Ви залишили зілля в інвентарі.")
            return gold

        if choice == "A":
            earned = 0
            for slot in potion_slots:
                unit_price = potions_pool.get(slot["name"], {}).get("price", 20)
                earned += unit_price * slot["count"]
            potion_slots.clear()
            gold += earned
            print(f"[Продано] Ви заробили {earned} золота! Всього золота: {gold}.")
            return gold

        idx = int(choice)
        if idx < 1 or idx > len(potion_slots):
            print("[Увага] Невірний номер слота.")
            return gold

        slot = potion_slots[idx - 1]
        unit_price = potions_pool.get(slot["name"], {}).get("price", 20)
        qty_str = input(f"Скільки продати (1-{slot['count']})? ").strip()
        qty = int(qty_str)

        if qty < 1 or qty > slot["count"]:
            print("[Увага] Некоректна кількість.")
            return gold

        earned = unit_price * qty
        slot["count"] -= qty
        if slot["count"] == 0:
            potion_slots.pop(idx - 1)

        gold += earned
        print(f"[Продано] Отримано {earned} золота! Всього золота: {gold}.")
        return gold
    except ValueError:
        print("[Помилка вводу] Введіть коректне число або 'A'.")
        return gold
    except Exception as error:
        print(f"[Помилка під час продажу]: {error}")
        return gold


def check_game_ending(gold, target_gold, day, max_days):
    """Перевіряє умови виграшу або програшу. Повертає 'WIN', 'LOSE' або None."""
    try:
        if gold >= target_gold:
            return "WIN"
        if day >= max_days:
            return "LOSE"
        return None
    except Exception as error:
        print(f"[Помилка перевірки кінцівки]: {error}")
        return None


# ==================== 4. ТОЧКА ВХОДУ ====================

def main():
    """Головна точка входу в RPG-гру Алхіміка."""
    try:
        max_days = 5
        target_gold = 150
        gold = 0

        ing_slots = []
        potion_slots = []

        ingredients_pool = create_ingredients_pool()
        potions_pool = create_potions_pool(ingredients_pool)

        print("=== RPG АЛХІМІК ===")
        print(f"Мета: зібрати {target_gold} золота за {max_days} днів, щоб викупити майстерню.")
        print(f"Завантажено: {len(ingredients_pool)} інгредієнтів та {len(potions_pool)} зіль.")

        for day in range(1, max_days + 1):
            grant_daily_ingredients(ing_slots, ingredients_pool, potions_pool)

            while True:
                show_inventory(ing_slots, potion_slots, gold, target_gold, day, max_days)
                print("Дії протягом дня:")
                print("  1. Зварити зілля")
                print("  2. Завершити день і перейти до продажу зіль")

                action = input("Оберіть дію (1/2): ").strip()
                if action == "1":
                    craft_potion(ing_slots, potion_slots, potions_pool)
                elif action == "2":
                    break
                else:
                    print("[Увага] Оберіть 1 або 2.")

            gold = sell_potions_end_of_day(potion_slots, potions_pool, gold)

            ending = check_game_ending(gold, target_gold, day, max_days)
            if ending == "WIN":
                print("\n🎉 ПЕРЕМОГА! Ви зібрали потрібну суму золота та стали майстром Гільдії!")
                break
            elif ending == "LOSE":
                print(f"\n💀 ПОРАЗКА! {max_days} днів минуло, а ви зібрали лише {gold} із {target_gold} золота.")
                break

    except KeyboardInterrupt:
        print("\n[Гру перервано користувачем]")
    except Exception as error:
        print(f"[Критична помилка гри]: {error}")


if __name__ == "__main__":
    main()
