class SQLSyntaxError(Exception):
    pass


class NotEnoughParametersError(SQLSyntaxError):
    pass


class WrongParametersError(SQLSyntaxError):
    pass


class UnknownCommandError(SQLSyntaxError):
    pass
