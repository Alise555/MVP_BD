from typing import Any, List, Dict, Optional
from src.container.container import Container  
from src.storage.storage import Storage 

class Table(Container):
    """
    Класс, представляющий таблицу в базе данных.
    """
    
    def __init__(self, name: str, db_name: str = "default_db"):
        """
        Инициализация таблицы.
        
        Args:
            name (str): Имя таблицы
            db_name (str): Имя базы данных
        """
        super().__init__(name)
        self.name = name
        self.db_name = db_name
        self.storage = Storage(db_name, name)
        
        # Метаданные: {имя_колонки: тип_данных}
        self.columns_metadata = {}  # Заменяем self.columns
        # Данные таблицы: список строк, где каждая строка - список значений
        self.data = []
        
        # Загружаем начальные данные
        self._load_initial_data()
    
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
        try:
            # Проверяем существование колонки
            if column_name not in self.columns_metadata:
                print(f"Ошибка: Колонка '{column_name}' не существует")
                return False
            
            print(f"Удаление колонки '{column_name}'")
            
            # 1. Определяем индекс удаляемой колонки
            col_index = list(self.columns_metadata.keys()).index(column_name)
            
            # 2. Удаляем колонку из метаданных
            del self.columns_metadata[column_name]
            
            # 3. Удаляем соответствующий столбец из каждой строки данных
            for row in self.data:
                if len(row) > col_index:
                    del row[col_index]
            
            # 4. Сохраняем изменения через Storage
            self.storage.update_metadata(self.columns_metadata)
            self.storage.update_data_file(self.data)
            
            print(f"Колонка '{column_name}' успешно удалена")
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