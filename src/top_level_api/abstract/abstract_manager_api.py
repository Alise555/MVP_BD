from abc import ABC, abstractmethod


class AbstractDBAPI(ABC):
    """
    Абстрактный класс для работы с БД (CRUD для Баз Данных).
    """
    @abstractmethod
    def create_database(self, db_name:str):
        pass

    @abstractmethod
    def update_database(self, old_db_name: str, new_db_name: str):
        pass

    @abstractmethod
    def drop_database(self, db_name:str):
        pass

    @abstractmethod
    def show_databases(self):
        pass

    @abstractmethod
    def use_database(self, db_name:str):
        pass

    @abstractmethod
    def get_current_db(self):
        pass
