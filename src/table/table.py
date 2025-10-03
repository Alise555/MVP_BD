import os
from typing import Any, List, Dict, Optional
from table.container import Container
from storage.storage import Storage
from config.config import path
from models.dynamic_model import create_dynamic_model


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
<<<<<<< HEAD
        self.storage = Storage()

    def _load_table_data(self, db_name: str, table_name: str):
=======
        super().__init__(name)
        self.name = name
        self.db_name = db_name
        self.storage = storage if storage is not None else Storage(db_name, name)
        
        # Метаданные: {имя_колонки: тип_данных}
        self.columns_metadata = {}  # Заменяем self.columns
        # Данные таблицы: список строк, где каждая строка - список значений
        self.data = []
        
        # Загружаем начальные данные
        self._load_initial_data()
        # self.indexes = Index.get_all_indexes()
        self.config = Config()
        self.data_file_path = self.config.data_file_path
        self.metadata_file_path = self.config.metadata_file_path
    
    def _load_initial_data(self):
>>>>>>> Table
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
<<<<<<< HEAD

    def modify_column(
        self,
        db_name: str,
        table_name: str,
        old_column_name: str,
        new_column_name: str,
        new_data_type: Optional[str] = None,
    ) -> bool:
=======
    
    def modify_column(self, old_column_name: str, new_column_name: str, 
                      new_data_type: Optional[str] = None) -> bool:
>>>>>>> Table
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
<<<<<<< HEAD
        pass

=======
        # TODO: Реализовать удаление колонки
        print(f"Удаление колонки '{column_name}' (заглушка)")
        return True
    
>>>>>>> Table
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

<<<<<<< HEAD
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
=======
    def insert(self, values: Dict[str, Any]) -> Dict[str, bool]:
        """
        Вставить запись в таблицу.
        
        Args:
            values (Dict[str, Any]): Список Pydantic-моделей для вставки
                {имя_колонки: значение}
                
        Returns:
            Dict[str, bool]: True если успешно, False если ошибка
        """
        try:
            table_structure = self.storage.get_metadata(self.metadata_file_path)
            print(table_structure, "eeee")
            PydanticModel = create_dynamic_model(conditions=table_structure)
            print(PydanticModel.__annotations__)
            object = PydanticModel(**values)
            self.storage.insert_in_data_file(self.data_file_path, values)
            print(f"Вставка данных: {object}")
            return {"success": True}
        except Exception as e:
            print(f"Error: {e}")
            return {"success": False}

    def select(self,
               columns: Optional[List[str]] = None, 
               conditions: Optional[Dict[str, Any]] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Выбрать данные из таблицы.
        
        Args:
            columns (List[str], optional): Список колонок для вывода
            conditions (Dict[str, Any], optional): Условия выборки, например:
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
        full_data = self.storage.get_from_data_file(self.data_file_path)
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
                        if ("min_length" in rules and 
                            len(value) < rules["min_length"]) or ("max_length" in rules and 
                                                                  len(value) > rules["max_length"]):
                            match = False
                            break
                    # проверка числа 
                    if isinstance(value, (int, float)):
                        if ("gt" in rules and value <= rules["gt"]) or ("lt" in rules and value >= rules["lt"]):
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

    def update(self,
               new_data: Dict[str, Any], 
               conditions: Optional[Dict[str, Any]] = None) -> int:
        """
        Обновить данные в таблице.
        
        Args:
            new_data (Dict[str, Any]): Новые значения
            conditions (Dict[str, Any], optional): Условия для обновления
            
        Returns:
            int: Количество обновленных строк
        """
        updated_rows = 0
        table_structure = self.storage.get_metadata(self.metadata_file_path)
        PydanticModel = create_dynamic_model(conditions=table_structure)

        full_data = self.storage.get_from_data_file(self.data_file_path)
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
            self.storage.update_data_file(self.data_file_path, full_data)
        print(f"Обновление данных: {new_data}, условия: {conditions} ")
        return updated_rows
    
    def delete(self,
               conditions: Dict[str, Any]) -> int:
        """
        Удалить данные из таблицы.
        
        Args:
            table_name (str): Имя таблицы
            conditions (Dict[str, Any]): Условия для удаления
            
        Returns:
            int: Количество удаленных строк
        """
        full_data = self.storage.get_from_data_file(self.data_file_path)
        remaining_data = []
        delete_rows = 0

        for row in full_data:
            match = all(row.get(key) == value for key, value in conditions.items())
            if match:
                delete_rows += 1
            else:
                remaining_data.append(row)
        # Сохраняем оставшиеся данные обратно в хранилище
        self.storage.update_data_file(self.data_file_path, tuple(remaining_data))
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

    
>>>>>>> Table
