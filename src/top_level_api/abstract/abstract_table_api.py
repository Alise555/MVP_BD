from abc import ABC, abstractmethod
from typing import Dict, Any


class AbstractTableAPI(ABC):
    """Abstract API для работы с колонками таблицы и индексы."""

    @abstractmethod
    def add_column(self, table_name: str, column_data: Dict):
        """Добавляет новую колонку в таблицу."""
        pass

    @abstractmethod
    def modify_column(self, table_name: str, column_name: str, column_data: Dict):
        """Изменяет существующую колонку."""
        pass

    @abstractmethod
    def drop_column(self, table_name: str, column_name: str):
        """Удаляет колонку из таблицы."""
        pass
    
    @abstractmethod
    def create_index(self, index_name: str, index_struct:dict):
        """Создает индекс для таблицы."""
        pass

    @abstractmethod
    def drop_index(self, index_name: str):
        """Удаляет индекс из таблицы."""
        pass
