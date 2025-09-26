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
        return self.database.create_table(table_name, table_struct)
    
    def describe_table(self, table_name: str) -> Dict[str, Any]:
        return self.database.describe_table(table_name)
    
    def drop_table(self, table_name: str) -> ApiResult:
        return self.database.drop_table(table_name)
    
    def show_tables(self) -> List[str]:
        return self.database.show_tables()
