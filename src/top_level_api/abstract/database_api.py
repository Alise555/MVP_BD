from abc import ABC, abstractmethod


class AbstractDBAPI(ABC):
    """
    Абстрактный класс для работы с БД (CRUD для Баз Данных).
    """
    @abstractmethod
    def create_database(self, name:str):
        pass

    @abstractmethod
    def update_database(self, old_name:str, new_name:str):
        pass

    @abstractmethod
    def delete_database(self, name:str):
        pass

    @abstractmethod
    def show_databases(self):
        pass

    @abstractmethod
    def use_database(self, name:str):
        pass
