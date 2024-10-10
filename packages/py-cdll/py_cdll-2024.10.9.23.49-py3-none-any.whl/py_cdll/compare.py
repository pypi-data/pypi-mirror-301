from enum import Enum, auto
from typing import Any


class Comparison(Enum):
    EQUALITY = auto()
    IDENTITY = auto()


def compare_identity(data0: Any, data1: Any) -> bool:
    is_identical: bool = False
    if data0 is data1:
        is_identical = True
    return is_identical


def compare_equality(data0: Any, data1: Any) -> bool:
    is_equal: bool = False
    if data0 == data1:
        is_equal = True
    return is_equal


def compare(data0: Any, data1: Any, comparison: Comparison) -> bool:
    is_comparable: bool = False

    match comparison:
        case Comparison.IDENTITY:
            is_comparable = compare_identity(data0, data1)
        case Comparison.EQUALITY:
            is_comparable = compare_equality(data0, data1)

    return is_comparable
