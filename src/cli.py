from parser.parser import Parser


if __name__ == "__main__":
    db_name = "test_db"
    command_buffer = []
    parser = Parser()
    while True:
        #       db_name = parser.get_current_db()
        CURSOR = ">"
        if command_buffer:
            CURSOR = "|"
        try:
            user_input = input(f"{db_name}{CURSOR}").lower()
            if user_input == "help":
                parser.show_help()
                print()
                command_buffer = []
                continue
            if user_input != "":
                command_buffer.append(user_input)
            elif user_input.endswith(";"):
                parser.parse_input(command_buffer.copy())
                command_buffer = []
            if user_input.lower().startswith("exit"):
                break
        except KeyboardInterrupt:
            print()
            command_buffer = []
            continue
