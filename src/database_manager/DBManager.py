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
        self._databases = set()
        self._current_database = ""

    def create_database(self, database_name: str):
        """Создаёт новую базу данных.
        Args:
            database_name (str): Имя создаваемой базы данных.
            metadata (Dict): Метаданные для базы данных.
        """
        if database_name in self._databases:
            raise Exception("Db already created")
        result_create_folder = self._storage.create_folder(
            os.path.join(path, database_name)
        )
        if result_create_folder == Status.OK:
            self._databases.add(database_name)
            if self._databases:
                result_metadata = self._storage.update_metadata(self._databases, path)
            else:
                result_metadata = self._storage.create_metadata(self._databases, path)
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
        if database_name not in self._databases:
            raise Exception("Unknown db")
        result_delete_folder = self._storage.delete_folder(
            os.path.join(path, database_name)
        )
        if result_delete_folder == Status.OK:
            self._databases.remove(database_name)
            result_metadata = self._storage.update_metadata(self._databases, path)
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
        if old_database_name not in self._databases:
            raise Exception("Unknown db")
        result_rename_folder = self._storage.rename_folder(
            old_database_name, new_database_name
        )
        if result_rename_folder == Status.OK:
            self._databases.remove(old_database_name)
            self._databases.add(new_database_name)
            result_metadata = self._storage.update_metadata(self._databases, path)
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
        if database_name not in self._databases:
            raise Exception("Unknown db_name")
        result_metadata = self._storage.get_metadata(path)
        self._current_database = database_name

    def show_databases(self) -> List[str]:
        """Возвращает список всех баз данных."""
        result_metadata = self._storage.get_metadata(path)
        return list(self._databases)

    def current_database(self):
        """Возвращает имя текущей активной базы данных."""
        return self._current_database
