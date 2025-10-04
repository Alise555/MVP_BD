import os

from typing import List
from enum_status import Status
from storage.storage import Storage
from config.config import path


class DBManager:
    """Класс для управления базами данных.
    Позволяет создавать, удалять, переименовывать и переключаться между базами данных.
    Использует внешнее хранилище для операций с папками и метаданными.
    """

    def __init__(self) -> None:
        """Инициализирует экземпляр DBManager.
        Args:
            storage (str): Объект хранилища.
        """
        self._storage = Storage()
        self._current_database = ""

    def create_database(self, database_name: str):
        """Создаёт новую базу данных.
        Args:
            database_name (str): Имя создаваемой базы данных.
            metadata (Dict): Метаданные для базы данных.
        """
        databases = set(self._get_databases()["databases"])
        if database_name in databases:
            raise Exception("Db already created")
        result_create_folder = self._storage.create_folder(
            os.path.join(path, database_name)
        )
        if result_create_folder == Status.OK:
            databases.add(database_name)
            if databases:
                result_metadata = self._storage.update_metadata(
                    self._form_metadata_dict(databases), path
                )
            else:
                result_metadata = self._storage.create_metadata(
                    self._form_metadata_dict(databases), path
                )
            if result_metadata == Status.OK:
                return Status.OK
            else:
                raise Exception("Broken metadata")
        else:
            raise Exception("Broken folder")

    def delete_database(self, database_name: str):
        """Удаляет базу данных.
        Args:
            database_name (str): Имя удаляемой базы данных.
        """
        databases = set(self._get_databases()["databases"])
        if database_name not in databases:
            raise Exception("Unknown db")
        result_delete_folder = self._storage.delete_folder(
            os.path.join(path, database_name)
        )
        if result_delete_folder == Status.OK:
            databases.remove(database_name)
            result_metadata = self._storage.update_metadata(
                self._form_metadata_dict(databases), path
            )
            if result_metadata == Status.OK:
                return Status.OK
            else:
                raise Exception("Broken metadata")
        else:
            raise Exception("Broken folder")

    def update_database(self, old_database_name: str, new_database_name: str):
        """Переименовывает базу данных.
        Args:
            old_database_name (str): Текущее имя базы данных.
            new_database_name (str): Новое имя базы данных.
        """
        databases = set(self._get_databases()["databases"])
        if old_database_name not in databases:
            raise Exception("Unknown db")
        result_rename_folder = self._storage.rename_folder(
            os.path.join(path, old_database_name), new_database_name
        )
        if result_rename_folder == Status.OK:
            databases.remove(old_database_name)
            databases.add(new_database_name)
            result_metadata = self._storage.update_metadata(
                self._form_metadata_dict(databases), path
            )
            if result_metadata == Status.OK:
                return Status.OK
            else:
                raise Exception("Broken metadata")
        else:
            raise Exception("Broken folder")

    def use_database(self, database_name: str):
        """Устанавливает активную базу данных.
        Args:
            database_name (str): Имя базы данных, которую нужно использовать.
        """
        databases = set(self._get_databases()["databases"])
        if database_name not in databases:
            raise Exception("Unknown db_name")
        self._current_database = database_name
        return Status.OK

    def show_databases(self) -> dict:
        """Возвращает список всех баз данных."""
        return self._get_databases()

    def current_database(self):
        """Возвращает имя текущей активной базы данных."""
        return self._current_database

    def _form_metadata_dict(self, databases: set) -> dict:
        """Формирует данные для метадата формата"""
        return {"databases": list(databases)}

    def _get_databases(self) -> dict:
        try:
            return self._storage.get_metadata(path)
        except FileNotFoundError:
            return {"databases": []}
