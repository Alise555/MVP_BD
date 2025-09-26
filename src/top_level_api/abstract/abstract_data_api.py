from abc import ABC, abstractmethod
from typing import Dict, Any


class AbstractDataAPI(ABC):
    """Abstract API для операций с данными в таблице"""

    @abstractmethod
    def insert(self, data: Dict[str, Any]):
        """Вставляет новую запись в таблицу."""
        pass

    @abstractmethod
    def select(self, records: Dict[str, Any] = None):
        """Выбирает записи из таблицы по условиям."""
        pass

    @abstractmethod
    def update(self, records: Dict[str, Any], new_data: Dict[str, Any]):
        """Обновляет записи в таблице."""
        pass

    @abstractmethod
    def delete_from(self, records: Dict[str, Any]):
        """Удаляет записи из таблицы по условиям."""
        pass
