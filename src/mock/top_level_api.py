class TopLevelApi:
    current_db = "default_db"

    def get_current_db(self):
        return self.current_db

    def create_database(self, db_name: str):
        return f"create database <{db_name}> OK"

    def update_database(self, old_db_name: str, new_db_name: str):
        return f"update database <{old_db_name}> -> <{new_db_name}> OK"

    def drop_database(self, db_name: str):
        return f"drop database <{db_name}> OK"

    def show_databases(self):
        return "database_1\ndatabase_2"

    def use_database(self, db_name: str):
        self.current_db = db_name
        return f"use database <{self.current_db}> OK"

    def show_tables(self):
        return "table_1\ntable_2"

    def create_table(self, table_name: str, table_struct: dict):
        return f"create table <{table_name}> OK\nstruct {table_struct}"

    def describe_table(self, db_name: str):
        return f"<{db_name}>\nname: str\nage: int"

    def drop_table(self, table_name: str):
        return f"drop table <{table_name}>: OK"

    def truncate_table(self, table_name: str):
        return f"truncate table <{table_name}>: OK"

    def add_column(self, column_data: dict):
        return f"add column {column_data} OK"

    def drop_column(self, column_name: str):
        return f"drop column {column_name} OK"

    def modify_column(self, column_name: str, column_data: dict):
        return f"modify column {column_name} -> {column_data}"

    def select_from(self, fields: str, table_name: str, filtered: tuple = None):
        if fields == "*":
            fields = "ALL"
        if filtered:
            return f"select {fields} from {table_name} where {filtered}"
        return f"select {fields} from {table_name}"

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

    def insert(self, table_name: str, fields: tuple, values: list | tuple):
        if isinstance(values, list):
            result_str = ""
            for item in values:
                result_str += f"insert into {table_name}, {fields}, {item}\n"
            return result_str
        else:
            return f"insert into {table_name}, {fields}, {values}"
