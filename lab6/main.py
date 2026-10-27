from decorators import return_second_call


# Застосовуємо наш декоратор до тестової функції
@return_second_call
def say_hello(name):
    print(f"  -> Виконання функції: Привіт, {name}!")
    return f"Успішно привітали {name}"


# Точка входу
if __name__ == '__main__':
    print("--- Запуск програми ---")

    # Викликаємо декоровану функцію
    res = say_hello("Роман")

    print(f"Отриманий результат у головній програмі: {res}")