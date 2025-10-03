import os
import sys

from table.table import Table
from storage.storage import Storage


class TopLevelApi:
    current_db = "default_db"
    tables = {}

    def get_current_db(self):  # pragma: no cover
        return self.current_db

    def create_database(self, db_name: str):
        storage = Storage()
        storage.create_folder(db_name)
        return f"create database <{db_name}> OK"

    def update_database(self, old_db_name: str, new_db_name: str):
        return f"update database <{old_db_name}> -> <{new_db_name}> OK"

    def drop_database(self, db_name: str):
        storage = Storage()
        storage.delete_folder(db_name)
        return f"drop database <{db_name}> OK"

    def show_databases(self):
        items = os.listdir(".")
        databases = [item for item in items if os.path.isdir(item) and not item.startwith(".")]
        return "\n".join(databases) if databases else "No databases"

    def use_database(self, db_name: str):
        self.current_db = db_name
        return f"use database <{self.current_db}> OK"

    def show_tables(self):
        if not os.path.exists(self.current_db):
            return "No tables"
        items = os.listdir(self.current_db)
        tables = []
        for item in items:
            if item.endswith('_metadata.json'):
                table_name = item.replace('_metadata.json', '')
                tables.append(table_name)
        return "\n".join(tables) if tables else "No tables"

    def create_table(self, table_name: str, table_struct: dict):
        try:
            # Создаем реальную таблицу
            table = Table(table_name, self.current_db)
            
            # Добавляем колонки из структуры
            for column_name, data_type in table_struct.items():
                if "class" in str(data_type):
                    data_type = str(data_type).split("'")[1]
                table.add_column({column_name: data_type})
        
            self.tables[table_name] = table
            
            return f"create table <{table_name}> OK\nstruct {table_struct}"
        except Exception as e:
            return f"Error creating table: {e}"

    def describe_table(self, table_name: str):
        try:
            if table_name in self.tables:
                table = self.tables[table_name]
            else:
                # Загружаем существующую таблицу
                table = Table(table_name, self.current_db)
                self.tables[table_name] = table
            
            # Форматируем вывод структуры
            result = f"<{table_name}>\n"
            for column, data_type in table.columns_metadata.items():
                result += f"{column}: {data_type}\n"
            return result.strip()
        except Exception as e:
            return f"Error describing table: {e}"

    def drop_table(self, table_name: str):
        try:
            if table_name in self.tables:
                del self.tables[table_name]
            
            # Удаляем файлы таблицы
            storage = Storage()
            metadata_path = f"{self.current_db}/{table_name}_metadata.json"
            data_path = f"{self.current_db}/{table_name}_data.pkl"
            
            storage.delete_metadata(metadata_path)
            storage.delete_data_file(data_path)
            
            return f"drop table <{table_name}> OK"
        except Exception as e:
            return f"Error dropping table: {e}"

    def truncate_table(self, table_name: str):
        try:
            if table_name in self.tables:
                table = self.tables[table_name]
                table.data = []  # Очищаем данные
                
                # Сохраняем пустые данные
                data_path = f"{self.current_db}/{table_name}_data.pkl"
                table.storage.update_data_file([], data_path)
            
            return f"truncate table <{table_name}> OK"
        except Exception as e:
            return f"Error truncating table: {e}"


    def add_column(self, table_name: str, column_data: dict):
        try:
            if table_name in self.tables:
                table = self.tables[table_name]
            else:
                table = Table(table_name, self.current_db)
                self.tables[table_name] = table
            
            success = table.add_column(column_data)
            if success:
                return f"alter table <{table_name}> add column {column_data} OK"
            else:
                return f"Error adding column to table {table_name}"
        except Exception as e:
            return f"Error adding column: {e}"

    def drop_column(self, table_name: str, column_name: str):
        try:
            if table_name in self.tables:
                table = self.tables[table_name]
            else:
                table = Table(table_name, self.current_db)
                self.tables[table_name] = table
            
            success = table.drop_column(column_name)
            if success:
                return f"alter table <{table_name}> drop column {column_name} OK"
            else:
                return f"Error dropping column from table {table_name}"
        except Exception as e:
            return f"Error dropping column: {e}"

    def modify_column(self, table_name: str, old_column_name: str, column_data: dict):
        try:
            if table_name in self.tables:
                table = self.tables[table_name]
            else:
                table = Table(table_name, self.current_db)
                self.tables[table_name] = table
            
            success = table.modify_column(old_column_name, column_data)
            if success:
                return f"alter table <{table_name}> modify column <{old_column_name}> -> <{column_data}> OK"
            else:
                return f"Error modifying column in table {table_name}"
        except Exception as e:
            return f"Error modifying column: {e}"

    def select_from(self, fields: tuple, table_name: str, filtered: tuple = None):
        if fields[0] == "*":
            fields = "ALL"
        if not filtered:
            return f"select {fields} from {table_name}"
        if filtered:
            return f"select {fields} from {table_name} where {filtered}"

    def delete_from(self, table_name: str, filtered: tuple = None):
        if filtered:
            return f"delete from {table_name} where {filtered}"
        else:
            return f"delete from {table_name}"

    def update(
        self,
        table_name: str,
        fields: dict,
        filtered: tuple = None,
    ):
        if filtered:
            return f"update {table_name} set {fields} where {filtered}"
        else:
            return f"update {table_name} set {fields}"

    def insert(self, table_name: str, fields: tuple, values: list):
        result_str = "" + f"insert into {table_name} {fields} "
        values = [str(item) for item in values if item]
        result_str += ", ".join(values)
        return result_str
