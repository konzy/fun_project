from typing import Any, List


def run_function(function: str, column_values: List[str] | None, args: List[str] | None) -> Any:
    if function == "concat":
        return concat(column_values, args)
    if function == "default_value":
        return default_value(column_values, args)
    return None


def concat(column_values: List[str] | None, args: List[str] | None) -> str | None:
    if column_values is None or column_values == []:
        return None
    return "".join(column_values)


def default_value(column_values: List[str] | None, args: List[str] | None) -> str | None:
    if column_values is None or column_values == [] or column_values[0] == "":
        if args is None or args == []:
            return None
        return args[0]
    return column_values[0]
