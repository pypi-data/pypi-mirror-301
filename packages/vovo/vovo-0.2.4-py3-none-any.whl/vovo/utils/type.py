from typing import Union, Any


def get_type(value: Any) -> Union[str, type]:
    """
    从字典中检索类型值

    Returns:
        The type value.
    """
    # get "type" or "annotation" from the value
    _type = value.get("type") or value.get("annotation")

    return _type if isinstance(_type, str) else _type.__name__
