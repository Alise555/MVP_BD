from dataclasses import dataclass
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
    
    def __init__(
            self,
            # data_root: str | Path = "./data"
            db_manager
        ):
        # self.data_root = Path(data_root).resolve()
        # self.data_root.mkdir(parents=True, exist_ok=True)
        # self.current_db: Optional[str] = None
        self.db_manager = db_manager

    def create_database(self, name:str) -> ApiResult:
        """Создает базу данных."""
        try:
            return self.db_manager.create_db(name)
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка в создание БД: {str(e)}")

    def update_database(self, old_name:str, new_name:str) -> ApiResult:
        """Переименовывает базу данных."""
        try:
            return self.db_manager.update_db(old_name, new_name)
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка в переименовании БД: {str(e)}")
        
    def delete_database(self, name:str) -> ApiResult:
        """Удаляет базу данных."""
        try:
            return self.db_manager.delete_db(name)
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка при удалении БД: {str(e)}")
    
    def show_databases(self) -> ShowDataBases:
        """Возвращает список всех баз данных."""
        try:
            return self.db_manager.show_database()
        except Exception as e:
            return ShowDataBases(
                status=Status.ERROR,
                databases=[],
                message=f"Ошибка при получении списка БД: {str(e)}"
            )
        
    def use_database(self, name:str) -> ApiResult:
        """Выбирает базу данных для работы."""
        try:
            return self.db_manager.use_database(name)
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка при выборе БД: {str(e)}")



# if __name__ == "__main__":
#     api = DBAPI("./data")

#     print(api.create_database("test1"))
#     print(api.show_databases())
#     print(api.use_database("test1"))
#     print(api.update_database("test1", "test2"))
#     print(api.show_databases())
#     print(api.delete_database("test2"))
#     print(api.show_databases())

