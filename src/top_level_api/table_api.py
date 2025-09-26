from typing import Any, Dict
from database_api import ApiResult
from abstract.abstract_table_api import AbstractTableAPI


class TableAPI(AbstractTableAPI):
    """Top-level API для работы с колонками таблицы и индексами."""
    
    def __init__(self, table):
        self.table = table
    
    def add_column(self, column_name: str, column_type: str) -> ApiResult:
        """Добавляет колонку - делегирует низкоуровневому Table"""
        return self.table.add_column(column_name, column_type)
    
    def modify_column(self, column_name: str, new_definition: Dict[str, Any]) -> ApiResult:
        """Изменяет колонку - делегирует низкоуровневому Table"""
        return self.table.modify_column(column_name, new_definition)
    
    def drop_column(self, column_name: str) -> ApiResult:
        """Удаляет колонку - делегирует низкоуровневому Table"""
        return self.table.drop_column(column_name)
    
    def create_index(self, index_name, index_sturct) -> ApiResult:
        """Создает индекс - делегирует низкоуровневому Table"""
        return self.table.create_index(index_name, index_sturct)
    
    def drop_index(self, index_name) -> ApiResult:
        """Удаляет индекс - делегирует низкоуровневому Table"""
        return self.table.drop_index.drop_index(index_name)