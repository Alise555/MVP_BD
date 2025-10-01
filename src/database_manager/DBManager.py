from typing import List
from enum_status import Status


class DBManager:
    """Класс для управления базами данных.
    Позволяет создавать, удалять, переименовывать и переключаться между базами данных.
    Использует внешнее хранилище для операций с папками и метаданными.
    """

    def __init__(self, storage: str) -> None:
        """Инициализирует экземпляр DBManager.
        Args:
            storage (str): Объект хранилища.
        """
        self._storage = storage
        self._databases = set()
        self._current_database = ""

    def create_db(self, database_name: str):
        """Создаёт новую базу данных.
        Args:
            database_name (str): Имя создаваемой базы данных.
            metadata (Dict): Метаданные для базы данных.
        """
        if database_name in self._databases:
            return Status.ERROR
        result_create_folder = self._storage.create_folder(database_name)
        if result_create_folder == Status.OK:
            self._databases.add(database_name)
            if self._databases:
                result_metadata = self._storage.update_metadata(self._databases, "/")
            else:
                result_metadata = self._storage.create_metadata(self._databases, "/")
            if result_metadata == Status.OK:
                return Status.OK
            else:
                return Status.ERROR
        else:
            return Status.ERROR

    def delete_db(self, database_name: str):
        """Удаляет базу данных.
        Args:
            database_name (str): Имя удаляемой базы данных.
        """
        if database_name not in self._databases:
            return Status.ERROR
        result_delete_folder = self._storage.delete_folder(database_name)
        if result_delete_folder == Status.OK:
            self._databases.remove(database_name)
            result_metadata = self._storage.update_metadata(self._databases, "/")
            if result_metadata == Status.OK:
                return Status.OK
            else:
                return Status.ERROR
        else:
            return Status.ERROR

    def update_db(self, old_database_name: str, new_database_name: str):
        """Переименовывает базу данных.
        Args:
            old_database_name (str): Текущее имя базы данных.
            new_database_name (str): Новое имя базы данных.
        """
        if old_database_name not in self._databases:
            return Status.ERROR
        result_rename_folder = self._storage.rename_folder(old_database_name, new_database_name)
        if result_rename_folder == Status.OK:
            self._databases.remove(old_database_name)
            self._databases.add(new_database_name)
            result_metadata = self._storage.update_metadata(self._databases, "/")
            if result_metadata == Status.OK:
                return Status.OK
            else:
                return Status.ERROR
        else:
            return Status.ERROR

    def use_database(self, database_name: str):
        """Устанавливает активную базу данных.
        Args:
            database_name (str): Имя базы данных, которую нужно использовать.
        """
        if database_name not in self._databases:
            return Status.ERROR
        result_metadata = self._storage.get_metadata("/")
        self._current_database = database_name

    def show_database(self) -> List[str]:
        """Возвращает список всех баз данных.
        """
        result_metadata = self._storage.get_metadata("/")
        return list(self._databases)

    def current_database(self):
        """Возвращает имя текущей активной базы данных.
        """
        return self._current_database
