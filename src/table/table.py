from typing import Any, List, Dict, Optional
from src.table.container import Container  
from src.storage.storage import Storage 
from src.models.dynamic_model import create_dynamic_model
from src.config import Config
# from src.index.index import Index


class Table(Container):
    """
    Класс, представляющий таблицу в базе данных.
    """
    
    def __init__(self, name: str, db_name: str = "default_db", storage: Storage = None):
        """
        Инициализация таблицы.
        
        Args:
            name (str): Имя таблицы
            db_name (str): Имя базы данных
            storage (Storage, optional): Объект хранилища. Если не передан, создается новый.
        """
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
        config = Config()
        self.data_file_path = config.data_file_path
        self.metadata_file_path = config.metadata_file_path
    
    def _load_initial_data(self):
        """Загрузка начальных данных из Storage"""
        try:
            self.columns_metadata = self.storage.load_metadata()
            self.data = self.storage.load_data()
        except:
            # Если файлы не существуют, инициализируем пустыми значениями
            self.columns_metadata = {}
            self.data = []
    
    def get_name(self) -> str:
        """Получить имя таблицы."""
        return self.name
    
    def get_size(self) -> int:
        """Получить количество записей в таблице."""
        return len(self.data)
    
    def is_empty(self) -> bool:
        """Проверить, пуста ли таблица."""
        return len(self.data) == 0
    
    def add_column(self, column_name: str, data_type: str) -> bool:
        """
        Добавить колонку в таблицу.
        
        Args:
            column_name (str): Имя колонки
            data_type (str): Тип данных колонки
            
        Returns:
            bool: True если успешно, False если ошибка
        """
        try:
            # Проверяем, существует ли уже колонка
            if column_name in self.columns_metadata:
                print(f"Ошибка: Колонка '{column_name}' уже существует")
                return False
            
            print(f"Добавление колонки '{column_name}' типа '{data_type}'")
            
            # 1. Добавляем колонку в метаданные
            self.columns_metadata[column_name] = data_type
            
            # 2. Добавляем значение по умолчанию к каждой существующей строке
            default_value = self._get_default_value(data_type)
            for row in self.data:
                row.append(default_value)
            
            # 3. Сохраняем изменения через Storage
            self.storage.update_metadata(self.columns_metadata)
            self.storage.update_data_file(self.data)
            
            print(f"Колонка '{column_name}' успешно добавлена")
            return True
            
        except Exception as e:
            print(f"Ошибка при добавлении колонки: {e}")
            return False
    
    def modify_column(self, old_column_name: str, new_column_name: str, 
                      new_data_type: Optional[str] = None) -> bool:
        """
        Изменить колонку в таблице.
        
        Args:
            old_column_name (str): Текущее имя колонки
            new_column_name (str): Новое имя колонки
            new_data_type (str, optional): Новый тип данных
            
        Returns:
            bool: True если успешно, False если ошибка
        """
        try:
            # Проверяем существование старой колонки
            if old_column_name not in self.columns_metadata:
                print(f"Ошибка: Колонка '{old_column_name}' не существует")
                return False
            
            # Проверяем, не конфликтует ли новое имя с существующими колонками
            if new_column_name != old_column_name and new_column_name in self.columns_metadata:
                print(f"Ошибка: Колонка '{new_column_name}' уже существует")
                return False
            
            print(f"Изменение колонки '{old_column_name}' на '{new_column_name}'")
            
            # 1. Получаем индекс колонки
            column_names = list(self.columns_metadata.keys())
            col_index = column_names.index(old_column_name)
            
            # 2. Изменяем имя колонки если нужно
            if new_column_name != old_column_name:
                # Сохраняем тип данных
                data_type = self.columns_metadata[old_column_name]
                # Удаляем старую колонку и добавляем с новым именем
                del self.columns_metadata[old_column_name]
                self.columns_metadata[new_column_name] = data_type
                # Обновляем индекс
                col_index = list(self.columns_metadata.keys()).index(new_column_name)
            
            # 3. Изменяем тип данных если указан
            if new_data_type and new_data_type != self.columns_metadata[new_column_name]:
                old_type = self.columns_metadata[new_column_name]
                self.columns_metadata[new_column_name] = new_data_type
                print(f"Тип данных изменен с '{old_type}' на '{new_data_type}'")
                
                # Преобразуем существующие данные к новому типу
                for row in self.data:
                    if row[col_index] is not None:
                        try:
                            row[col_index] = self._convert_value(row[col_index], new_data_type)
                        except (ValueError, TypeError):
                            # Если преобразование невозможно, устанавливаем значение по умолчанию
                            row[col_index] = self._get_default_value(new_data_type)
            
            # 4. Сохраняем изменения через Storage
            self.storage.update_metadata(self.columns_metadata)
            self.storage.update_data_file(self.data)
            
            print("Колонка успешно изменена")
            return True
            
        except Exception as e:
            print(f"Ошибка при изменении колонки: {e}")
            return False
    
    def drop_column(self, column_name: str) -> bool:
        """
        Удалить колонку из таблицы.
        
        Args:
            column_name (str): Имя колонки для удаления
            
        Returns:
            bool: True если успешно, False если ошибка
        """
        # TODO: Реализовать удаление колонки
        print(f"Удаление колонки '{column_name}' (заглушка)")
        return True
    
    def _get_default_value(self, data_type: str) -> Any:
        """Возвращает значение по умолчанию для типа данных"""
        defaults = {
            'str': '',
            'int': 0,
            'float': 0.0,
            'bool': False
        }
        return defaults.get(data_type, None)
    
    def _convert_value(self, value: Any, target_type: str) -> Any:
        """Преобразует значение к целевому типу"""
        converters = {
            'str': str,
            'int': int,
            'float': float,
            'bool': bool
        }
        converter = converters.get(target_type)
        if converter:
            return converter(value)
        return value

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
            PydanticModel = create_dynamic_model(conditions=table_structure)
            object = PydanticModel(**values)
            self.storage.insert_in_data_file(self.data_file_path, values)
            print(f"Вставка данных: {object} (заглушка)")
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
            PydanticModel = create_dynamic_model(conditions=conditions)
            for row in full_data:
                try: 
                    PydanticModel(**row)
                    filtered_data.append(row)
                except Exception:
                    continue
        if columns:
            result = []
            for row in filtered_data:
                result.append({key: row[key] for key in columns if key in row}) 
            return result
        print(f"Выбор колонок: {columns}, условия: {conditions} (заглушка)")
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

        if PydanticModel(**new_data):
            full_data = self.storage.get_from_data_file(self.data_file_path)
            for row in full_data:
                # Проверяем, подходит ли строка под условия (если условия есть)
                match = True
                if conditions:
                    match = all(row.get(key) == value for key, value in conditions.items())

                if match and len(full_data) > 1:
                    row.update(new_data)  # Обновляем только разрешённые поля
                    updated_rows += 1
            if updated_rows > 0:
                self.storage.update_data_file(self.data_file_path, full_data)
            print(f"Обновление данных: {new_data}, условия: {conditions} (заглушка)")
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
        PydanticModel = create_dynamic_model(conditions=conditions)

        # Фильтруем строки, которые НЕ соответствуют условиям (их оставим)
        remaining_data = []
        delete_rows = 0

        for row in full_data:
            try:
                PydanticModel(**row)  # Если валидация проходит, строка подлежит удалению
                delete_rows += 1
            except Exception:
                remaining_data.append(row)  # Если не проходит, оставляем

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

    