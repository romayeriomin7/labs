def return_second_call(func):
    """Декоратор, який викликає функцію двічі, але повертає результат лише другого виклику."""

    def wrapper(*args, **kwargs):
        # 1. Перший виклик функції (результат ігнорується)
        func(*args, **kwargs)

        # 2. Другий виклик функції (результат зберігається та повертається)
        result = func(*args, **kwargs)
        return result

    return wrapper