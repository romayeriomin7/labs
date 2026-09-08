print("Hello World")

name = "Roman" #str-порядок
age = 16 #int-ціле число
height = 1.78 #float-робове число
student = True #bool-true or false

numbers = [1, 2, 3] #list-список
coordinates = (10, 20) #tuple-незмінні
unique = {1, 2, 3}
person = { "name" : "Roman",  "age" : 16 }

print(name, type(name))
print(age, type(age))
print(height, type(height))
print(student, type(student))
print(numbers, type(numbers))
print(coordinates, type(coordinates))
print(unique, type(unique))
print(person, type(person))

a = 10
b = 3

print("Додавання (+):", a + b)
print("Віднімання (-):", a - b)
print("Множення (*):", a * b)
print("Ділення (/):", a / b)
print("Остача від ділення (%):", a % b)
print("Цілочисельне ділення (//):", a // b)
print("Піднесення до степеня (**):", a ** b)