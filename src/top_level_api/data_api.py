from typing import Any, Dict, List, Tuple
from src.enum_status import Status
from database_api import ApiResult
from abstract.abstract_data_api import AbstractDataAPI


class DataAPI(AbstractDataAPI):
    """Top-level API для операций с данными в таблице"""

    def __init__(self, table):
        self.table = table
    
    def insert(self, table_name: str, fields: Tuple, values: List[Any]) -> ApiResult:
        """Вставляет запись - делегирует низкоуровневому Table"""
        try:
            result = self.table.insert(table_name, fields, values)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка при вставке данных: {str(e)}")
    
    def select(self, fields: Tuple, table_name: str, filtered: Tuple = None):
        """Выбирает записи - делегирует низкоуровневому Table"""
        try:
            result = self.table.select_from(fields, table_name, filtered)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка при выборке данных: {str(e)}")
    
    def update(self, table_name: str, fields: Dict[str, Any], filtered: Tuple = None) -> ApiResult:
        """Обновляет записи - делегирует низкоуровневому Table"""
        try:
            result = self.table.update(table_name, fields, filtered)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка при обновлении данных: {str(e)}")
    
    def delete_from(self, table_name: str, filtered: Tuple = None) -> ApiResult:
        """Удаляет записи - делегирует низкоуровневому Table"""
        try:
            result = self.table.delete_from(table_name, filtered)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка при удалении данных: {str(e)}")
