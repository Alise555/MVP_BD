import os
from typing import Tuple, Dict, Any, List
import json
import pickle


class Storage:
    def create_folder(self, folder_path: str):
        """
        Создать папку по пути folder_path
        Args:
            folder_path(str): путь к создаваемой папке
        """
        pass
    
    def delete_folder(self, folder_path: str):
        """
        Удалить папку по пути folder_path и все ее содержимое
        Args:
            folder_path(str): путь к удаляемой папке
        """
        pass
    
    def rename_folder(self, folder_path: str, new_name: str):
        """
        Переименовать папку по пути folder_path на new_name
        Args:
            folder_path(str): путь к папке
            new_name(str): новое название папки
        """
        pass
    
    def create_data_file(self, data_file_path: str):
        """
        Создать data_file
        Args:
            data_file_path(str): путь к data_file
        """
        if os.path.exists(data_file_path):
            return 
        with open(data_file_path, 'w'):
            pass
    
    def insert_in_data_file(self, data_file_path: str, content: Dict[str, Any]):
        """
        Поместить в data_file новое содержимое content (вставляем данные в конец data_file)
        Args:
            data_file_path(str): путь к data_file
            content(str): содержимое, которое вставляем в data_file
        """
        with open(data_file_path, 'ab') as f:
            to_dump = list(content.values())
            pickle.dump(to_dump, f)

    def update_data_file(self, data_file_path: str, new_content: List[List[Any]]):
        """
        Перезаписать содержимое data_file новым содержимым new_content
        Args:
            data_file_path(str): путь к обновляемому data_file
            new_content(str): новое содержимое, которое попадет перезапишет data_file
        """
        with open(data_file_path, 'wb') as f:
            for row in new_content:
                pickle.dump(row, f)
        

    def get_from_data_file(self, data_file_path: str) -> List[List[Any]]:
        """
        Получить содержимое data_file
        Args:
            data_file_path(str): путь к data_file
        """
        # pickle для каждого insert создает новую pickle-последовательность. поэтому либо здесь код будет раздутый,
        # либо в insert придется каждый раз заново файл читать. пока что так оставим (хотя меня бесит что нужно лишние байты хранить)
        rows = []
        with open(data_file_path, 'rb') as f:
            try:
                while True:
                    row = pickle.load(f)
                    rows.append(row)
            except EOFError:
                pass
        return rows
        
    def delete_data_file(self, data_file_path: str):
        """
        Удалить data_file
        Args:
            data_file_path(str): путь к файлу, который удаляем
        """
        if os.path.exists(data_file_path):
            os.remove(data_file_path)
        
    def create_metadata(self, metadata: dict, metadata_file_path: str):
        """
        Создать файл с метаданными
        Args:
            metadata_file(str): название файла, который создаем
        
        """
        pass
        
    def update_metadata(self, metadata: dict, metadata_file_path: str):
        """
        Обновить файл с метаданными
        Args:
            metadata_file_path(str): название файла, который обновляем
        """
        pass
        
    def get_metadata(self, metadata_file_path: str) -> dict:
        """
        Получить содержимое файла с метаданными
        Args:
            metadata_file_path(str): путь к файлу с метаданными
        """
        pass
        
    def delete_metadata(self, metadata_file_path: str):
        """
        Удалить файл с метаданными
        Args:
            metadata_file_path(str): путь к файлу, который удаляем
        """
        pass
        
    def create_index_file(self, index_file: str, type: str):
        """
        Создать индекс файл
        Args:
            index_file(str): название файла, который создаем
        """
        pass
        
    def delete_index_file(self, index_file: str):
        """
        Получить содержимое файла с метаданными
        Args:
            index_file(str): название файла, который удаляем
        """
        pass
        
    def update_index_file(self, index_file: str):
        """
        Удалить файл с метаданными
        Args:
            index_file(str): название файла, который обновляем
        """
        pass
