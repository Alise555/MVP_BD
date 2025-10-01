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

    def create_table(self, table_name:str, table_struct:Dict[str, Any]) -> ApiResult:
        """Создаёт таблицу."""
        try:
            result = self.database.create_table(table_name, table_struct)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка при создании таблицы: {str(e)}")
    
    def describe_table(self, db_name: str):
        """Возвращает структуру таблицы."""
        try:
            result = self.database.describe_table(db_name)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка в структуре таблицы: {str(e)}")
    
    def drop_table(self, table_name: str) -> ApiResult:
        """Удаляет таблицу."""
        try:
            result = self.database.drop_table(table_name)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка при удалении таблицы: {str(e)}")
    
    def show_tables(self) -> List[str]:
        """Возвращает список имён таблиц."""
        try:
            result = self.database.show_tables()
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка в возврате списка таблиц: {str(e)}")
    
    def truncate_table(self, table_name:str) -> ApiResult:
        """Очищает таблицу."""
        try:
            result = self.database.truncate_table(table_name)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка при очистке таблицы: {str(e)}")
