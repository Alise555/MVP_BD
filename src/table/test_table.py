import sys
import os

from table.table import Table

def test_basic_functionality(table):
    """Тестирование базового функционала"""
    print("\n=== ТЕСТ БАЗОВОГО ФУНКЦИОНАЛА ===")
    print(f"Имя таблицы: {table.get_name()}")
    print(f"Размер таблицы: {table.get_size()}")
    print(f"Таблица пуста: {table.is_empty()}")

def test_add_column(table):
    """Тестирование добавления колонок"""
    print("\n=== ТЕСТ ДОБАВЛЕНИЯ КОЛОНОК ===")
    table.add_column("id", "int")
    table.add_column("name", "str")
    table.add_column("age", "int")
    print("Колонки добавлены")

def test_modify_column(table):
    """Тестирование изменения колонок"""
    print("\n=== ТЕСТ ИЗМЕНЕНИЯ КОЛОНОК ===")
    table.modify_column("name", "full_name", "varchar(100)")
    print("Колонка изменена")

def test_drop_column(table):
    """Тестирование удаления колонок"""
    print("\n=== ТЕСТ УДАЛЕНИЯ КОЛОНОК ===")
    table.drop_column("age")
    print("Колонка удалена")

def test_insert_data(table):
    """Тестирование вставки данных"""
    print("\n=== ТЕСТ ВСТАВКИ ДАННЫХ ===")
    table.insert({"id": 1, "name": "Alice", "age": 25})
    table.insert({"id": 2, "name": "Bob", "age": 30})
    table.insert({"id": 3, "name": "Charlie", "age": 35})
    print("Данные вставлены")

def test_select_data(table):
    """Тестирование выборки данных"""
    print("\n=== ТЕСТ ВЫБОРКИ ДАННЫХ ===")
    # Выборка всех колонок
    result1 = table.select()
    print(f"Все данные: {result1}")
    
    # Выборка конкретных колонок
    result2 = table.select(columns=["id", "name"])
    print(f"Только id и name: {result2}")
    
    # Выборка с условиями
    result3 = table.select(conditions={"name": "Alice"})
    print(f"Где name='Alice': {result3}")

def test_update_data(table):
    """Тестирование обновления данных"""
    print("\n=== ТЕСТ ОБНОВЛЕНИЯ ДАННЫХ ===")
    updated = table.update({"age": 26}, {"name": "Alice"})
    print(f"Обновлено записей: {updated}")

def test_delete_data(table):
    """Тестирование удаления данных"""
    print("\n=== ТЕСТ УДАЛЕНИЯ ДАННЫХ ===")
    deleted = table.delete({"name": "Bob"})
    print(f"Удалено записей: {deleted}")

def test_all_functions():
    """Тестирование всех функций последовательно"""
    print("\n" + "="*50)
    print(" ПОЛНОЕ ТЕСТИРОВАНИЕ ВСЕХ ФУНКЦИЙ")
    print("="*50)
    
    table = Table("users")
    
    test_basic_functionality(table)
    test_add_column(table)
    test_insert_data(table)
    test_select_data(table)
    test_modify_column(table)
    test_update_data(table)
    test_delete_data(table)
    test_drop_column(table)
    
    print("\n ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ")

def interactive_test():
    """Интерактивный выбор тестов"""
    table = Table("users")
    
    tests = {
        "1": ("Базовый функционал", test_basic_functionality),
        "2": ("Добавление колонок", test_add_column),
        "3": ("Изменение колонок", test_modify_column),
        "4": ("Удаление колонок", test_drop_column),
        "5": ("Вставка данных", test_insert_data),
        "6": ("Выборка данных", test_select_data),
        "7": ("Обновление данных", test_update_data),
        "8": ("Удаление данных", test_delete_data),
        "9": ("ВСЕ ТЕСТЫ", test_all_functions)
    }
    
    while True:
        print("\n" + "="*40)
        print(" ВЫБЕРИТЕ ТЕСТ ДЛЯ ВЫПОЛНЕНИЯ")
        print("="*40)
        
        for key, (name, _) in tests.items():
            print(f"{key}. {name}")
        print("0. Выход")
        
        choice = input("\nВаш выбор (0-9): ").strip()
        
        if choice == "0":
            print("Выход из тестирования")
            break
        elif choice in tests:
            test_name, test_func = tests[choice]
            print(f"\n🚀 Запуск теста: {test_name}")
            try:
                if choice == "9":
                    test_func()  # Для полного теста не передаем table
                else:
                    test_func(table)
                print(f" Тест '{test_name}' завершен успешно")
            except Exception as e:
                print(f" Ошибка в тесте '{test_name}': {e}")
        else:
            print(" Неверный выбор. Попробуйте снова.")

def main():
    """Основная функция"""
    print("🔧 ТЕСТИРОВАНИЕ КЛАССА TABLE")
    print("Выберите режим тестирования:")
    print("1. Интерактивный выбор тестов")
    print("2. Полное тестирование всех функций")
    
    choice = input("Ваш выбор (1-2): ").strip()
    
    if choice == "1":
        interactive_test()
    elif choice == "2":
        test_all_functions()
    else:
        print("Неверный выбор. Запуск интерактивного режима.")
        interactive_test()

if __name__ == "__main__":
    main()