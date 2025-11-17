import os
from datetime import datetime

def logger(path):
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

@logger('cookbook.log')
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

@logger('cookbook.log')
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
    test_3()