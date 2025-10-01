import sys
import os
from unittest.mock import MagicMock

from src.table.table import Table

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
    print("📊 ПОЛНОЕ ТЕСТИРОВАНИЕ ВСЕХ ФУНКЦИЙ")
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
    
    print("\n✅ ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ")

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
        print("🎯 ВЫБЕРИТЕ ТЕСТ ДЛЯ ВЫПОЛНЕНИЯ")
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
                print(f"✅ Тест '{test_name}' завершен успешно")
            except Exception as e:
                print(f"❌ Ошибка в тесте '{test_name}': {e}")
        else:
            print("❌ Неверный выбор. Попробуйте снова.")

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


def test_insert_success():
    test_data = {"id": 1, "name": "Alice", "age": 30}
    table_structure = {"id": int, "name": str, "age": int}
    Table(name="test").storage.get_metadata = MagicMock(return_value=table_structure)
    result = Table(name="test").insert(values=test_data)
    assert result == {"success": True}


def test_insert_failed():
    test_data = {"id": 1, "name": "Alice", "age": "thirty"}
    table_structure = {"id": int, "name": str, "age": int}
    Table(name="test").storage.get_metadata = MagicMock(return_value=table_structure)
    result = Table(name="test").insert(values=test_data)
    assert result == {"success": False}


def test_select():
    test_data = ({"id": 1, "username": "Bob", "age": 24}, {"id": 2, "username": "Alice", "age": 14},
                 {"id": 3, "username": "Mark", "age": 1}, {"id": 4, "username": "Li", "age": 0},)
    Table(name="test").storage.get_from_data_file = MagicMock(return_value=test_data)
    test_columns = ["username"]
    test_conditions = {
        "username": {
            "type": str,
            "min_length": 2,
            "max_length": 20,
        },
        "age": {
            "type": int,
            "gt": 2,
            "lt": 120
        }
    }
    result = Table(name="test").select(columns=test_columns, conditions=test_conditions)
    assert result == [{"id": 2, "username": "Alice", "age": 14}]


def test_update():
    table_structure = {"id": int, "username": str, "age": int}
    Table(name="test").storage.get_metadata = MagicMock(return_value=table_structure)
    test_full_data = ({"id": 1, "username": "Tima", "age": 13}, {"id": 2, "username": "Robert", "age": 43},)
    Table(name="test").storage.get_from_data_file = MagicMock(return_value=test_full_data)
    new_data = {"username": "Franklin", "age": 25}
    test_conditions = {"username": "Robert"}
    result = Table(name="test").update(new_data=new_data, conditions=test_conditions)
    assert result == 1


def test_delete():
    test_full_data = ({"id": 1, "username": "Tima", "age": 13}, {"id": 2, "username": "Robert", "age": 43},)
    Table(name="test").storage.get_from_data_file = MagicMock(return_value=test_full_data)
    test_conditions = {"username": "Tima"}
    result = Table(name="test").delete(conditions=test_conditions)
    assert result == 1


if __name__ == "__main__":
    main()