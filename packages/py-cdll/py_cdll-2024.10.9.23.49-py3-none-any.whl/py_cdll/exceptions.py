class BaseCDLLException(Exception):
    """Base exception for Circular Doubly Linked List project."""


class NegativeIndexError(BaseCDLLException):
    """Raise for indices that should be at least 0."""


class ValueNotFoundError(BaseCDLLException):
    """Raise for searches that return no result."""


class FirstValueNotFoundError(BaseCDLLException):
    """Raise when the first input of a method was not found where expected."""


class SecondValueNotFoundError(BaseCDLLException):
    """Raise when the second input of a method was not found where expected."""


class ValuesNotAdjacentError(BaseCDLLException):
    """Raise when values were not found adjacent to each other."""


class NoAdjacentValueError(BaseCDLLException):
    """Raise for searches for adjacent values in lists with single item."""


class MultipleValuesFoundError(BaseCDLLException):
    """Raise for searches that return no result."""


class EmptyCDLLError(BaseCDLLException):
    """Raise when an iterable is found to be empty."""


class NotEmptyTypeError(BaseCDLLException):
    """Raise for values that are not EMPTY."""


class UnevenListLengthError(BaseCDLLException):
    """Raise for lists that contain uneven amount of items."""


class InputNotIterableError(BaseCDLLException):
    """Raise when an input is not iterable."""
