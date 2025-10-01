import json
from typing import Dict, List, Any, Tuple


class Storage:
    """Класс для работы с файловой системой"""
    
    def __init__(self, db_name: str, table_name: str):
        self.db_name = db_name
        self.table_name = table_name
    
    def update_metadata(self, metadata: Dict[str, Any]) -> None:
        """Обновляет метаданные таблицы (Table_INFO)"""
        print(f"Storage: Обновление метаданных для таблицы {self.table_name}")
        print(f"Метаданные: {metadata}")
        # Реальная логика записи в Table_INFO
    
    def update_data_file(self, data_file_path: str, data: Tuple[Dict[str, Any]]) -> None:
        """Обновляет файл с данными таблицы (Table_DATA)"""
        print(f"Storage: Обновление данных для таблицы {self.table_name}")
        print(f"Количество записей: {len(data)}")
        # Реальная логика записи в Table_DATA
    
    def load_metadata(self) -> Dict[str, Any]:
        """Загружает метаданные таблицы"""
        # Заглушка - в реальности загрузка из Table_INFO
        return {}
    
    def load_data(self) -> List[List[Any]]:
        """Загружает данные таблицы"""
        # Заглушка - в реальности загрузка из Table_DATA
        return []
    
    def insert_in_data_file(self, data_file_path: str, values: Dict[str, Any]) -> None:
        print(f"Storage: Вставка данных в таблицу {self.table_name}")

    def get_metadata(self, table_name: str) -> Dict[str, Any]:
        """Передает структуру таблицы
        Args:
            table_name (str): имя таблицы
        Returns:
            Dict[str, Any]: струтура таблицы
        """ 
        # Заглушка   
        return {}     
    
    def get_from_data_file(self, table_name: str) -> Tuple[Dict[str, Any]]:
        """Передает данные таблицы
        Args:
            table_name (str): имя таблицы
        Returns:
            Tuple[Dict[str, Any]]: данные таблицы
        """ 
        # Заглушка   
        return tuple()