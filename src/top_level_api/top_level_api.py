from dataclasses import dataclass
from typing import Any

from enum_status import Status
from Database.databases.relational_db import RelationalDB
from database_manager.DBManager import DBManager
from table.table import Table


@dataclass
class ApiResult:
    status: Status
    message: str = ""


@dataclass
class ShowDataBases:
    status: Status
    databases: list[str]
    message: str = ""


class TopLevelApi:
    def __init__(self):
        self.database = RelationalDB()
        self.db_manager = DBManager()

    #  self.table = Table()

    def create_table(self, table_name: str, table_struct: dict[str, Any]) -> ApiResult:
        """Создаёт таблицу."""
        try:
            result = self.database.create_table(
                table_name, table_struct, self.db_manager.current_database()
            )
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(
                status=Status.ERROR, message=f"Ошибка при создании таблицы: {str(e)}"
            )

    def describe_table(self, table_name: str):
        """Возвращает структуру таблицы."""
        try:
            result = self.database.describe_table(
                table_name, self.db_manager.current_database()
            )
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(
                status=Status.ERROR, message=f"Ошибка в структуре таблицы: {str(e)}"
            )

    def drop_table(self, table_name: str) -> ApiResult:
        """Удаляет таблицу."""
        try:
            result = self.database.drop_table(
                table_name, self.db_manager.current_database()
            )
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(
                status=Status.ERROR, message=f"Ошибка при удалении таблицы: {str(e)}"
            )

    def show_tables(self) -> list[str]:
        """Возвращает список имён таблиц."""
        try:
            result = self.database.show_tables(self.db_manager.current_database())
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(
                status=Status.ERROR,
                message=f"Ошибка в возврате списка таблиц: {str(e)}",
            )

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
            result = self.db_manager.current_database()
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(
                status=Status.ERROR,
                message=f"Ошибка при получении текущей БД: {str(e)}",
            )

    def add_column(self, table_name: str, column_data: dict) -> ApiResult:
        """Добавляет колонку - делегирует низкоуровневому Table"""
        try:
            result = self.table.add_column(table_name, column_data)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(
                status=Status.ERROR,
                message=f"Ошибка при добавлении колонки: {str(e)}",
            )

    def modify_column(
        self, table_name: str, column_name: str, column_data: dict
    ) -> ApiResult:
        """Изменяет колонку - делегирует низкоуровневому Table"""
        try:
            return self.table.modify_column(table_name, column_name, column_data)
        except Exception as e:
            return ApiResult(
                status=Status.ERROR,
                message=f"Ошибка при изменении колонки: {str(e)}",
            )

    def drop_column(self, table_name: str, column_name: str) -> ApiResult:
        """Удаляет колонку - делегирует низкоуровневому Table"""
        try:
            return self.table.drop_column(table_name, column_name)
        except Exception as e:
            return ApiResult(
                status=Status.ERROR,
                message=f"Ошибка при удалении колонки: {str(e)}",
            )

    def create_index(
        self, table_name: str, index_name: str, index_struct: dict
    ) -> ApiResult:
        """Создает индекс - делегирует низкоуровневому Table"""
        try:
            result = self.table.create_index(table_name, index_name, index_struct)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(
                status=Status.ERROR,
                message=f"Ошибка при создании индекса: {str(e)}",
            )

    def drop_index(self, table_name: str, index_name: str) -> ApiResult:
        """Удаляет индекс - делегирует низкоуровневому Table"""
        try:
            result = self.table.drop_index(table_name, index_name)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(
                status=Status.ERROR,
                message=f"Ошибка при удалении индекса: {str(e)}",
            )

    def insert(self, table_name: str, fields: tuple, values: list[Any]) -> ApiResult:
        """Вставляет запись - делегирует низкоуровневому Table"""
        try:
            result = self.table.insert(table_name, fields, values)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(
                status=Status.ERROR, message=f"Ошибка при вставке данных: {str(e)}"
            )

    def select(self, fields: tuple, table_name: str, filtered: tuple = None):
        """Выбирает записи - делегирует низкоуровневому Table"""
        try:
            result = self.table.select_from(fields, table_name, filtered)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(
                status=Status.ERROR, message=f"Ошибка при выборке данных: {str(e)}"
            )

    def update(
        self, table_name: str, fields: dict[str, Any], filtered: tuple = None
    ) -> ApiResult:
        """Обновляет записи - делегирует низкоуровневому Table"""
        try:
            result = self.table.update(table_name, fields, filtered)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(
                status=Status.ERROR, message=f"Ошибка при обновлении данных: {str(e)}"
            )

    def delete_from(self, table_name: str, filtered: tuple = None) -> ApiResult:
        """Удаляет записи - делегирует низкоуровневому Table"""
        try:
            result = self.table.delete_from(table_name, filtered)
            return ApiResult(status=Status.OK, message=result)
        except Exception as e:
            return ApiResult(
                status=Status.ERROR, message=f"Ошибка при удалении данных: {str(e)}"
            )
