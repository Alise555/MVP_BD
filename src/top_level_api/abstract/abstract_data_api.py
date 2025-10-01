from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple


class AbstractDataAPI(ABC):
    """Abstract API для операций с данными в таблице"""

    @abstractmethod
    def insert(self, table_name: str, fields: Tuple, values: List):
        """Вставляет новую запись в таблицу."""
        pass

    @abstractmethod
    def select(self, fields: tuple, table_name: str, filtered: tuple = None):
        """Выбирает записи из таблицы по условиям."""
        pass

    @abstractmethod
    def update(self, table_name: str, fields: Dict[str, Any], filtered: Tuple = None):
        """Обновляет записи в таблице."""
        pass

    @abstractmethod
    def delete_from(self, table_name: str, filtered: Tuple = None):
        """Удаляет записи из таблицы по условиям."""
        pass

    @abstractmethod
    def truncate_table(self, table_name:str):
        """Очищает таблицу."""
        pass
