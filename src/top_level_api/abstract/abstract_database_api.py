from abc import ABC, abstractmethod


class AbstractDatabaseAPI(ABC):

    @abstractmethod
    def create_table(self, table_name: str, table_struct: dict) -> None:
        """Создает новую таблицу в базе данных."""
        pass

    @abstractmethod
    def describe_table(self, table_name: str) -> dict:
        """Возвращает структуру таблицы."""
        pass

    @abstractmethod
    def drop_table(self, table_name: str) -> None:
        """Удаляет таблицу из базы данных."""
        pass

    @abstractmethod
    def show_tables(self) -> list:
        """Возвращает список всех таблиц в базе данных."""
        pass
