import pytest

from parser.parser import Parser
from exceptions.SQLSyntaxError import WrongParametersError, UnknownCommandError


@pytest.mark.parametrize(
    "input_data, response",
    [
        ("create database test", "create database <test> OK"),
        ("update database test test_1", "update database <test> -> <test_1> OK"),
        ("use database test", "use database <test> OK"),
        ("drop database test", "drop database <test> OK"),
        ("show databases", "database_1\ndatabase_2"),
        (
            "create table test (name: str, age: int)",
            "create table <test> OK\nstruct {'name': <class 'str'>, 'age': <class 'int'>}",
        ),
        ("drop table test", "drop table <test> OK"),
        ("truncate table test", "truncate table <test> OK"),
        ("describe table test", "<test>\nname: str\nage: int"),
        ("show tables", "table_1\ntable_2"),
        (
            "alter table test_table modify column test test_1:int",
            "alter table <test_table> modify column <test> -> <{'test_1': <class 'int'>}>",
        ),
        (
            "alter table test_table add column name:str",
            "alter table <test_table> add column {'name': <class 'str'>} OK",
        ),
        (
            "alter table test_table drop column test",
            "alter table <test_table> drop column test OK",
        ),
        ("select name, age from test", "select (['name', 'age'],) from test"),
        ("select * from test where id=1", "select ALL from test where ('id=1',)"),
        ("delete from test", "delete from test"),
        ("delete from test where id=1", "delete from test where ('id=1',)"),
        ("update test set name=admin", "update test set {'name': 'admin'}"),
        (
            "update test set name=admin where id=1",
            "update test set {'name': 'admin'} where ('id=1',)",
        ),
        (
            "insert into test (name, level) values (admin, 1)",
            "insert into test (['name', 'level'],) ('admin', '1')",
        ),
        (
            "insert into test (name) values (admin)",
            "insert into test ('name',) ('admin',)",
        ),
        (
            "insert into test (name, level) values (admin, 1), (test, 2), (user, 3)",
            "insert into test (['name', 'level'],) ('admin', '1'), ('test', '2'), ('user', '3')",
        ),
    ],
)
def test_valid_input(input_data, response):
    parser = Parser()
    assert parser._parse_command(input_data) == response


@pytest.mark.parametrize(
    "input_data, error",
    [
        ("create database test 1234", WrongParametersError),
        ("create not_database", UnknownCommandError),
        ("create table test (name)", WrongParametersError),
    ],
)
def test_invalid_input(input_data, error):
    parser = Parser()
    with pytest.raises(error):
        parser._parse_command(input_data)
