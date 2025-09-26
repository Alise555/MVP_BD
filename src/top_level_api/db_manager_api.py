from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from src.enum_status import Status
from abstract.abstract_manager_api import AbstractDBAPI


@dataclass
class ApiResult:
    status: Status
    message: str = ""


@dataclass
class ShowDataBases:
    status: Status
    databases: List[str]
    message: str = ""


class DBAPI(AbstractDBAPI):
    
    def __init__(self, data_root: str | Path = "./data"):
        self.data_root = Path(data_root).resolve()
        self.data_root.mkdir(parents=True, exist_ok=True)
        self.current_db: Optional[str] = None

    def create_database(self, name:str) -> ApiResult:
        return DBManager.create_db(name)
    
    def update_database(self, old_name:str, new_name:str) -> ApiResult:
        return DBManager.update_db(old_name, new_name)
        
    def delete_database(self, name:str) -> ApiResult:
        return DBManager.delete_db(name)
    
    def show_databases(self) -> ShowDataBases:
        return DBManager.show_database()
        
    def use_database(self, name:str) -> ApiResult:
        return DBManager.use_database(name)



# if __name__ == "__main__":
#     api = DBAPI("./data")

#     print(api.create_database("test1"))
#     print(api.show_databases())
#     print(api.use_database("test1"))
#     print(api.update_database("test1", "test2"))
#     print(api.show_databases())
#     print(api.delete_database("test2"))
#     print(api.show_databases())

