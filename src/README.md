*** Запуск общего функционала 

Чтобы запустить проект, клонируйте репозиторий и перейдите в него через командную строку:
    ```
    git clone https://github.com/Alise555/MVP_BD.git
    ```
    ```
    cd MVP_BD
    ```
перейдите по ветке dev:

    ```
    git switch dev
    ```

*далее для ввода команд на Windows используйте ```python```вместо ```python3```
Создайте виртуальное окружение:

    ```
    python3 -m venv venv
    ```

Активируйте виртуальное окружение:
Linux/macOS:

    ```
    source venv/bin/activate
    ```
Windows:

    ```
    venv/Scripts/activate
    ```
- В терминале вы должны увидеть (venv) слева

Установите зависимости из файла requirements.txt:

    ```
    pip install -r requirements.txt 
    ```

** Заполнение требуемых данных
В файле src/config/config.py заполните данные - пути к БД и файла, где будут храниться метаданные. Например:

```
path = "/home/../MVP_BD/research/test"  # путь где будут хранится бд
metadata_name = "metadata_file"  # .metadata название файла metadata
```

** Создание конфигурации для запуска
Сочетанием клавиш **Ctrl+Shift+D** откройте вкладку **Run and Debug**. Редактор кода предложит создать файл: **create a launch.json.file**. Нажмите на гиперссылку. Откроется всплывающее окно. Выберите **Python Debugger** -> **Python File**. Введите следующее:

```
{
            "name": "Cli",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/src/cli.py",
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/src/"
            }
        }
```

** Работа программы 
Для ознакомления с существующими командами, запустите проект, в терминал введите:

```
help
```
Выведится набор команд

Для продолжения работы с программой, введите одну из команд. Примеры использования:

1) create table <table_name> (<field_name>:<field_type>, <field_name>:<field_type>, ...); -- перед созданием необходимо выбрать базу данных - use database <name_database>;
2) drop table <table_name>;
3) describe table <table_name>;
4) show tables ; - перед выводом таблиц необходимо выбрать базу данных - use database <name_database>;
5) create database <name_database>;
6) update database <old_name_database> <new_name_database>;
7) use database <name_database>;
8) drop database <name_database>;
9) show databases ;
----
10) alter table <table_name> add column <column_name>:<column_type>;- не добавляется
11) drop column
12) alter table <table_name> modify column <old_column_name> <new_column_name>:<new_column_type>; - не изменяется
13) update
14) select
15) delete
16) insert

Для выхода из программы введите в терминал:

```
exit
```
