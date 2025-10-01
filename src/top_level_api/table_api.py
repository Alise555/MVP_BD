from typing import Any, Dict
from src.enum_status import Status
from database_api import ApiResult
from abstract.abstract_table_api import AbstractTableAPI


class TableAPI(AbstractTableAPI):
    """Top-level API для работы с колонками таблицы и индексами."""
    
    def __init__(self, table):
        self.table = table
    
    def add_column(self, table_name: str, column_data: Dict) -> ApiResult:
        """Добавляет колонку - делегирует низкоуровневому Table"""
        try:
            result = self.table.add_column(table_name, column_data)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(status=ApiResult.status.ERROR, message=f"Ошибка при добавлении колонки: {str(e)}")
    
    def modify_column(self, table_name: str, column_name: str, column_data: Dict) -> ApiResult:
        """Изменяет колонку - делегирует низкоуровневому Table"""
        try:
            return self.table.modify_column(table_name, column_name, column_data)
        except Exception as e:
            return ApiResult(status=ApiResult.status.ERROR, message=f"Ошибка при изменении колонки: {str(e)}")
    
    def drop_column(self, table_name: str, column_name: str) -> ApiResult:
        """Удаляет колонку - делегирует низкоуровневому Table"""
        try:
            return self.table.drop_column(table_name, column_name)
        except Exception as e:
            return ApiResult(status=ApiResult.status.ERROR, message=f"Ошибка при удалении колонки: {str(e)}")
    
    def create_index(self, table_name: str, index_name: str, index_struct: Dict) -> ApiResult:
        """Создает индекс - делегирует низкоуровневому Table"""
        try:
            result = self.table.create_index(table_name, index_name, index_struct)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(status=ApiResult.status.ERROR, message=f"Ошибка при создании индекса: {str(e)}")
    
    def drop_index(self, table_name: str, index_name: str) -> ApiResult:
        """Удаляет индекс - делегирует низкоуровневому Table"""
        try:
            result = self.table.drop_index(table_name, index_name)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(status=ApiResult.status.ERROR, message=f"Ошибка при удалении индекса: {str(e)}")
