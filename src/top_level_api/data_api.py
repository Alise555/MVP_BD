from typing import Any, Dict
from database_api import ApiResult
from abstract.abstract_data_api import AbstractDataAPI
from src.enum_status import Status


class DataAPI(AbstractDataAPI):
    """Top-level API для операций с данными в таблице"""

    def __init__(self, table):
        self.table = table
    
    def insert(self, data: Dict[str, Any]) -> ApiResult:
        """Вставляет запись - делегирует низкоуровневому Table"""
        return self.table.insert(data)
    
    def select(self, records: Dict[str, Any] = None):
        """Выбирает записи - делегирует низкоуровневому Table"""
        return super().select(records)
    
    def update(self, records: Dict[str, Any], new_data: Dict[str, Any]) -> ApiResult:
        """Обновляет записи - делегирует низкоуровневому Table"""
        return super().update(records, new_data)
    
    def delete_from(self, records: Dict[str, Any]) -> ApiResult:
        """Удаляет записи - делегирует низкоуровневому Table"""
        return super().delete_from(records)
