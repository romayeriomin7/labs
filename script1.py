
users = {
    "vasyl": {"password": "123", "grades": [10, 11, 4, 12, 5]},
    "nazar": {"password": "456", "grades": [3, 2, 4, 5, 8]},
    "petro": {"password": "789", "grades": [6, 7, 8, 9, 10]},
    "olga": {"password": "000", "grades": [2, 12, 4, 9, 5]}
}

login = input("Введіть логін: ")
password = input("Введіть пароль: ")

if login in users and users[login]["password"] == password:
    print("Вхід успішний!")

    user_grades = users[login]["grades"]
    print("Ваші оцінки:", user_grades)

    good_count = 0  # для оцінок від 5 до 12
    bad_count = 0  # для оцінок від 1 до 4

    for grade in user_grades:
        if grade >= 5 and grade <= 12:
            good_count = good_count + 1
        elif grade >= 1 and grade <= 4:
            bad_count = bad_count + 1

    # Виводим результат
    print("Кількість задовільних оцінок (5-12):", good_count)
    print("Кількість незадовільних оцінок (1-4):", bad_count)

else:
    print("Невірний логін або пароль!")
