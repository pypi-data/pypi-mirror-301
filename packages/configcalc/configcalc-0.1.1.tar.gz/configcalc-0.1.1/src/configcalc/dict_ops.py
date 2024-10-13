from typing import Any


def get_deep(nested_list: list[Any], indices: list[int]) -> Any:
    # see https://stackoverflow.com/a/44579249/10926757
    if (len(indices) > 1) and (isinstance(nested_list[indices[0]], (list, dict))):
        return get_deep(nested_list[indices[0]], indices[1:])
    else:
        return nested_list[indices[0]]


def set_deep(nested_list: list[Any], indices: list[int], value: Any) -> list[Any]:
    if (len(indices) > 1) and isinstance(nested_list[indices[0]], (list, dict)):
        set_deep(nested_list[indices[0]], indices[1:], value)
    else:
        nested_list[indices[0]] = value
    return nested_list
