from typing import Any, Dict, List
from src.enum_status import Status
from database_api import ApiResult
from abstract.abstract_data_api import AbstractDataAPI


class DataAPI(AbstractDataAPI):
    """Top-level API для операций с данными в таблице"""

    def __init__(self, table):
        self.table = table
    
    def insert(self, data: Dict[str, Any]) -> ApiResult:
        """Вставляет запись - делегирует низкоуровневому Table"""
        try:
            return self.table.insert(data)
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка при вставке данных: {str(e)}")
    
    def select(self, records: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Выбирает записи - делегирует низкоуровневому Table"""
        return self.table.select(records)
    
    def update(self, records: Dict[str, Any], new_data: Dict[str, Any]) -> ApiResult:
        """Обновляет записи - делегирует низкоуровневому Table"""
        try:
            return self.table.update(records, new_data)
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка при обновлении данных: {str(e)}")
    
    def delete_from(self, records: Dict[str, Any]) -> ApiResult:
        """Удаляет записи - делегирует низкоуровневому Table"""
        try:
            return self.table.delete_from(records)
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка при удалении данных: {str(e)}")
