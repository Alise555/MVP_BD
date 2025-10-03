from typing import Tuple, Dict, Any, List
import os
import json
import pickle
import shutil

from enum_status import Status
from config.config import metadata_name, data_name, offset_name


class Storage:
    def create_folder(self, folder_path: str):
        """
        Создать папку по пути folder_path
        Args:
            folder_path(str): путь к создаваемой папке
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            return Status.OK
        return Status.ERROR

    def delete_folder(self, folder_path: str):
        """
        Удалить папку по пути folder_path и все ее содержимое
        Args:
            folder_path(str): путь к удаляемой папке
        """
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path, ignore_errors=True)
            return Status.OK
        return Status.ERROR

    def rename_folder(self, folder_path: str, new_name: str):
        """
        Переименовать папку по пути folder_path на new_name
        Args:
            folder_path(str): путь к папке
            new_name(str): новое название папки
        """
        if os.path.exists(folder_path):
            base_dir = os.path.dirname(folder_path)
            new_path = os.path.join(base_dir, new_name)
            os.rename(folder_path, new_path)
            return Status.OK
        return Status.ERROR

    def create_data_file(self, data_file_path: str):
        """
        Создать data_file
        Args:
            data_file_path(str): путь к data_file
        """
        data_path = os.path.join(data_file_path, data_name)
        if os.path.exists(data_path):
            return Status.ERROR
        with open(data_path, "w"):
            pass
        return Status.OK

    def insert_in_data_file(self, data_file_path: str, content: Dict[str, Any]):
        """
        Поместить в data_file новое содержимое content (вставляем данные в конец data_file)
        Args:
            data_file_path(str): путь к data_file
            content(str): содержимое, которое вставляем в data_file
        """

        with open(data_file_path, "ab") as f:
            to_dump = list(content.values())
            pickle.dump(to_dump, f)
        return Status.OK

    def update_data_file(self, data_file_path: str, new_content: List[List[Any]]):
        """
        Перезаписать содержимое data_file новым содержимым new_content
        Args:
            data_file_path(str): путь к обновляемому data_file
            new_content(str): новое содержимое, которое попадет перезапишет data_file
        """
        with open(data_file_path, "wb") as f:
            for row in new_content:
                pickle.dump(row, f)
        return Status.OK

    def get_from_data_file(self, data_file_path: str) -> List[List[Any]]:
        """
        Получить содержимое data_file
        Args:
            data_file_path(str): путь к data_file
        """
        # pickle для каждого insert создает новую pickle-последовательность. поэтому либо здесь код будет раздутый,
        # либо в insert придется каждый раз заново файл читать. пока что так оставим (хотя меня бесит что нужно лишние байты хранить)
        rows = []
        data_path = os.path.join(data_file_path, data_name)
        with open(data_path, "rb") as f:
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
        data_path = os.path.join(data_file_path, data_name)
        if os.path.exists(data_path):
            os.remove(data_path)
            return Status.OK
        return Status.ERROR

    def create_metadata(self, metadata: dict, metadata_file_path: str):
        """
        Создать файл с метаданными.

        Args:
            metadata (dict): Словарь с метаданными.
            metadata_file_path (str): Путь к файлу с метаданными.

        """
        metadata_file_path = os.path.join(metadata_file_path, metadata_name)
        with open(metadata_file_path, "w") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
        return Status.OK

    def update_metadata(self, metadata: dict, metadata_file_path: str):
        """
        Обновить файл с метаданными

        Args:
            metadata (dict): Словарь с метаданными.
            metadata_file_path (str): Путь к файлу с метаданными.
        """
        metadata_file_path = os.path.join(metadata_file_path, metadata_name)
        with open(metadata_file_path, "w") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
        return Status.OK

    def get_metadata(self, metadata_file_path: str) -> dict:
        """
        Получить содержимое файла с метаданными.

        Args:
            metadata_file_path (str): Путь к файлу с метаданными.
        Returns:
            metadata (dict): Словарь с метаданными.

        """
        metadata_file_path = os.path.join(metadata_file_path, metadata_name)
        with open(metadata_file_path, "r") as f:
            metadata = json.load(f)

        return metadata

    def delete_metadata(self, metadata_file_path: str):
        """
        Удалить файл с метаданными
        Args:

            metadata_file_path(str): путь к файлу, который удаляем
        """
        metadata_file_path = os.path.join(metadata_file_path, metadata_name)
        if os.path.exists(metadata_file_path):
            os.remove(metadata_file_path)
            return Status.OK

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

    def write_data(self, data: list[dict], table_path: str):
        data_path = os.path.join(table_path, data_name)
        offsets = self.read_offsets(table_path)
        with open(data_path, "ab") as f:
            for item in data:
                offsets.append(f.tell())
                pickle.dump(item, f)
            self.write_offsets(offsets, table_path)

    def write_offsets(self, offsets: list[int], table_path: str):
        offset_path = os.path.join(table_path, offset_name)
        with open(offset_path, "w") as f:
            data = {"offsets": offsets}
            json.dump(data, f)

    def read_offsets(self, table_path: str):
        try:
            offset_path = os.path.join(table_path, offset_name)
            with open(offset_path, "r") as f:
                return json.load(f)["offsets"]
        except FileNotFoundError:
            return []
