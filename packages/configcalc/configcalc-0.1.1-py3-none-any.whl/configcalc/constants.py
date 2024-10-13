import math
from collections.abc import Callable

from configcalc.typing import Number

OPERATIONS: dict[str, Callable[[Number, Number], Number]] = {
    r"+": lambda a, b: a + b,
    r"-": lambda a, b: a - b,
    r"*": lambda a, b: a * b,
    r"/": lambda a, b: a / b,
    r"^": lambda a, b: a**b,
}

MATH_FUNCTIONS: list[str] = []
MATH_CONSTANTS: list[str] = []
for math_object_name in dir(math):
    math_object = getattr(math, math_object_name)
    if callable(math_object) and not math_object_name.startswith("__"):
        MATH_FUNCTIONS.append(math_object_name)
    elif isinstance(math_object, float):
        MATH_CONSTANTS.append(math_object_name)
