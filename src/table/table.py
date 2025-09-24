from typing import Any, List, Dict, Optional
from src.container.container import Container  # Импортируем абстрактный класс

class Table(Container):
    """
    Класс, представляющий таблицу в базе данных.
    """
    
    def __init__(self, name: str):
        """
        Инициализация таблицы.
        
        Args:
            name (str): Имя таблицы
        """
        super().__init__(name)
        # TODO: Добавить инициализацию полей таблицы
        self.name = name
        self.columns = []  # Список колонок
        self.data = []     # Данные таблицы
        print(f"Таблица '{name}' создана (заглушка)")
    
    def get_name(self) -> str:
        """
        Получить имя таблицы.
        
        Returns:
            str: Имя таблицы
        """
        # TODO: Реализовать получение имени
        return self.name
    
    def get_size(self) -> int:
        """
        Получить количество записей в таблице.
        
        Returns:
            int: Количество записей
        """
        # TODO: Реализовать подсчет записей
        return len(self.data)
    
    def is_empty(self) -> bool:
        """
        Проверить, пуста ли таблица.
        
        Returns:
            bool: True если таблица пуста
        """
        # TODO: Реализовать проверку пустоты
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
        # TODO: Реализовать добавление колонки
        print(f"Добавление колонки '{column_name}' типа '{data_type}' (заглушка)")
        return True
    
    def modify_column(self, old_column_name: str, new_column_name: str, new_data_type: Optional[str] = None) -> bool:
        """
        Изменить колонку в таблице.
        
        Args:
            old_column_name (str): Текущее имя колонки
            new_column_name (str): Новое имя колонки
            new_data_type (str, optional): Новый тип данных
            
        Returns:
            bool: True если успешно, False если ошибка
        """
        # TODO: Реализовать изменение колонки
        print(f"Изменение колонки '{old_column_name}' на '{new_column_name}' (заглушка)")
        return True
    
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
    
    def insert(self, values: Dict[str, Any]) -> bool:
        """
        Вставить запись в таблицу.
        
        Args:
            values (Dict[str, Any]): Словарь значений для вставки
                {имя_колонки: значение}
                
        Returns:
            bool: True если успешно, False если ошибка
        """
        # TODO: Реализовать вставку данных
        print(f"Вставка данных: {values} (заглушка)")
        return True
    
    def select(self, columns: List[str] = None, conditions: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Выбрать данные из таблицы.
        
        Args:
            columns (List[str], optional): Список колонок для выборки
            conditions (Dict[str, Any], optional): Условия выборки
            
        Returns:
            List[Dict[str, Any]]: Список строк, соответствующих условиям
        """
        # TODO: Реализовать выборку данных
        print(f"Выборка колонок: {columns}, условия: {conditions} (заглушка)")
        return []
    
    def update(self, values: Dict[str, Any], conditions: Dict[str, Any] = None) -> int:
        """
        Обновить данные в таблице.
        
        Args:
            values (Dict[str, Any]): Новые значения
            conditions (Dict[str, Any], optional): Условия для обновления
            
        Returns:
            int: Количество обновленных строк
        """
        # TODO: Реализовать обновление данных
        print(f"Обновление данных: {values}, условия: {conditions} (заглушка)")
        return 0
    
    def delete(self, conditions: Dict[str, Any] = None) -> int:
        """
        Удалить данные из таблицы.
        
        Args:
            conditions (Dict[str, Any], optional): Условия для удаления
            
        Returns:
            int: Количество удаленных строк
        """
        # TODO: Реализовать удаление данных
        print(f"Удаление данных с условиями: {conditions} (заглушка)")
        return 0
    
