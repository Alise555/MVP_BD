import pytest
from table.table import Table
from unittest.mock import MagicMock


@pytest.fixture
def mock_data():
    return ({"id": 1, "username": "Bob", "age": 24}, {"id": 2, "username": "Alice", "age": 14},
            {"id": 3, "username": "Mark", "age": 1}, {"id": 4, "username": "Li", "age": 0},)


@pytest.mark.parametrize(
        "test_data, table_struct, exp_result",
        [
            ({"id": 1, "name": "Alice", "age": 30}, {"id": int, "name": str, "age": int}, {"success": True}),
            ({"id": 1, "name": "Alice", "age": "thirty"}, {"id": int, "name": str, "age": int}, {"success": False})
        ]
)
def test_insert(test_data, table_struct, exp_result):
    table = Table(name="test")
    table.storage.get_metadata = MagicMock(return_value=table_struct)
    table.storage.insert_in_data_file = MagicMock()
    result = table.insert(values=test_data)
    assert result == exp_result


@pytest.mark.parametrize(
        "test_columns, test_conditions, data, exp_result",
        [
            # 1. Базовый тест: проверка строки на длину и тип
            (
                ["username"],
                {
                    "username": {
                        "type": str,
                        "min_length": 4,
                        "max_length": 10,
                    }
                },
                (
                    {"username": "Bob", "age": 12},       # не проходит (длина < 4)
                    {"username": "Alice", "age": 24},     # проходит
                    {"username": "VeryLongUsername", "age": 7},  # не проходит (длина > 10)
                    {"username": 123, "age": 0},         # не проходит (не строка)
                ),
                [{"username": "Alice"}]
            ),

            # 2. Проверка числовых ограничений (gt/lt)
            (
                ["age"],
                {
                    "age": {
                        "type": int,
                        "gt": 18,
                        "lt": 60
                    }
                },
                (
                    {"age": 17},   # не проходит (≤ 18)
                    {"age": 25},   # проходит
                    {"age": 60},   # не проходит (≥ 60)
                    {"age": "25"},  # не проходит (не int)
                ),
                [{"age": 25}]
            ),

            # 3. Комбинированная проверка (строка + число)
            (
                ["username", "age"],
                {
                    "username": {
                        "type": str,
                        "min_length": 2,
                    },
                    "age": {
                        "type": int,
                        "gt": 0,
                        "lt": 120
                    }
                },
                (
                    {"username": "A", "age": 20},      # не проходит (username слишком короткий)
                    {"username": "Bob", "age": -5},    # не проходит (age ≤ 0)
                    {"username": "Alice", "age": 150},  # не проходит (age ≥ 120)
                    {"username": "Bob", "age": 25},    # проходит
                ),
                [{"username": "Bob", "age": 25}]
            ),

            # 4. Пустые условия (должны вернуть все записи для запрошенных колонок)
            (
                ["username", "age"],
                {},
                (
                    {"username": "Bob", "age": 25},
                    {"username": "Alice", "age": 30},
                ),
                [
                    {"username": "Bob", "age": 25},
                    {"username": "Alice", "age": 30},
                ]
            ),

            # 5. Условия для несуществующих колонок
            (
                ["username"],
                {
                    "nonexistent_column": {
                        "type": str,
                        "min_length": 2,
                    },
                    "username": {
                        "type": str,
                        "min_length": 3,
                    }
                },
                (
                    {"username": "Bo"}, 
                    {"username": "Bob"},
                ),
                []
            ),

            # 6. Проверка на точное совпадение (не словарь правил)
            (
                ["status"],
                {"status": "active"},
                (
                    {"status": "active"},   # проходит
                    {"status": "inactive"},  # не проходит
                ),
                [{"status": "active"}]
            ),

            # 7. Пустой результат (ни одна запись не подходит)
            (
                ["username"],
                {
                    "username": {
                        "type": str,
                        "min_length": 10,
                    }
                },
                (
                    {"username": "Bob"},
                    {"username": "Alice"},
                ),
                []
            ),

            # 8. Проверка float значений
            (
                ["temperature"],
                {
                    "temperature": {
                        "type": float,
                        "gt": 0.0,
                        "lt": 100.0
                    }
                },
                (
                    {"temperature": -5.0},   # не проходит
                    {"temperature": 22.5},   # проходит
                    {"temperature": 100.0},  # не проходит
                    {"temperature": "hot"},   # не проходит (не float)
                ),
                [{"temperature": 22.5}]
            ),
            # 9. Без указания колонок
            ([], {"username": {"type": str, "min_length": 2, "max_length": 20}, 
                  "age": {"type": int, "gt": 2, "lt": 120}},
                ({"id": 1, "username": "Bob", "age": 24}, {"id": 2, "username": "Alice", "age": 14},
                 {"id": 3, "username": "Mark", "age": 1}, {"id": 4, "username": "Li", "age": 0},),
                [{"id": 1, "username": "Bob", "age": 24}, {"id": 2, "username": "Alice", "age": 14}])
        ]
)
def test_select(data, test_columns, test_conditions, exp_result):
    table = Table(name="test")
    table.storage.get_from_data_file = MagicMock(return_value=data)
    result = table.select(columns=test_columns, conditions=test_conditions)
    assert result == exp_result


def test_update(mock_data):
    table_structure = {"id": int, "username": str, "age": int}
    table = Table(name="test")
    table.storage.get_metadata = MagicMock(return_value=table_structure)
    table.storage.get_from_data_file = MagicMock(return_value=mock_data)
    new_data = {"username": "Franklin", "age": 25}
    test_conditions = {"username": "Mark"}
    result = table.update(new_data=new_data, conditions=test_conditions)
    assert result == 1


def test_delete(mock_data):
    table = Table(name="test")
    table.storage.get_from_data_file = MagicMock(return_value=mock_data)
    table.storage.update_data_file = MagicMock()
    test_conditions = {"username": "Bob"}
    result = table.delete(conditions=test_conditions)
    assert result == 1