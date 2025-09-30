from typing import Any, Dict
from database_api import ApiResult
from abstract.abstract_table_api import AbstractTableAPI


class TableAPI(AbstractTableAPI):
    """Top-level API для работы с колонками таблицы и индексами."""
    
    def __init__(self, table):
        self.table = table
    
    def add_column(self, column_name: str, column_type: str) -> ApiResult:
        """Добавляет колонку - делегирует низкоуровневому Table"""
        try:
            return self.table.add_column(column_name, column_type)
        except Exception as e:
            return ApiResult(status=ApiResult.status.ERROR, message=f"Ошибка при добавлении колонки: {str(e)}")
    
    def modify_column(self, column_name: str, new_definition: Dict[str, Any]) -> ApiResult:
        """Изменяет колонку - делегирует низкоуровневому Table"""
        try:
            return self.table.modify_column(column_name, new_definition)
        except Exception as e:
            return ApiResult(status=ApiResult.status.ERROR, message=f"Ошибка при изменении колонки: {str(e)}")
    
    def drop_column(self, column_name: str) -> ApiResult:
        """Удаляет колонку - делегирует низкоуровневому Table"""
        try:
            return self.table.drop_column(column_name)
        except Exception as e:
            return ApiResult(status=ApiResult.status.ERROR, message=f"Ошибка при удалении колонки: {str(e)}")
    
    def create_index(self, index_name, index_struct) -> ApiResult:
        """Создает индекс - делегирует низкоуровневому Table"""
        try:
            return self.table.create_index(index_name, index_struct)
        except Exception as e:
            return ApiResult(status=ApiResult.status.ERROR, message=f"Ошибка при создании индекса: {str(e)}")
    
    def drop_index(self, index_name) -> ApiResult:
        """Удаляет индекс - делегирует низкоуровневому Table"""
        try:
            return self.table.drop_index(index_name)
        except Exception as e:
            return ApiResult(status=ApiResult.status.ERROR, message=f"Ошибка при удалении индекса: {str(e)}")
