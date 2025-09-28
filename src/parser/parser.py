import re

from exceptions.SQLSyntaxError import (
    NotEnoughParametersError,
    WrongParametersError,
    UnknownCommandError,
    SQLSyntaxError,
)
from parser.constants import TopLevelApi, commands_data, TypesEnum


class Parser:
    commands = {}

    api: TopLevelApi

    def __init__(self):
        self.api = TopLevelApi()

    def parse_input(self, user_input: list[str]) -> None:
        """Принимает ввод от пользователя и разбивает одну большую команду на под-команды и выполняет каждую команду последовательно
        Например:

        Вход:
        ```
        ["create"
        "table"
        "test"
        "; show tables;"]
        ```

        Выход:
        ```
        ["create table test;", "show tables"]
        ```

        Args:
            input (list[str]): Список строк введенных пользователем до строки с ; на конце
        """
        user_input = " ".join(user_input)
        user_input = user_input.split(";")
        user_input = [item.strip() for item in user_input if item]
        for item in user_input:
            print(item)
            try:
                print(self.parse_command(item))
            except SQLSyntaxError as e:
                print(e)

    def parse_command(self, command: str) -> str:
        """Проверяет, что команда на входе существует, парсит с нее данные и вызывает соответствующий метод TopLevelApi

        Args:
            command (str): команда для выполнения

        Raises:
            WrongParametersError: Возникает при подаче лишних или неправильных параметров
            NotEnoughParametersError: Возникает, когда недостаточно параметров для вызова метода
            UnknownCommandError: Возникает, когда команду на входе нельзя определить

        Returns:
            str: Итог выполнения метода
        """
        for key, value in commands_data.items():
            if key in command:
                pattern = value.pattern
                method = value.method
                if pattern:
                    try:
                        result: tuple[str] = re.search(
                            pattern=pattern, string=command
                        ).groups()
                    except AttributeError as e:
                        raise NotEnoughParametersError(
                            f"Not enough parameters for command\n{value.usage}"
                        ) from e
                    data = []
                    if result:
                        result = [item for item in result if item]
                    match = re.fullmatch(pattern=pattern, string=command)
                    if match:
                        for item in result:
                            if (
                                item.startswith("(")
                                and item.endswith(")")
                                or "," in item
                                or "and" in item
                            ):
                                if ":" in item or "and" not in item and "=" in item:
                                    data.append(self.parse_dict_string(item))
                                else:
                                    data.append(self.parse_tuple_string(item))
                            else:
                                if ("=" in item and "==" not in item) or (":" in item):
                                    data.append(self.parse_dict_string(item))
                                elif "==" in item:
                                    data.append((item,))
                                else:
                                    data.append(item)
                    else:
                        raise WrongParametersError(
                            f"Unknown parameters in command\n{value.usage}"
                        )
                if pattern:
                    for item in data:
                        if item is None:
                            raise NotEnoughParametersError(
                                "Not enough parameters for this command"
                            )
                    return method(self.api, *data)
                return method(self.api)

        raise UnknownCommandError("Unknown command write <help> in this terminal")

    def parse_tuple_string(self, tuple_string: str) -> tuple | list:
        """Разбивает последовательность данных (<value>, <value>) из str в tuple или list

        Args:
            tuple_string (str): Строка последовательность

        Returns:
            tuple | list: Кортеж / список последовательности
        """
        data = tuple_string
        if data.count("(") > 1 and data.count(")") > 1:
            result = []
            pattern = r"\(([^()]*)\)"
            data = re.findall(pattern, data)
            for item in data:
                new_data = item.split(",")
                new_data = [item.strip() for item in new_data]
                result_tuple = tuple(new_data)
                result.append(result_tuple)
            return result
        else:
            if "(" in tuple_string and ")" in tuple_string:
                data = data[1:-1]
            if "," in data:
                delimeter = ","
            else:
                delimeter = "and"
            data = data.split(delimeter)
            data = [item.strip() for item in data if item]
            return tuple(data)

    def parse_dict_string(self, dict_string: str) -> dict:
        """Разбивает строку с последовательностью ключ: значение или ключ=значение на словарь данных

        Args:
            dict_string (str): Строка последовательность

        Returns:
            dict: Словарь данных
        """
        result = {}
        data = dict_string
        if "(" in dict_string and ")" in dict_string:
            data = dict_string[1:-1]
        if "," in data:
            data = data.split(",")
            data = [item.strip() for item in data]
        else:
            data = [data]
        for item in data:
            temp = []
            if ":" in item:
                temp = item.split(":")
            elif "=" in item:
                temp = item.split("=")
            if len(temp) == 2:
                key = temp[0].strip()
                if temp[1].strip().upper() in TypesEnum._member_names_:
                    value = TypesEnum[temp[1].strip().upper()].value
                else:
                    value = temp[1].strip()
                result[key] = value
        return result

    def show_help(self):
        """Вывод краткой справки"""
        print("Available commands:\n")
        for item in commands_data.keys():
            print(item)
