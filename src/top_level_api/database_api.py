from dataclasses import dataclass
from typing import Any, Dict, List

from src.enum_status import Status
from abstract.abstract_database_api import AbstractDatabaseAPI


@dataclass
class ApiResult:
    status: Status
    message: str = ""


class DatabaseAPI(AbstractDatabaseAPI):
    """Top-level API для работы с таблицами"""

    def __init__(self, database):
        self.database = database

    def create_table(self, table_name:str, table_struct:dict) -> ApiResult:
        """Создаёт таблицу."""
        try:
            return self.database.create_table(table_name, table_struct)
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка при создании таблицы: {str(e)}")
    
    def describe_table(self, table_name: str) -> Dict[str, Any]:
        """Возвращает структуру таблицы."""
        try:
            result = self.database.describe_table(table_name)
            return result if result is not None else {}
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка в структуре таблицы: {str(e)}")
    
    def drop_table(self, table_name: str) -> ApiResult:
        """Удаляет таблицу."""
        try:
            return self.database.drop_table(table_name)
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка при удалении таблицы: {str(e)}")
    
    def show_tables(self) -> List[str]:
        """Возвращает список имён таблиц."""
        try:
            result = self.database.show_tables()
            return result if result is not None else []
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка в возврате списка таблиц: {str(e)}")
