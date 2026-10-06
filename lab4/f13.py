from tabulate import tabulate

def run():
    data = [["Файл", "Статус"], ["f1-f15", "OK"]]
    print("13. tabulate:\n", tabulate(data, headers="firstrow"))