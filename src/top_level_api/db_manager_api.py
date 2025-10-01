from dataclasses import dataclass
from typing import List, Optional

from enum_status import Status
from top_level_api.abstract.abstract_manager_api import AbstractDBAPI


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
        db_manager=None,
    ):
        # self.data_root = Path(data_root).resolve()
        # self.data_root.mkdir(parents=True, exist_ok=True)
        self.current_db: Optional[str] = None
        self.db_manager = db_manager

    def create_database(self, db_name: str) -> ApiResult:
        """Создает базу данных."""
        try:
            result = self.db_manager.create_database(db_name)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(
                status=Status.ERROR, message=f"Ошибка в создание БД: {str(e)}"
            )

    def update_database(self, old_db_name: str, new_db_name: str) -> ApiResult:
        """Переименовывает базу данных."""
        try:
            result = self.db_manager.update_database(old_db_name, new_db_name)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(
                status=Status.ERROR, message=f"Ошибка в переименовании БД: {str(e)}"
            )

    def drop_database(self, db_name: str) -> ApiResult:
        """Удаляет базу данных."""
        try:
            result = self.db_manager.delete_database(db_name)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(
                status=Status.ERROR, message=f"Ошибка при удалении БД: {str(e)}"
            )

    def show_databases(self) -> ShowDataBases:
        """Возвращает список всех баз данных."""
        try:
            return self.db_manager.show_databases()
        except Exception as e:
            return ShowDataBases(
                status=Status.ERROR,
                databases=[],
                message=f"Ошибка при получении списка БД: {str(e)}",
            )

    def use_database(self, db_name: str) -> ApiResult:
        """Выбирает базу данных для работы."""
        try:
            result = self.db_manager.use_database(db_name)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(
                status=Status.ERROR, message=f"Ошибка при выборе БД: {str(e)}"
            )

    def get_current_db(self) -> ApiResult:
        """Возвращает текущую базу данных."""
        try:
            result = self.db_manager.get_current_db()
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(
                status=Status.ERROR,
                message=f"Ошибка при получении текущей БД: {str(e)}",
            )


# if __name__ == "__main__":
#     api = DBAPI("./data")

#     print(api.create_database("test1"))
#     print(api.show_databases())
#     print(api.use_database("test1"))
#     print(api.update_database("test1", "test2"))
#     print(api.show_databases())
#     print(api.delete_database("test2"))
#     print(api.show_databases())
