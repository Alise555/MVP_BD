import os
import json


class Storage:
    def create_folder(folder_path: str):
        """
        Создать папку по пути folder_path
        Args:
            folder_path(str): путь к создаваемой папке
        """
        # if not dbname:
            
        pass
    
    def delete_folder(folder_path: str):
        """
        Удалить папку по пути folder_path и все ее содержимое
        Args:
            folder_path(str): путь к удаляемой папке
        """
        # os.rmtree(folder_name+parent_folder)
        # os.path.join()
        pass
    
    def rename_folder(folder_path: str, new_name: str):
        """
        Переименовать папку по пути folder_path на new_name
        Args:
            folder_path(str): путь к папке
            new_name(str): новое название папки
        """
        pass
    
    # Сигнатура методов, которые работают с data_file изменится, когда я начну их реализовывать!!!!!
    def create_data_file(data_file_path: str):
        """
        Создать data_file
        Args:
            data_file_path(str): путь к data_file
        """
        pass
    
    def insert_in_data_file(data_file_path: str, content: str):
        """
        Поместить в data_file новое содержимое content
        Args:
            data_file_path(str): путь к data_file
            content(str): содержимое, которое вставляем в data_file
        """
        pass
        
    def update_data_file(data_file: str, row_structure: str): # пока что стр, потом посмотрим, как лучше передавать
        """
        Обновить в datafile содержимое, находящееся на позиции 
        Args:
            datafile_name(str): название data_file
            new_content(str): новое содержимое, которое попадет в data_file
        """
        pass
        
    def get_from_data_file(data_file_path: str):
        """
        Получить содержимое data_file
        Args:
            data_file_path(str): путь к data_file
        """
        pass
        
    def delete_from_data_file(data_file: str, conditions: str):
        """
        Удалить из data_file содержимое, удовлетворяющее некоторым условиям (подумаем, как это сделать)
        Args: 
            data_file(str): название data_file
            conditions(str): условия, по которым удаляем
        """
        pass
        
    def delete_data_file(data_file_path: str):
        """
        Удалить data_file
        Args:
            data_file_path: путь к файлу, который удаляем
        """
        pass
        
    #================================================================================

    def create_metadata(metadata: dict, metadata_file_path: str):
        """
        Создать файл с метаданными.

        Args:
            metadata (dict): Словарь с метаданными.
            metadata_file_path (str): Путь к файлу с метаданными.
        """
        with open(metadata_file_path, "w") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
        
    def update_metadata(metadata: dict, metadata_file_path: str):
        """
        Обновить файл с метаданными

        Args:
            metadata (dict): Словарь с метаданными.
            metadata_file_path (str): Путь к файлу с метаданными.
        """
        with open(metadata_file_path, "w") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
        
    def get_metadata(metadata_file_path: str) -> dict:
        """
        Получить содержимое файла с метаданными.

        Args:
            metadata_file_path (str): Путь к файлу с метаданными.
        Returns:
            metadata (dict): Словарь с метаданными.
        """
        with open(metadata_file_path, "r") as f:
            metadata = json.load(f)

        return metadata
        
    def delete_metadata(metadata_file_path: str):
        """
        Удалить файл с метаданными
        Args:
            metadata_file_path (str): Путь к удаляемому файлу.
        """
        
        if os.path.exists(metadata_file_path):
            os.remove(metadata_file_path)

    #================================================================================

    def create_index_file(index_file: str, type: str):
        """
        Создать индекс файл
        Args:
            index_file: название файла, который создаем
        """
        pass
        
    def delete_index_file(index_file: str):
        """
        Получить содержимое файла с метаданными
        Args:
            index_file: название файла, который удаляем
        """
        pass
        
    def update_index_file(index_file: str):
        """
        Удалить файл с метаданными
        Args:
            index_file: название файла, который обновляем
        """
        pass
        