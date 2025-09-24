from abstract.base_db import BaseDB


class RelationalDB(BaseDB):

    def create_table(self, table_name: str, table_struct: dict) -> bool|Exception:
        """Создает новую таблицу в базе данных."""
        try:
            self._storage.create_folder(table_name)
            metadata = self._storage.create_metadata(table_struct)
            self._storage.create_data_file(table_name, metadata)
            return True
        except Exception as e:
            raise Exception(f"Error creating table {table_name}: {e}")

    def describe_table(self, table_name: str) -> dict:
        """Возвращает структуру таблицы."""
        try:
            res: dict = self._storage.get_metadata(table_name)
            return res
        except Exception as e:
            raise Exception(f"Error describing table {table_name}: {e}")

    def drop_table(self, table_name: str) -> bool:
        """Удаляет таблицу из базы данных."""
        try:
            self._storage.delete_data_file(table_name)
            self._storage.delete_metadata(table_name)
            self._storage.delete_folder(table_name)
            return True
        except Exception as e:
            raise Exception(f"Error dropping table {table_name}: {e}")

    def show_tables(self) -> list[str]:
        """Возвращает список всех таблиц в базе данных."""
        res: dict = self._storage.get_metadata()
        # Логика какая-то
        tables: list[str] = [res.keys()]
        return tables
