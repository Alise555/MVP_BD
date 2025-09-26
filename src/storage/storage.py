class Storage:
    def create_folder(folder_name: str):
        """
        Создать папку с названием folder_name
        Args:
            folder_name(str): название папки
        """
        pass
    
    def delete_folder(folder_name: str):
        """
        Удалить папку с названием folder_name и все ее содержимое
        Args:
            folder_name(str): название папки
        """
        pass
    
    def rename_folder(folder_name: str, new_name: str):
        """
        Переименовать папку folder_name на new_name
        Args:
            folder_name(str): старое название папки
            new_name(str): новое название папки
        """
        pass
    
    def create_data_file(data_file_name: str, folder: str):
        """
        Создать data_file
        Args:
            datafile_name(str): название data_file
            folder(str): название папки, в которой создаем data_file
        """
        pass
    
    def insert_in_data_file(data_file: str, content: str):
        """
        Поместить в data_file новое содержимое content
        Args:
            data_file(str): название data_file
            content(str): содержимое, которое вставляем в data_file
        """
        pass
        
    def update_data_file(data_file: str, new_content: str, pos: int):
        """
        Обновить в datafile содержимое, находящееся на позиции 
        Args:
            datafile_name(str): название data_file
            new_content(str): новое содержимое, которое попадет в data_file
            pos(int): позиция обновляемого содержимого в data_file (в байтах)
        """
        pass
        
    def get_from_data_file(data_file: str):
        """
        Получить содержимое data_file
        Args:
            data_file(str): название data_file
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
        
    def delete_data_file(data_file: str):
        """
        Удалить data_file
        Args:
            data_file: название к файлу, который удаляем
        """
        pass
        
    def create_metadata(metadata_file: str):
        """
        Создать файл с метаданными
        Args:
            metadata_file: название файла, который создаем
        
        """
        pass
        
    def update_metadata(metadata_file: str):
        """
        Удалить файл с метаданными
        Args:
            metadata_file: название файла, который обновляем
        """
        pass
        
    def get_metadata(metadata_file: str):
        """
        Получить содержимое файла с метаданными
        Args:
            metadata_file: название файла, который читаем
        """
        pass
        
    def delete_metadata(metadata_file: str):
        """
        Удалить файл с метаданными
        Args:
            metadata_file: название файла, который удаляем
        """
        pass
        
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
        