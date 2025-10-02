from dataclasses import dataclass
from typing import Callable
import re

from exceptions.SQLSyntaxError import (
    WrongParametersError,
    UnknownCommandError,
    SQLSyntaxError,
)
from parser.constants import (
    TopLevelApi,
    commands_data,
    TypesEnum,
)
from enum_status import Status


@dataclass
class ApiResult:
    status: Status
    message: str = ""


class Parser:
    commands = {}

    def __init__(self):
        self.top_level_api = TopLevelApi()

    def get_current_db(self):
        data: ApiResult = self.top_level_api.get_current_db()
        return data.message

    def parse_input(self, user_input: list[str]) -> None:  # pragma: no cover
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
            try:
                print(self._parse_command(item))
            except SQLSyntaxError as e:
                print(e)

    def _parse_command(self, command: str) -> str:
        """Проверяет, что команда на входе существует, парсит с нее данные и вызывает соответствующий метод TopLevelApi

        Args:
            command (str): команда для выполнения

        Raises:
            WrongParametersError: Возникает при подаче лишних или неправильных параметров
            UnknownCommandError: Возникает, когда команду на входе нельзя определить

        Returns:
            str: Итог выполнения метода
        """
        for key, value in commands_data.items():
            if key in command:
                method_fields = value.method.__annotations__
                method_fields.pop("return", 0)
                values = None
                if value.pattern is None:
                    return value.method(self.top_level_api)
                else:
                    values = []
                    match = re.fullmatch(pattern=value.pattern, string=command)
                    if match:
                        groups = match.groups()
                    else:
                        raise WrongParametersError(
                            f"Wrong parameters with this command\n{value.usage}"
                        )
                    for field_value, field_type in zip(groups, method_fields.values()):
                        values.append(
                            self._parse_field(
                                field_value=field_value, field_type=field_type
                            )
                        )
                    return value.method(self.top_level_api, *values)
        raise UnknownCommandError("Unknown command\nUse help command in this terminal")

    def _parse_field(
        self, field_value: str, field_type: type
    ) -> tuple | list | dict | str:
        """В зависимости от типа данных, вызывает определенную функцию для парсинга строку с данными

        Args:
            field_value (str): Строка с данными
            field_type (type): В какой тип данных должно превратиться поле field_value

        Returns:
            tuple | list | dict | str: Извлеченная структура данных
        """
        method = parse_types.get(field_type, None)
        if method:
            return method(field_value)
        else:
            return field_value


def _parse_tuple_string(tuple_string: str) -> tuple:
    """Разбивает строку с последовательностью на кортеж данных последовательности

    Args:
        tuple_string (str): Входная строка для обработки

    Returns:
        tuple: Кортеж с извлеченными данными
    """
    if tuple_string is None:
        return None
    if tuple_string.startswith("(") and tuple_string.endswith(")"):
        tuple_string = tuple_string[1:-1]
    result = tuple_string
    delimeters = [",", "and"]
    for delimeter in delimeters:
        if delimeter in tuple_string:
            result = tuple_string.split(delimeter)
            result = [item.strip() for item in result if item]
    return (result,)


def _parse_dict_string(dict_string: str) -> dict:
    """Разбивает строку с указанием данных на словарь данных

    Args:
        dict_string (str): Строка с данными

    Returns:
        dict: Словарь данных
    """
    if dict_string.startswith("(") and dict_string.endswith(")"):
        dict_string = dict_string[1:-1]
    delimeters = [":", "="]
    result = {}
    for delimeter in delimeters:
        if delimeter in dict_string:
            if "," in dict_string:
                data = dict_string.split(",")
            else:
                data = [dict_string]
            for item in data:
                pair = item.split(delimeter)
                pair = [item.strip() for item in pair if item]
                key = pair[0]
                value = pair[1]
                if delimeter == ":" and pair[1].upper() in TypesEnum._member_names_:
                    value = TypesEnum[value.upper()].value
                result[key] = value
    return result


def _parse_list_string(list_string: str) -> list:
    """Используется, чтобы обработать строку
    Если в ней есть большая последовательность сгруппированных данных

    Args:
        list_string (str): Строка с данными

    Returns:
        list: Список элементов
    """
    result = []
    pattern = r"(\w+\,?\s*\w*)"
    groups = re.findall(pattern=pattern, string=list_string)
    for item in groups:
        if "," in item:
            data = item.split(",")
            data = tuple([item.strip() for item in data if item])
        else:
            data = (item,)
        result.append(data)
    return result


def show_help():  # pragma: no cover
    """Вывод краткой справки"""
    print("Available commands:\n")
    for item in commands_data.keys():
        print(item)


parse_types: dict[type, Callable] = {
    str: None,
    dict: _parse_dict_string,
    list: _parse_list_string,
    tuple: _parse_tuple_string,
}
