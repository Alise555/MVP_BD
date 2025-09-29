# Storage.create_folder(self, 'new_folder', '')

class Storage:
    def create_folder(self, folder_path: str):
        """
        Создать папку по пути folder_path
        Args:
            folder_path(self, str): путь к создаваемой папке
        """
        # if not dbname:
            
        pass
    
    def delete_folder(self, folder_path: str):
        """
        Удалить папку по пути folder_path и все ее содержимое
        Args:
            folder_path(self, str): путь к удаляемой папке
        """
        # os.rmtree(self, folder_name+parent_folder)
        # os.path.join(self, )
        pass
    
    def rename_folder(self, folder_path: str, new_name: str):
        """
        Переименовать папку по пути folder_path на new_name
        Args:
            folder_path(self, str): путь к папке
            new_name(self, str): новое название папки
        """
        pass
    
    # Сигнатура методов, которые работают с data_file изменится, когда я начну их реализовывать!!!!!
    def create_data_file(self, data_file_path: str):
        """
        Создать data_file
        Args:
            data_file_path(self, str): путь к data_file
        """
        pass
    
    def insert_in_data_file(self, data_file_path: str, content: str):
        """
        Поместить в data_file новое содержимое content (self, вставляем данные в конец data_file)
        Args:
            data_file_path(self, str): путь к data_file
            content(self, str): содержимое, которое вставляем в data_file
        """
        pass
        
    def update_data_file(self, data_file_path: str, new_content: str): # пока что стр, потом посмотрим, как лучше передавать
        """
        Перезаписать содержимое data_file новым содержимым new_content
        Args:
            datafile_name(self, str): путь к обновляемому data_file
            new_content(self, str): новое содержимое, которое попадет перезапишет data_file
        """
        pass
        
    def get_from_data_file(self, data_file_path: str):
        """
        Получить содержимое data_file
        Args:
            data_file_path(self, str): путь к data_file
        """
        pass
        
    def delete_data_file(self, data_file_path: str):
        """
        Удалить data_file
        Args:
            data_file_path: путь к файлу, который удаляем
        """
        pass
        
    def create_metadata(self, metadata: dict, metadata_file_path: str):
        """
        Создать файл с метаданными
        Args:
            metadata_file: название файла, который создаем
        
        """
        pass
        
    def update_metadata(self, metadata: dict, metadata_file_path: str):
        """
        Обновить файл с метаданными
        Args:
            metadata_file_path: название файла, который обновляем
        """
        pass
        
    def get_metadata(self, metadata_file_path: str) -> dict:
        """
        Получить содержимое файла с метаданными
        Args:
            metadata_file_path: путь к файлу с метаданными
        """
        pass
        
    def delete_metadata(self, metadata_file_path: str):
        """
        Удалить файл с метаданными
        Args:
            metadata_file_path: путь к файлу, который удаляем
        """
        pass
        
    def create_index_file(self, index_file: str, type: str):
        """
        Создать индекс файл
        Args:
            index_file: название файла, который создаем
        """
        pass
        
    def delete_index_file(self, index_file: str):
        """
        Получить содержимое файла с метаданными
        Args:
            index_file: название файла, который удаляем
        """
        pass
        
    def update_index_file(self, index_file: str):
        """
        Удалить файл с метаданными
        Args:
            index_file: название файла, который обновляем
        """
        pass
        