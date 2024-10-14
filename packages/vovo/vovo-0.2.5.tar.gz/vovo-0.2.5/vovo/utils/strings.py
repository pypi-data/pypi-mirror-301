import re
from typing import Any, List


pattern_uppercase = re.compile(r"([A-Z]+)([A-Z][a-z])")
pattern_camel_case = re.compile(r"([a-z\d])([A-Z])")


def str_to_snake(string: str) -> str:
    """
    Examples:
    -------
    >>> str_to_snake("myCamelName") == my_camel_name"
    assert str_to_snake("snake-case-example") == "snake_case_example"
    assert str_to_snake("AnotherExample123") == "another_example123"
    assert str_to_snake("PascalCase") == "pascal_case"
    """
    string = pattern_uppercase.sub(r"\1_\2", string)
    string = pattern_camel_case.sub(r"\1_\2", string)
    string = string.replace("-", "_")
    return string.lower()


def stringify_value(val: Any) -> str:
    """Stringify a value.

    Args:
        val: The value to stringify.

    Returns:
        str: The stringifies value.
    """
    if isinstance(val, str):
        return val
    elif isinstance(val, dict):
        return "\n" + stringify_dict(val)
    elif isinstance(val, list):
        return "\n".join(stringify_value(v) for v in val)
    else:
        return str(val)


def stringify_dict(data: dict) -> str:
    """Stringify a dictionary.

    Args:
        data: The dictionary to stringify.

    Returns:
        str: The stringifies dictionary.
    """
    text = ""
    for key, value in data.items():
        text += key + ": " + stringify_value(value) + "\n"
    return text


def join_with_separator(items: List[Any], separator: str = ", ") -> str:
    """Convert a list to a string separated by a custom separator.

    Args:
        items: The list to convert.
        separator: The string to use as a separator, default is ', '.

    Returns:
        str: The separated string.
    """
    return separator.join(str(item) for item in items)
