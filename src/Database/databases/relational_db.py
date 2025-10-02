from Database.abstract.base_db import BaseDB
from storage.storage import Storage
from config.config import path as base_url
import os


class RelationalDB(BaseDB):

    def __init__(self):
        self._storage = Storage()

    def create_table(
        self, table_name: str, table_struct: dict, db_name: str
    ) -> bool | Exception:
        """Создает таблицу в базе данных.

        Args:
            table_name (str): Имя таблицы
            table_struct (dict): Структура таблицы

        Raises:
            Exception: Если таблица уже существует или произошла ошибка при создании таблицы.

        Returns:
            bool | Exception: True если таблица создана успешно, иначе Exception.
        """
        try:
            db_path = self.get_db_path(db_name)
            # Путь до файла таблицы
            table_path = os.path.join(db_path, table_name)
            # Создаем директорию
            self._storage.create_folder(folder_path=table_path)
            tables_metadata: dict[str, list] = self.get_tables_metadata(db_name)
            # Создаем метадату
            self._storage.create_metadata(
                metadata=table_struct, metadata_file_path=table_path
            )

            # Создаем путь до файла с данными
            data_file_path = os.path.join(table_path)
            self._storage.create_data_file(data_file_path=data_file_path)
            tables_metadata["tables"].append(table_name)
            self.update_tables_metadata(db_name, tables_metadata)
            return True
        except Exception as e:
            raise Exception(f"Error creating table {table_name}: {e}")

    def describe_table(self, table_name: str, db_name: str) -> dict:
        """Возвращает метаданные таблицы.

        Args:
            table_name (str): Имя таблицы

        Raises:
            Exception: Если таблица не найдена или произошла ошибка при получении метаданных.

        Returns:
            dict: Метаданные таблицы.
        """

        try:
            db_path = self.get_db_path(db_name)
            # Путь до файла таблицы
            table_path = os.path.join(db_path, table_name)

            # Создаем путь до метадаты
            metadata_path = os.path.join(table_path)

            res: dict = self._storage.get_metadata(metadata_file_path=metadata_path)
            return res
        except Exception as e:
            raise Exception(f"Error describing table {table_name}: {e}")

    def drop_table(self, table_name: str, db_name: str) -> bool | Exception:
        """Удаляет таблицу из базы данных.

        Args:
            table_name (str): Имя таблицы

        Raises:
            Exception: Если таблица не найдена или произошла ошибка при удалении таблицы.

        Returns:
            bool | Exception: True если таблица удалена успешно, иначе Exception.
        """

        try:
            db_path = self.get_db_path(db_name)
            # Путь до файла таблицы
            table_path = os.path.join(db_path, table_name)
            # Удаляем директорию
            self._storage.delete_folder(folder_path=table_path)
            tables_metadata = self.get_tables_metadata(db_name)
            tables_metadata["tables"].remove(table_name)
            self.update_tables_metadata(db_name, tables_metadata)
            return True
        except Exception as e:
            raise Exception(f"Error dropping table {table_name}: {e}")

    def show_tables(self, db_name: str) -> list[str]:
        """Возвращает список всех таблиц в базе данных.

        Returns:
            list[str]: Список имен таблиц.
        """
        db_path = self.get_db_path(db_name)
        # Создает путь до метадаты базы данных

        # Получаем метадату базы данных
        res: dict = self._storage.get_metadata(metadata_file_path=db_path)

        # Забираем по ключу все таблицы в бд
        tables: list[str] = list(res["tables"])
        return tables

    def get_db_path(self, db_name: str) -> str:
        return os.path.join(base_url, db_name)

    def update_tables_metadata(self, db_name: str, metadata: dict):
        metadata_path = os.path.join(base_url, db_name)
        try:
            self._storage.update_metadata(metadata, metadata_path)
        except FileNotFoundError:
            self._storage.create_metadata(metadata, metadata_path)

    def get_tables_metadata(self, db_name: str) -> dict[str, list]:
        try:
            metadata_path = os.path.join(base_url, db_name)
            data = self._storage.get_metadata(metadata_path)
            return data
        except FileNotFoundError:
            return {"tables": []}
