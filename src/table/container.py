from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional


class Container(ABC):
    """
    Абстрактный базовый класс для контейнеров данных.
    """
    
    @abstractmethod
    def __init__(self, name: str):
        """
        Инициализация контейнера.
        
        Args:
            name (str): Имя контейнера
        """
        pass
    
    # @abstractmethod
    # def get_name(self) -> str:
    #     """
    #     Получить имя контейнера.
        
    #     Returns:
    #         str: Имя контейнера
    #     """
    #     pass
    
    # @abstractmethod
    # def get_size(self) -> int:
    #     """
    #     Получить размер контейнера (количество элементов/записей).
        
    #     Returns:
    #         int: Размер контейнера
    #     """
    #     pass
    
    # @abstractmethod
    # def is_empty(self) -> bool:
    #     """
    #     Проверить, пуст ли контейнер.
        
    #     Returns:
    #         bool: True если контейнер пуст
    #     """
    #     pass