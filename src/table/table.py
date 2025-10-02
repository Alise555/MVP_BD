import os
from typing import Any, List, Dict, Optional


from table.container import Container
from storage.storage import Storage
from config.config import path


class Table(Container):
    """
    Класс, представляющий таблицу в базе данных.
    """

    def __init__(self):
        """
        Инициализация таблицы.

        Args:
            name (str): Имя таблицы
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

    # Остальные методы остаются как заглушки
    def insert(self, values: Dict[str, Any]) -> bool:
        """Вставить запись в таблицу."""
        print(f"Вставка данных: {values} (заглушка)")
        return True

    def select(
        self, columns: List[str] = None, conditions: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Выбрать данные из таблицы."""
        print(f"Выборка колонок: {columns}, условия: {conditions} (заглушка)")
        return []

    def update(self, values: Dict[str, Any], conditions: Dict[str, Any] = None) -> int:
        """Обновить данные в таблице."""
        pass

    def delete(self, conditions: Dict[str, Any] = None) -> int:
        """Удалить данные из таблицы."""
        pass

    def show_structure(self) -> None:
        """Показать структуру таблицы (для отладки)"""
        pass
