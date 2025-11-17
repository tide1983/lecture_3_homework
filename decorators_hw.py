import os
from datetime import datetime


# Задание 1: Базовый декоратор
def logger_v1(old_function):
    def new_function(*args, **kwargs):
        result = old_function(*args, **kwargs)
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        function_name = old_function.__name__
        
        args_str = ', '.join([str(arg) for arg in args])
        kwargs_str = ', '.join([f'{key}={value}' for key, value in kwargs.items()])
        all_args = ', '.join(filter(None, [args_str, kwargs_str]))
        
        with open('main.log', 'a', encoding='utf-8') as log_file:
            log_file.write(f'{timestamp} - {function_name}({all_args}) -> {result}\n')
        
        return result

    return new_function


# Задание 2: Параметризованный декоратор
def logger_v2(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            function_name = old_function.__name__
            
            args_str = ', '.join([str(arg) for arg in args])
            kwargs_str = ', '.join([f'{key}={value}' for key, value in kwargs.items()])
            all_args = ', '.join(filter(None, [args_str, kwargs_str]))
            
            with open(path, 'a', encoding='utf-8') as log_file:
                log_file.write(f'{timestamp} - {function_name}({all_args}) -> {result}\n')
            
            return result
        return new_function
    return __logger


def test_1():
    print("Запуск теста 1...")
    
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger_v1
    def hello_world():
        return 'Hello World'

    @logger_v1
    def summator(a, b=0):
        return a + b

    @logger_v1
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'
    
    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'
    
    print("Тест 1 пройден успешно!")


def test_2():
    print("Запуск теста 2...")
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger_v2(path)
        def hello_world():
            return 'Hello World'

        @logger_v2(path)
        def summator(a, b=0):
            return a + b

        @logger_v2(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:
        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'
    
    print("Тест 2 пройден успешно!")


# Задание 3: Пример применения к предыдущему ДЗ
@logger_v2('cookbook.log')
def read_cookbook(filename):
    """Функция для чтения кулинарной книги из файла"""
    cook_book = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            while True:
                dish_name = file.readline().strip()
                if not dish_name:
                    break
                
                ingredient_count = int(file.readline().strip())
                ingredients = []
                
                for _ in range(ingredient_count):
                    ingredient_line = file.readline().strip()
                    ingredient_info = ingredient_line.split(' | ')
                    ingredient = {
                        'ingredient_name': ingredient_info[0],
                        'quantity': int(ingredient_info[1]),
                        'measure': ingredient_info[2]
                    }
                    ingredients.append(ingredient)
                
                cook_book[dish_name] = ingredients
                file.readline()  # пропускаем пустую строку
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return {}
    
    return cook_book


@logger_v2('cookbook.log')
def calculate_ingredients(dishes, person_count, cook_book):
    """Функция для расчета необходимых ингредиентов"""
    shop_list = {}
    
    for dish in dishes:
        if dish in cook_book:
            for ingredient in cook_book[dish]:
                name = ingredient['ingredient_name']
                measure = ingredient['measure']
                quantity = ingredient['quantity'] * person_count
                
                if name in shop_list:
                    shop_list[name]['quantity'] += quantity
                else:
                    shop_list[name] = {'measure': measure, 'quantity': quantity}
    
    return shop_list


def test_3():
    print("Запуск теста 3 (пример применения)...")
    
    # Создаем тестовый файл с рецептами
    with open('test_recipes.txt', 'w', encoding='utf-8') as f:
        f.write("""Омлет
3
Яйцо | 2 | шт
Молоко | 100 | мл
Помидор | 1 | шт

Фахитос
4
Говядина | 200 | г
Перец | 1 | шт
Лаваш | 1 | шт
Сметана | 50 | г

""")
    
    # Тестируем наши функции с логгированием
    cookbook = read_cookbook('test_recipes.txt')
    print("Кулинарная книга:", cookbook)
    
    shopping_list = calculate_ingredients(['Омлет', 'Фахитос'], 2, cookbook)
    print("Список покупок на 2 персоны:", shopping_list)
    
    # Проверяем, что логи записались
    assert os.path.exists('cookbook.log'), 'файл cookbook.log должен существовать'
    
    with open('cookbook.log', 'r', encoding='utf-8') as log_file:
        log_content = log_file.read()
        assert 'read_cookbook' in log_content
        assert 'calculate_ingredients' in log_content
    
    print("Тест 3 пройден успешно!")


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
    print("\nВсе тесты пройдены успешно!")