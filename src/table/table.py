import os 
import json
from typing import Any, List, Dict, Optional
from table.container import Container  
from storage.storage import Storage 

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
        self.storage = storage if storage is not None else Storage()
        
        # Метаданные: {имя_колонки: тип_данных}
        self.columns_metadata = {}  # Заменяем self.columns
        # Данные таблицы: список строк, где каждая строка - список значений
        self.data = []
        
        # Загружаем начальные данные
        self._load_initial_data()
    
    def _load_initial_data(self):
        """Загрузка начальных данных из Storage"""
        try:
            # Создаем папку базы данных если не существует
            if not os.path.exists(self.db_name):
                os.makedirs(self.db_name, exist_ok=True)
            
            metadata_file_path = f"{self.db_name}/{self.name}_metadata.json"
            data_file_path = f"{self.db_name}/{self.name}_data.pkl"
            
            # Создаем файлы если не существуют
            if not os.path.exists(data_file_path):
                with open(data_file_path, 'wb') as f:
                    pass  # Создаем пустой файл
            
            if not os.path.exists(metadata_file_path):
                with open(metadata_file_path, 'w') as f:
                    json.dump({}, f)  # Создаем пустые метаданные
            
            self.columns_metadata = self.storage.get_metadata(metadata_file_path)
            self.data = self.storage.get_from_data_file(data_file_path)
            
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
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
    
    def add_column(self, column_info: dict) -> bool:
        """
        Добавить колонку в таблицу (только метаданные).
        
        Args:
            column_info (dict): Словарь с информацией о колонке {имя: тип}
        
        Returns:
            bool: True если успешно, False если ошибка
        """
        try:
            if not column_info:
                print("Ошибка: Пустая информация о колонке")
                return False
                
            column_name = list(column_info.keys())[0]
            data_type_str = str(column_info[column_name])
            
            # Преобразуем <class 'str'> в 'str'
            if "class" in data_type_str:
                data_type = data_type_str.split("'")[1]
            elif ":" in data_type_str:
                # Формат: str age (исправляем парсинг)
                data_type = data_type_str.split()[0]  # Берем первое слово
            else:
                data_type = data_type_str

            valid_types = ['str', 'int', 'float', 'bool']
            if data_type not in valid_types:
                print(f"Предупреждение: Неизвестный тип данных '{data_type}', используем 'str'")
                data_type = 'str'
            
            # Проверяем, существует ли уже колонка
            if column_name in self.columns_metadata:
                print(f"Ошибка: Колонка '{column_name}' уже существует")
                return False
            
            print(f"Добавление колонки '{column_name}' типа '{data_type}'")
            
            # ТОЛЬКО добавляем колонку в метаданные
            self.columns_metadata[column_name] = data_type
            
            # ТОЛЬКО сохраняем изменения метаданных через Storage
            metadata_file_path = f"{self.db_name}/{self.name}_metadata.json"
            self.storage.update_metadata(self.columns_metadata, metadata_file_path)
            
            print(f"Колонка '{column_name}' успешно добавлена в метаданные")
            return True
            
        except Exception as e:
            print(f"Ошибка при добавлении колонки: {e}")
            return False

    def modify_column(self, old_column_name: str, column_changes: dict) -> bool:
        """
        Изменить колонку в таблице (только метаданные).
        
        Args:
            old_column_name (str): Текущее имя колонки
            column_changes (dict): Словарь с изменениями {новое_имя: новый_тип}
        
        Returns:
            bool: True если успешно, False если ошибка
        """
        try:
            # Извлекаем новое имя и тип из словаря
            new_column_name = list(column_changes.keys())[0]
            new_data_type_str = str(column_changes[new_column_name])
            
            # Преобразуем <class 'str'> в 'str'
            if "class" in new_data_type_str:
                new_data_type = new_data_type_str.split("'")[1]
            else:
                new_data_type = new_data_type_str
            
            # Проверяем существование старой колонки
            if old_column_name not in self.columns_metadata:
                print(f"Ошибка: Колонка '{old_column_name}' не существует")
                return False
            
            # Проверяем, не конфликтует ли новое имя с существующими колонками
            if new_column_name != old_column_name and new_column_name in self.columns_metadata:
                print(f"Ошибка: Колонка '{new_column_name}' уже существует")
                return False
            
            print(f"Изменение колонки '{old_column_name}' на '{new_column_name}' с типом '{new_data_type}'")
            
            # ТОЛЬКО работаем с метаданными
            if new_column_name != old_column_name:
                # Сохраняем текущий тип данных и переименовываем
                current_type = self.columns_metadata[old_column_name]
                del self.columns_metadata[old_column_name]
                self.columns_metadata[new_column_name] = current_type
            
            # Всегда обновляем тип данных (даже если имя не изменилось)
            old_type = self.columns_metadata[new_column_name]
            self.columns_metadata[new_column_name] = new_data_type
            print(f"Тип данных изменен с '{old_type}' на '{new_data_type}'")
            
            # ТОЛЬКО сохраняем изменения метаданных
            metadata_file_path = f"{self.db_name}/{self.name}_metadata.json"
            self.storage.update_metadata(self.columns_metadata, metadata_file_path)
            
            print("Метаданные колонки успешно изменены")
            return True
            
        except Exception as e:
            print(f"Ошибка при изменении колонки: {e}")
            return False

    def drop_column(self, column_name: str) -> bool:
        """
        Удалить колонку из таблицы (только метаданные).
        
        Args:
            column_name (str): Имя колонки для удаления
            
        Returns:
            bool: True если успешно, False если ошибка
        """
        try:
            # Проверяем существование колонки
            if column_name not in self.columns_metadata:
                print(f"Ошибка: Колонка '{column_name}' не существует")
                return False
            
            print(f"Удаление колонки '{column_name}' из метаданных")
            
            # ТОЛЬКО удаляем колонку из метаданных
            del self.columns_metadata[column_name]
            
            # ТОЛЬКО сохраняем изменения метаданных
            metadata_file_path = f"{self.db_name}/{self.name}_metadata.json"
            self.storage.update_metadata(self.columns_metadata, metadata_file_path)
            
            print(f"Колонка '{column_name}' успешно удалена из метаданных")
            return True
            
        except Exception as e:
            print(f"Ошибка при удалении колонки: {e}")
            return False
    
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
    
    # Остальные методы остаются как заглушки
    def insert(self, values: Dict[str, Any]) -> bool:
        """Вставить запись в таблицу."""
        print(f"Вставка данных: {values} (заглушка)")
        return True
    
    def select(self, columns: List[str] = None, conditions: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Выбрать данные из таблицы."""
        print(f"Выборка колонок: {columns}, условия: {conditions} (заглушка)")
        return []
    
    def update(self, values: Dict[str, Any], conditions: Dict[str, Any] = None) -> int:
        """Обновить данные в таблице."""
        print(f"Обновление данных: {values}, условия: {conditions} (заглушка)")
        return 0
    
    def delete(self, conditions: Dict[str, Any] = None) -> int:
        """Удалить данные из таблицы."""
        print(f"Удаление данных с условиями: {conditions} (заглушка)")
        return 0
    
    def show_structure(self) -> None:
        """Показать структуру таблицы (для отладки)"""
        print(f"\nТаблица: {self.name}")
        print("Колонки:", self.columns_metadata)
        print("Количество записей:", len(self.data))
        if self.data:
            print("Первые 3 записи:")
            for i, row in enumerate(self.data[:3]):
                print(f"  {i}: {row}")