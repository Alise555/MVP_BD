from enum import Enum

from exceptions.SQLSyntaxError import SQLSyntaxError
from mock.top_level_api import TopLevelApi


class TypesEnum(Enum):
    INT = int
    STR = str


class Parser:
    commands = {}

    def __init__(self):
        self.commands: dict[str, dict] = {
            "database": {
                "create database": (TopLevelApi.create_database, 1),
                "update database": (TopLevelApi.update_database, 2),
                "drop database": (TopLevelApi.drop_database, 1),
                "show databases": (TopLevelApi.show_databases, 0),
                "use database": (TopLevelApi.use_database, 1),
            },
            "table": {
                "show tables": (TopLevelApi.show_tables, 0),
                "create table": (TopLevelApi.create_table, 2),
                "describe table": (TopLevelApi.describe_table, 1),
                "drop table": (TopLevelApi.drop_table, 1),
                "truncate table": (TopLevelApi.truncate_table, 1),
                "alter table": TopLevelApi.alter_table,
            },
        }
        self.api = TopLevelApi()

    def get_current_db(self):
        return self.api.get_current_db()

    def parse_input(self, data: list[str]):
        commands = " ".join(data)
        if commands.count(";") > 1:
            list_commands = commands.split(";")
            list_commands = [
                command.strip() for command in list_commands if command != ""
            ]
            for command in list_commands:
                print(self.parse_command(command.replace(";", "")))
        else:
            print(self.parse_command(commands.replace(";", "")))

    def parse_command(self, command: str):
        api = self.api
        sphere_key = [sphere for sphere in self.commands.keys() if sphere in command]
        if len(sphere_key) == 1:
            sphere_commands = self.commands[sphere_key[0]]
            sphere_command_key = [
                command_key for command_key in sphere_commands if command_key in command
            ]
            if len(sphere_command_key) == 1:
                method = sphere_commands[sphere_command_key[0]]
                data = command.replace(sphere_command_key[0], "").strip()
                additional_data = []
                method_data = []
                while "(" in data and ")" in data:
                    data_tuple = data[data.find("(") + 1 : data.find(")")]
                    if ":" in data_tuple:
                        additional_data.append(self._parse_type_data(data_tuple))
                    data = data.replace(data[data.find("(") : data.find(")") + 1], "")
                if data != "":
                    method_data = data.split(" ")
                method_data += additional_data
                method_data = [item for item in method_data if item]
                if len(method_data) == method[1]:
                    return method[0](api, *method_data)
                elif len(method_data) > method[1]:
                    print("Too much arguments!")
                else:
                    print("Not enough arguments!")

    def _parse_type_data(self, data: str) -> None:
        data_dict = {}
        data: list[str] = data.split(",")
        for pair in data:
            if ":" in pair:
                pair = pair.split(":")
                data_dict[pair[0].strip()] = TypesEnum[pair[1].strip().upper()].value
        return data_dict
