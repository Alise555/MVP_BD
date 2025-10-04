import os
from typing import Any, List, Dict, Optional, Tuple
from table.container import Container
from storage.storage import Storage
from config.config import path, metadata_name
from models.dynamic_model import create_dynamic_model
from pydantic_core import ValidationError
from enum_status import Status


class Table(Container):
    """
    Класс, представляющий таблицу в базе данных.
    """

    def __init__(self):
        """
        Инициализация таблицы.

        Args:
            table_name (str): Имя таблицы
            db_name (str): Имя базы данных
            storage (Storage, optional): Объект хранилища. Если не передан, создается новый.
        """
        self.storage = Storage()

    def _load_table_data(self, db_name: str, table_name: str):
        """Загрузка начальных данных из Storage"""
        return self.storage.get_metadata(os.path.join(path, db_name, table_name))

    # def get_name(self) -> str:
    #     """Получить имя таблицы."""
    #     return self.name

    # def get_size(self) -> int:
    #     """Получить количество записей в таблице."""
    #     return len(self.data)

    # def is_empty(self) -> bool:
    #     """Проверить, пуста ли таблица."""
    #     return len(self.data) == 0

    # def add_column(
    #     self, db_name: str, table_name, column_name: str, data_type: str
    # ) -> bool:
    #     """
    #     Добавить колонку в таблицу.

    #     Args:
    #         column_name (str): Имя колонки
    #         data_type (str): Тип данных колонки

    #     Returns:
    #         bool: True если успешно, False если ошибка
    #     """
    #     try:
    #         columns_metadata = self._load_table_data(
    #             db_name=db_name, table_name=table_name
    #         )
    #         # Проверяем, существует ли уже колонка
    #         if column_name in columns_metadata:
    #             print(f"Ошибка: Колонка '{column_name}' уже существует")
    #             return False

    #         print(f"Добавление колонки '{column_name}' типа '{data_type}'")

    #         # 1. Добавляем колонку в метаданные
    #         columns_metadata[column_name] = data_type

    #         # 2. Добавляем значение по умолчанию к каждой существующей строке
    #         default_value = self._get_default_value(data_type)
    #         for row in self.data:
    #             row.append(default_value)

    #         # 3. Сохраняем изменения через Storage
    #         self.storage.update_metadata(columns_metadata)
    #         #     self.storage.update_data_file(self.data) нужно продумать функционал обновления данных

    #         print(f"Колонка '{column_name}' успешно добавлена")
    #         return True

    #     except Exception as e:
    #         print(f"Ошибка при добавлении колонки: {e}")
    #         return False

    # def modify_column(
    #     self,
    #     db_name: str,
    #     table_name: str,
    #     old_column_name: str,
    #     new_column_name: str,
    #     new_data_type: Optional[str] = None,
    # ) -> bool:
    #     """
    #     Изменить колонку в таблице.

    #     Args:
    #         old_column_name (str): Текущее имя колонки
    #         new_column_name (str): Новое имя колонки
    #         new_data_type (str, optional): Новый тип данных

    #     Returns:
    #         bool: True если успешно, False если ошибка
    #     """
    #     pass

    # def drop_column(self, column_name: str) -> bool:
    #     """
    #     Удалить колонку из таблицы.

    #     Args:
    #         column_name (str): Имя колонки для удаления

    #     Returns:
    #         bool: True если успешно, False если ошибка
    #     """
    #     pass

    def _get_default_value(self, data_type: str) -> Any:
        """Возвращает значение по умолчанию для типа данных"""
        defaults = {"str": "", "int": 0, "float": 0.0, "bool": False}
        return defaults.get(data_type, None)

    def _convert_value(self, value: Any, target_type: str) -> Any:
        """Преобразует значение к целевому типу"""
        converters = {"str": str, "int": int, "float": float, "bool": bool}
        converter = converters.get(target_type)
        if converter:
            return converter(value)
        return value

    def insert(
        self, db_name: str, table_name: str, fields: Tuple[str], values: List[str]
    ) -> bool:
        """
        Вставить запись в таблицу.

        Args:
            values (Dict[str, Any]): Список Pydantic-моделей для вставки
                {имя_колонки: значение}

        Returns:
            bool: True если успешно, False если ошибка
        """
        db_path = os.path.join(path, db_name)
        table_path = os.path.join(db_path, table_name)
        try:
            table_structure = self.storage.get_metadata(table_path)
            PydanticModel = create_dynamic_model(
                conditions=table_structure, strict=True
            )
            data = [dict(zip(fields, item)) for item in values]
            for item in data:
                if PydanticModel.model_validate(item):
                    self.storage.write_data(table_path=table_path, data=[item])
            return Status.OK
        except ValidationError as e:
            print(f"Allowed only {table_structure} fields!\n{e}")
        except Exception as e:
            print(f"Error: {e}")
            return False

    def select(
        self,
        db_name: str,
        table_name: str,
        columns: Optional[Tuple[str]] = None,
        conditions: Optional[Tuple[str]] = None,
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Выбрать данные из таблицы.

        Args:
            columns (Tuple[str], optional): Список колонок для вывода
            conditions (Tuple[str], optional): Условия выборки

        Returns:
            List[Dict[str, Any]]: Список строк, соответствующих условиям
        """
        db_path = os.path.join(path, db_name)
        table_path = os.path.join(db_path, table_name)
        table_structure = self.storage.get_metadata(table_path)
        PydanticModel = create_dynamic_model(conditions=table_structure)
        new_data = []
        for item, offset in self.storage.read_data(table_path):
            if PydanticModel.model_validate(item):
                if conditions:
                    if check_conditions(conditions, item) is False:
                        continue
                if columns:
                    new_dict = {}
                    for column in columns:
                        try:
                            new_dict[column] = item[column]
                        except KeyError as e:
                            raise Exception(f"Unknown field {column}")
                    new_data.append(new_dict)
                else:
                    new_data.append(item)
        return new_data

    def update(
        self,
        new_data: Dict[str, Any],
        db_name: str,
        table_name: str,
        conditions: Optional[Tuple[str]] = None,
    ) -> int:
        """
        Обновить данные в таблице.

        Args:
            new_data (Dict[str, Any]): Новые значения
            conditions (Tuple[str], optional): Условия для обновления

        Returns:
            int: Количество обновленных строк
        """
        db_path = os.path.join(path, db_name)
        table_path = os.path.join(db_path, table_name)
        table_structure = self.storage.get_metadata(table_path)
        PydanticModel = create_dynamic_model(conditions=table_structure)
        for item, offset in self.storage.read_data(table_path):
            for key, value in new_data.items():
                if item.get(key, None) is not None:
                    item[key] = value
            if PydanticModel.model_validate(item):
                if conditions:
                    if check_conditions(conditions, item) is False:
                        continue
                self.storage.update_data(offset, item, table_path)
        return Status.OK

    def delete(self, db_name: str, table_name: str, conditions: Tuple[str]) -> int:
        """
        Удалить данные из таблицы.

        Args:
            table_name (str): Имя таблицы
            conditions (Tuple[str]): Условия для удаления

        Returns:
            int: Количество удаленных строк
        """
        db_path = os.path.join(path, db_name)
        table_path = os.path.join(db_path, table_name)

        for item, offset in self.storage.read_data(table_path):
            if conditions:
                if check_conditions(conditions, item) is False:
                    continue
            self.storage.delete_data(offset, table_path)
        return Status.OK

    def show_structure(self) -> None:
        """Показать структуру таблицы (для отладки)"""
        print(f"\nТаблица: {self.name}")
        print("Колонки:", self.columns_metadata)
        print("Количество записей:", len(self.data))
        if self.data:
            print("Первые 3 записи:")
            for i, row in enumerate(self.data[:3]):
                print(f"  {i}: {row}")


def parse_condition(condition_str: str) -> tuple:
    """Разбирает строку условия на столбец, оператор и значение."""
    # Определяем оператор (первый из доступных в строке)
    operators = [">=", "<=", "!=", "=", ">", "<"]
    operator = None
    for op in operators:
        if op in condition_str:
            operator = op
            break

    if not operator:
        raise ValueError(f"Неизвестный оператор в условии: {condition_str}")

    # Разбиваем строку на части
    column, value_str = condition_str.split(operator, 1)
    column = column.strip()

    # Преобразуем значение в нужный тип (int, float или str)
    try:
        value = int(value_str.strip())
    except ValueError:
        try:
            value = float(value_str.strip())
        except ValueError:
            value = value_str.strip().strip("'\"")  # Убираем кавычки, если строка

    return column, operator, value


def check_conditions(conditions: tuple, row: dict) -> bool:
    match = True
    for condition_str in conditions:
        column, operator, value = parse_condition(condition_str)
        row_value = str(row.get(column))
        value = str(value)

        # Проверяем условие
        if operator == "=" and not row_value == value:
            match = False
            break
        elif operator == ">" and not (row_value > value):
            match = False
            break
        elif operator == "<" and not (row_value < value):
            match = False
            break
        elif operator == ">=" and not (row_value >= value):
            match = False
            break
        elif operator == "<=" and not (row_value <= value):
            match = False
            break
        elif operator == "!=" and not (row_value != value):
            match = False
            break
    return match
