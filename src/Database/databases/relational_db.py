from abstract.base_db import BaseDB
import os


class RelationalDB(BaseDB):

    def __init__(self, cur_db: str, base_url):
        self.db_path = os.path.join(base_url, cur_db)

    def create_table(self, table_name: str, table_struct: dict) -> bool | Exception:
        """Создает таблицу в базе данных.

        Args:
            table_name (str): Имя таблицы
            table_struct (dict): Структура таблицы

        Raises:
            Exception: Если таблица уже существует или произошла ошибка при создании таблицы.

        Returns:
            bool | Exception: True если таблица создана успешно, иначе Exception.
        """
        try:
            # Путь до файла таблицы
            table_path = os.path.join(self.db_path, table_name)

            # Создаем директорию
            self._storage.create_folder(folder_path=table_path)

            # Создаем путь до метадаты
            metadata_path = os.path.join(table_path,"metadata")
            # Создаем метадату
            self._storage.create_metadata(metadata=table_struct, metadata_file_path=metadata_path)

            # Создаем путь до файла с данными
            data_file_path = os.path.join(table_path, "data")
            self._storage.create_data_file(data_file_path=data_file_path)
            return True
        except Exception as e:
            raise Exception(f"Error creating table {table_name}: {e}")

    def describe_table(self, table_name: str) -> dict:
        """Возвращает метаданные таблицы.

        Args:
            table_name (str): Имя таблицы

        Raises:
            Exception: Если таблица не найдена или произошла ошибка при получении метаданных.

        Returns:
            dict: Метаданные таблицы.
        """

        try:
            # Путь до файла таблицы
            table_path = os.path.join(self.db_path, table_name)

            # Создаем путь до метадаты
            metadata_path = os.path.join(table_path,"metadata")

            res: dict = self._storage.get_metadata(metadata_file_path=metadata_path)
            return res
        except Exception as e:
            raise Exception(f"Error describing table {table_name}: {e}")

    def drop_table(self, table_name: str) -> bool | Exception:
        """Удаляет таблицу из базы данных.

        Args:
            table_name (str): Имя таблицы

        Raises:
            Exception: Если таблица не найдена или произошла ошибка при удалении таблицы.

        Returns:
            bool | Exception: True если таблица удалена успешно, иначе Exception.
        """

        try:
            # Путь до файла таблицы
            table_path = os.path.join(self.db_path, table_name)

            # Удаляем директорию
            self._storage.delete_folder(folder_path=table_path)
            return True
        except Exception as e:
            raise Exception(f"Error dropping table {table_name}: {e}")

    def show_tables(self) -> list[str]:
        """Возвращает список всех таблиц в базе данных.

        Returns:
            list[str]: Список имен таблиц.
        """

        # Создает путь до метадаты базы данных
        db_metadata_path=os.join(self.db_path,"metadata")

        # Получаем метадату базы данных
        res: dict = self._storage.get_metadata(metadata_file_path=db_metadata_path)

        # Забираем по ключу все таблицы в бд
        tables: list[str] = res["tables"]
        return tables
