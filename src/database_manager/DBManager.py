import asyncio
from typing import Any, Dict, List


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

    def create_database(self, database_name: str, metadata: Dict[str, Any]):
        """Создаёт новую базу данных.
        Args:
            database_name (str): Имя создаваемой базы данных.
            metadata (Dict): Метаданные для базы данных.
        """
        if database_name in self._databases:
            return "error"

        result_create_folder = self._storage.create_folder(database_name)
        result_create_metadata = self._storage.create_metadata(metadata)

        if result_create_folder == "OK" and result_create_metadata == "OK":
            self._databases.add(database_name)
            return "OK"
        else:
            return "ERROR"

    def delete_database(self, database_name: str):
        """Удаляет базу данных.
        Args:
            database_name (str): Имя удаляемой базы данных.
        """
        if database_name not in self._databases:
            return "error"
        result_delete_folder = self._storage.delete_folder(database_name)
        if result_delete_folder == "OK":
            self._databases.remove(database_name)
            return "OK"
        else:
            return "ERROR"

    def rename_database(self, old_database_name: str, new_database_name: str):
        """Переименовывает базу данных.
        Args:
            old_database_name (str): Текущее имя базы данных.
            new_database_name (str): Новое имя базы данных.
        """
        if old_database_name not in self._databases:
            return "error"
        result_rename_folder = self._storage.rename_folder(old_database_name, new_database_name)
        result_update_metadata = self._storage.update_metadata()
        if result_rename_folder == "OK" and result_update_metadata == "OK":
            self._databases.remove(old_database_name)
            self._databases.add(new_database_name)
            return "OK"
        else:
            return "ERROR"

    def use_database(self, database_name: str) -> None:
        """Устанавливает активную базу данных.
        Args:
            database_name (str): Имя базы данных, которую нужно использовать.
        """
        if database_name not in self._databases:
            return "error"
        self._current_database = database_name

    def show_databases(self) -> List[str]:
        """Возвращает список всех баз данных.
        """
        return list(self._databases)

    def current_database(self):
        """Возвращает имя текущей активной базы данных.
        """
        return self._current_database