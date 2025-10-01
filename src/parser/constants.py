from enum import Enum
from typing import NamedTuple
from typing import Callable
from top_level_api.data_api import DataAPI
from top_level_api.database_api import DatabaseAPI
from top_level_api.db_manager_api import DBAPI
from top_level_api.table_api import TableAPI


class CommandInfo(NamedTuple):
    pattern: str
    method: Callable
    usage: str


USAGE_BASE = "Usage: "

commands_data: dict[str, CommandInfo] = {
    "create table": CommandInfo(
        r"create\s+table\s+(\w+)\s*(\((?:\w*\:\s*\w*\,?\s*)*\))",
        DatabaseAPI.create_table,
        USAGE_BASE + "CREATE TABLE <table_name> (<field_name>:<field_type>, ...)",
    ),
    "drop table": CommandInfo(
        r"drop\s+table\s+(\w*)",
        DatabaseAPI.drop_table,
        USAGE_BASE + "DROP TABLE <table_name>",
    ),
    "truncate table": CommandInfo(
        r"truncate\s+table\s+(\w*)",
        DatabaseAPI.truncate_table,
        USAGE_BASE + "TRUNCATE TABLE <table_name>",
    ),
    "describe table": CommandInfo(
        r"describe\s+table\s+(\w*)",
        DatabaseAPI.describe_table,
        USAGE_BASE + "DESCRIBE TABLE <table_name>",
    ),
    "show tables": CommandInfo(
        None, DatabaseAPI.show_tables, USAGE_BASE + "SHOW TABLES"
    ),
    "create database": CommandInfo(
        r"create\s+database\s+(\w*)",
        DBAPI.create_database,
        USAGE_BASE + "CREATE DATABASE <db_name>",
    ),
    "update database": CommandInfo(
        r"update\s+database\s+(\w*)\s+(\w+)",
        DBAPI.update_database,
        USAGE_BASE + "UPDATE DATABASE <old_db_name> <new_db_name>",
    ),
    "use database": CommandInfo(
        r"use\s+database\s+(\w*)",
        DBAPI.use_database,
        USAGE_BASE + "USE DATABASE <db_name>",
    ),
    "drop database": CommandInfo(
        r"drop\s+database\s+(\w*)",
        DBAPI.drop_database,
        USAGE_BASE + "DROP DATABASE <db_name>",
    ),
    "show databases": CommandInfo(
        None, DBAPI.show_databases, USAGE_BASE + "SHOW DATABASES <db_name>"
    ),
    "add column": CommandInfo(
        r"alter\s+table\s+(\w*)\s+add\s+column\s+(\w*\s*:\s*\w*)",
        TableAPI.add_column,
        USAGE_BASE + "ALTER TABLE <table_name> ADD COLUMN <column_name>:<column_type>",
    ),
    "drop column": CommandInfo(
        r"alter\s+table\s+(\w*)\s+drop\s+column\s+(\w*)",
        TableAPI.drop_column,
        USAGE_BASE + "ALTER TABLE <table_name> DROP COLUMN <column_name>",
    ),
    "modify column": CommandInfo(
        r"alter\s+table\s+(\w*)\s+modify\s+column\s+(\w*)\s+(\w*\s*:\s*\w*)",
        TableAPI.modify_column,
        USAGE_BASE
        + "ALTER TABLE <table_name> MODIFY COLUMN <old_column_name> <new_column_name>:<new_column_type>",
    ),
    "update": CommandInfo(
        r"update\s*(\w+)\s*set\s*(\w+=\w+(?:\,{1}\s*\w+\s*=\s*\w+|\d+)*)(?:\s*where\s*(\w+[!=><]+\w+|\d+))?",
        DataAPI.update,
        USAGE_BASE
        + "UPDATE <table_name> SET <column_name>=<value> (WHERE <column_name> == <value> AND ...)",
    ),
    "select": CommandInfo(
        r"select\s+(?:(\*{1}|\w+(?:\,\s*\w+)*)?)\s+from\s+(\w+)(?:\s+where\s+(\w+[!=><]+(?:\d|\w+)(?:\s+and\s+\w+\s*[!=><]+\s*(?:\d+|\w+))*)?)?",
        DataAPI.select,
        USAGE_BASE
        + "SELECT <fields> (or *) FROM <table_name> (WHERE <column_name> == <value> AND ...)",
    ),
    "delete": CommandInfo(
        r"delete\s+from\s+(\w+)(?:\s+where\s+(\w+[!=><]+(?:\d|\w+)(?:\s+and\s+\w+\s*[!=><]+\s*(?:\d+|\w+))*)?)?",
        DataAPI.delete_from,
        USAGE_BASE
        + "DELETE FROM <table_name> (WHERE <column_name> == <value> AND ...)",
    ),
    "insert": CommandInfo(
        r"insert\s+into\s+(\w+)\s*(\(\w+(?:\s*\,{1}\s*\w*)?\))\s+values\s*((?:\,?\s*\((?:\w+|d+){1}(?:\,{1}\s*(?:\w+|\d+))*\))*)",
        DataAPI.insert,
        USAGE_BASE
        + "INSERT INTO <table_name> (<field>, <field>) VALUES (<value>, <value>), (<value>, <value>)",
    ),
}


class TypesEnum(Enum):
    INT = int
    STR = str
