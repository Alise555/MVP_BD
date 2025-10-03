import os
from typing import Any, List, Dict, Optional, Tuple
from table.container import Container
from storage.storage import Storage
from config.config import path, metadata_name
from models.dynamic_model import create_dynamic_model


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

    def add_column(
        self, db_name: str, table_name, column_name: str, data_type: str
    ) -> bool:
        """
        Добавить колонку в таблицу.

        Args:
            column_name (str): Имя колонки
            data_type (str): Тип данных колонки

        Returns:
            bool: True если успешно, False если ошибка
        """
        try:
            columns_metadata = self._load_table_data(
                db_name=db_name, table_name=table_name
            )
            # Проверяем, существует ли уже колонка
            if column_name in columns_metadata:
                print(f"Ошибка: Колонка '{column_name}' уже существует")
                return False

            print(f"Добавление колонки '{column_name}' типа '{data_type}'")

            # 1. Добавляем колонку в метаданные
            columns_metadata[column_name] = data_type

            # 2. Добавляем значение по умолчанию к каждой существующей строке
            default_value = self._get_default_value(data_type)
            for row in self.data:
                row.append(default_value)

            # 3. Сохраняем изменения через Storage
            self.storage.update_metadata(columns_metadata)
            #     self.storage.update_data_file(self.data) нужно продумать функционал обновления данных

            print(f"Колонка '{column_name}' успешно добавлена")
            return True

        except Exception as e:
            print(f"Ошибка при добавлении колонки: {e}")
            return False

    def modify_column(
        self,
        db_name: str,
        table_name: str,
        old_column_name: str,
        new_column_name: str,
        new_data_type: Optional[str] = None,
    ) -> bool:
        """
        Изменить колонку в таблице.

        Args:
            old_column_name (str): Текущее имя колонки
            new_column_name (str): Новое имя колонки
            new_data_type (str, optional): Новый тип данных

        Returns:
            bool: True если успешно, False если ошибка
        """
        pass

    def drop_column(self, column_name: str) -> bool:
        """
        Удалить колонку из таблицы.

        Args:
            column_name (str): Имя колонки для удаления

        Returns:
            bool: True если успешно, False если ошибка
        """
        pass

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

    def insert(self, db_name: str, table_name: str, fields: Tuple[str], values: List[str]) -> bool:
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
            PydanticModel = create_dynamic_model(conditions=table_structure)
            print(PydanticModel.__annotations__)
            data = [dict(zip(fields, item)) for item in values]
            if all(PydanticModel.model_validate(d) for d in data):
                self.storage.write_data(table_path=table_path, data=data)
                return True
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
            conditions (Tuple[str], optional): Условия выборки, например:
                {
                    "username": {
                        "type": str,
                        "min_length": 3,
                        "max_length": 20,
                    },
                    "age": {
                        "type": int,
                        "gt": 0,
                        "lt": 120
                    }
                }

        Returns:
            List[Dict[str, Any]]: Список строк, соответствующих условиям
        """
        db_path = os.path.join(path, db_name)
        table_path = os.path.join(db_path, table_name)
        full_data = self.storage.read_data(table_path)
        filtered_data = []
        if conditions:
            for row in full_data:
                match = True
                for field, rules in conditions.items():
                    # проверка наличия поля
                    if field not in row:
                        match = False
                        break
                    value = row[field]
                    # проверка типа поля
                    if "type" in rules and not isinstance(value, rules["type"]):
                        match = False
                        break
                    # проверка строки на длину
                    if isinstance(value, str):
                        if (
                            "min_length" in rules and len(value) < rules["min_length"]
                        ) or (
                            "max_length" in rules and len(value) > rules["max_length"]
                        ):
                            match = False
                            break
                    # проверка числа
                    if isinstance(value, (int, float)):
                        if ("gt" in rules and value <= rules["gt"]) or (
                            "lt" in rules and value >= rules["lt"]
                        ):
                            match = False
                            break
                    if not isinstance(rules, dict) and value != rules:
                        match = False
                        break
                if match:
                    filtered_data.append(row)

        data = filtered_data if conditions else full_data

        if columns:
            return [{key: row[key] for key in columns if key in row} for row in data]
        print(f"Выбор колонок: {columns}, условия: {conditions}")
        return filtered_data

    def update(
        self, 
        new_data: Dict[str, Any], 
        db_name: str,
        table_name: str,
        conditions: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Обновить данные в таблице.

        Args:
            new_data (Dict[str, Any]): Новые значения
            conditions (Dict[str, Any], optional): Условия для обновления

        Returns:
            int: Количество обновленных строк
        """
        db_path = os.path.join(path, db_name)
        table_path = os.path.join(db_path, table_name)

        updated_rows = 0
        table_structure = self.storage.get_metadata(table_path)
        PydanticModel = create_dynamic_model(conditions=table_structure)

        full_data = self.storage.get_from_data_file(table_path)
        for row in full_data:
            # Проверяем, подходит ли строка под условия (если условия есть)
            match = True
            if conditions:
                match = all(row.get(key) == value for key, value in conditions.items())

            if match and len(full_data) > 1:
                row.update(new_data)  # Обновляем только разрешённые поля
                try:
                    if PydanticModel(**row):
                        updated_rows += 1
                except Exception as e:
                    print(f"Новые данные введены с ошибкой. Проверьте условия: {e}")
        if updated_rows > 0:
            self.storage.update_data_file(path, full_data)
        print(f"Обновление данных: {new_data}, условия: {conditions} ")
        return updated_rows

    def delete(self, db_name: str, table_name: str, 
               conditions: Dict[str, Any]) -> int:
        """
        Удалить данные из таблицы.

        Args:
            table_name (str): Имя таблицы
            conditions (Dict[str, Any]): Условия для удаления

        Returns:
            int: Количество удаленных строк
        """
        db_path = os.path.join(path, db_name)
        table_path = os.path.join(db_path, table_name)

        full_data = self.storage.get_from_data_file(table_path)
        remaining_data = []
        delete_rows = 0

        for row in full_data:
            match = all(row.get(key) == value for key, value in conditions.items())
            if match:
                delete_rows += 1
            else:
                remaining_data.append(row)
        # Сохраняем оставшиеся данные обратно в хранилище
        self.storage.update_data_file(table_path, remaining_data)
        return delete_rows

    def show_structure(self) -> None:
        """Показать структуру таблицы (для отладки)"""
        print(f"\nТаблица: {self.name}")
        print("Колонки:", self.columns_metadata)
        print("Количество записей:", len(self.data))
        if self.data:
            print("Первые 3 записи:")
            for i, row in enumerate(self.data[:3]):
                print(f"  {i}: {row}")
