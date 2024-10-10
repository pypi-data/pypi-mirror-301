# https://cppsecrets.com/users/109699104101114117107117114105109101103104971109749495564103109971051084699111109/Python-Program-to-Implement-Circular-Doubly-Linked-List.php
# https://www.sanfoundry.com/python-program-implement-circular-doubly-linked-list/
# https://github.com/rachit-ranjan16/dat_struct_py/blob/master/dat_struct_py/linkedlist.py
import logging
from collections.abc import Collection
from enum import Enum, auto
from typing import Any, List, Self

from .node import Node, _count_nodes
from .compare import Comparison, compare
from .exceptions import ValueNotFoundError, MultipleValuesFoundError, \
    NoAdjacentValueError, NotEmptyTypeError, NegativeIndexError, UnevenListLengthError, EmptyCDLLError, \
    FirstValueNotFoundError, SecondValueNotFoundError, ValuesNotAdjacentError, InputNotIterableError


class Connectivity(Enum):
    ADJACENT_NEXT = auto()
    ADJACENT_PREVIOUS = auto()


class Initial(object):
    pass


class Empty(object):
    def __repr__(self) -> str:
        return "EMPTY"


INITIAL = Initial()
EMPTY = Empty()


# TODO: fit requirements for "Iterable" by adding "__iter__" method
# TODO: create CircularDoublyLinkedListIterator()
#       https://stackoverflow.com/a/21665616
#       returning iterator capable object with index and link to parent data
#       when calling __iter__ on parent.
# TODO: improve to fit requirements for "Collection" typehint
# TODO: implement as python compliant container:
# https://docs.python.org/3/reference/datamodel.html#emulating-container-types
# https://stackoverflow.com/a/68446663

# https://docs.python.org/3/tutorial/datastructures.html
# TODO: switch meaning of remove and remove_first to remove and remove_all or something like that
# TODO: implement list.index equivalent
# TODO: implement list.count equivalent
# TODO: implement list.sort equivalent
# TODO: implement list.reverse equivalent
# TODO: implement list.copy equivalent
# TODO: implement del list[x] list[x:y] list[:] equivalent

#
# __add__

class CDLL:
    # TODO: rename "end" to "tail"

    def __init__(self, data: Collection[Any] | Initial = INITIAL, empty_length: int = 0) -> None:
        self._initialized: bool = False
        self._length: int = 0

        if data is not INITIAL and len(data) > 0:
            self._initialize(data)

        while len(self) < empty_length:
            self.append(EMPTY)

    def __repr__(self) -> str:
        # TODO: print ints without ''s
        try:
            node_list: List[Node] = [self._head]
            next_node: Node = self._head.next
            while next_node is not self._head:
                node_list.append(next_node)
                next_node = next_node.next
        except AttributeError:
            node_list: List[Node] = []

        node_datas: List[str] = [str(node.data) for node in node_list]
        string = str(node_datas)

        return string

    def __str__(self) -> str:
        return self.__repr__()

    def __add__(self, other: Self) -> Self:
        if not isinstance(other, CDLL):
            raise TypeError(f"Can only concatenate {type(self)} (not '{type(other)}') to {type(self)}")

        new_list: CDLL = CDLL()

        for item in self:
            new_list.append(item)

        for item in other:
            new_list.append(item)

        return new_list

    def __mul__(self, multiplier: int) -> Self:
        list_: CDLL
        if multiplier <= 0:
            list_ = CDLL()
        elif multiplier == 1:
            list_ = self
        else:
            list_ = CDLL()
            for _ in range(multiplier):
                for item in self:
                    list_.append(data=item)

        return list_

    @property
    def head(self) -> Any:
        try:
            return self._head.data
        except AttributeError:
            raise EmptyCDLLError

    @property
    def end(self) -> Any:
        try:
            return self._head.previous.data
        except AttributeError:
            raise EmptyCDLLError

    def _node_with_unique(self, data: Any, comparison: Comparison = Comparison.IDENTITY) -> Node:
        count: int = 0
        result_node: Node | None = None

        try:
            current_node: Node = self._head
        except AttributeError:
            raise EmptyCDLLError(f"CDLL with no values can not return a value.")

        for _ in range(self._length):
            is_comparable: bool = compare(data0=data, data1=current_node.data, comparison=comparison)

            if is_comparable:
                count += 1

                if count > 1:
                    raise MultipleValuesFoundError(f"More than one instance of data found")

                result_node = current_node

            current_node = current_node.next

        if count < 1:
            raise ValueNotFoundError(f"No instance of data found")

        return result_node

    def _node_with_first(self, data: Any, comparison: Comparison = Comparison.IDENTITY) -> Node:
        result_node: Node | None = None

        try:
            current_node: Node = self._head
        except AttributeError:
            raise EmptyCDLLError(f"CDLL with no values can not return a value.")

        for _ in range(self._length):
            is_comparable: bool = compare(data0=data, data1=current_node.data, comparison=comparison)

            if is_comparable:
                result_node = current_node
                break

            current_node = current_node.next

        if result_node is None:
            raise ValueNotFoundError(f"No instance of data found")

        return result_node

    # TODO: evaluate if other methods would benefit from interchangeable comparisons
    # TODO: would this benefit from _node_with_unique, as before_unique and after_unique ?
    def find_unique(self, data: Any, comparison: Comparison = Comparison.IDENTITY) -> int:
        if len(self) == 0:
            raise EmptyCDLLError(f"Impossible to find data in empty list.")

        count: int = 0
        recent_index: int = 0

        for index, data_ in enumerate(self):
            is_comparable: bool = compare(data0=data, data1=data_, comparison=comparison)

            if is_comparable:
                count += 1

                if count > 1:
                    raise MultipleValuesFoundError(f"More than one instance of data found")

                recent_index = index

        if count < 1:
            raise ValueNotFoundError(f"No instance of data found")

        return recent_index

    def find_first(self, data: Any, compare_eq: bool = False) -> int:
        # INFO: Comparison is on ID with "is", not on equality with "=="
        # TODO: implement id/eq with comparison enum

        first_found_at_index: int = 0
        count: int = 0

        for index, data_ in enumerate(self):
            if compare_eq:
                if data_ == data:
                    count += 1
                    first_found_at_index = index
                    break
            else:
                if data_ is data:
                    count += 1
                    first_found_at_index = index
                    break

        if count < 1:
            raise ValueNotFoundError(f"No instance of item found")

        return first_found_at_index

    # TODO: abstract before/after into unique that returns node instead of data
    #       and use previous/next node to pass to that
    #       to reduce code repetition
    def before_unique(self, data: Any) -> Any:
        if len(self) == 1:
            raise NoAdjacentValueError(f"No data possible before input in list of length 1")

        node: Node = self._node_with_unique(data=data, comparison=Comparison.IDENTITY)

        return node.previous.data

    def after_unique(self, data: Any) -> Any:
        if len(self) == 1:
            raise NoAdjacentValueError(f"No data possible after input in list of length 1")

        node: Node = self._node_with_unique(data=data, comparison=Comparison.IDENTITY)

        return node.next.data

    def set_before_unique(self, data: Any, set_data: Any) -> None:
        if len(self) == 1:
            raise NoAdjacentValueError(f"No data before input in list of length 1")

        node: Node = self._node_with_unique(data=data, comparison=Comparison.IDENTITY)
        node.previous.data = set_data

    def set_after_unique(self, data: Any, set_data: Any) -> None:
        if len(self) == 1:
            raise NoAdjacentValueError(f"No data after input in list of length 1")

        node: Node = self._node_with_unique(data=data, comparison=Comparison.IDENTITY)
        node.next.data = set_data

    # TODO: decide whether to rename "set_*_unique" to "replace", or "replace_unique" to "set_unique"
    def replace_unique(self, unique_data: Any, set_data: Any, comparison: Comparison = Comparison.IDENTITY) -> None:
        unique_index: int = self.find_unique(data=unique_data, comparison=comparison)
        self[unique_index] = set_data

    def ordered(self, data0: Any, data1: Any) -> (Any, Any):
        # TODO: refactor to have single pass of list instead of two

        try:
            data0_index: int = self.find_unique(data0)
        except ValueNotFoundError:
            # TODO: create test that triggers exception
            raise FirstValueNotFoundError(f"First value not found in CDLL.")

        try:
            data1_index: int = self.find_unique(data1)
        except ValueNotFoundError:
            # TODO: create test that triggers exception
            raise SecondValueNotFoundError(f"Second value not found in CDLL.")

        first_node: Any = data0 if data0_index < data1_index else data1
        second_node: Any = data0 if data0_index > data1_index else data1

        return first_node, second_node

    def ordered_occurrence(self, data_first: Any, data_second: Any) -> bool:
        try:
            first, second = self.ordered(data0=data_first, data1=data_second)
        except (FirstValueNotFoundError, SecondValueNotFoundError) as exception:
            raise exception

        ordered: bool = data_first is first and data_second is second
        return ordered

    def adjacent(self, data0: Any, data1: Any) -> bool:
        # TODO: raise exception if length is <2

        is_nodes_adjacent: bool = False

        try:
            data0_node: Node = self._node_with_unique(data=data0, comparison=Comparison.IDENTITY)
        except ValueNotFoundError:
            return is_nodes_adjacent

        is_data0_next_data1: bool = data0_node.next.data is data1
        is_data0_previous_data1: bool = data0_node.previous.data is data1
        is_nodes_adjacent = is_data0_next_data1 or is_data0_previous_data1

        return is_nodes_adjacent

    def adjacency_direction(self, first: Any, second: Any) -> Connectivity:
        # Direction from first towards second, if adjacent
        connectivity: Connectivity | None = None

        try:
            first_node: Node = self._node_with_unique(data=first, comparison=Comparison.IDENTITY)
        except ValueNotFoundError as exception:
            raise FirstValueNotFoundError from exception

        if first_node.next.data is second:
            connectivity: Connectivity = Connectivity.ADJACENT_NEXT
        elif first_node.previous.data is second:
            connectivity: Connectivity = Connectivity.ADJACENT_PREVIOUS

        try:
            second_node: Node = self._node_with_unique(data=second, comparison=Comparison.IDENTITY)
        except ValueNotFoundError as exception:
            raise SecondValueNotFoundError from exception

        if first_node and second_node and not connectivity:
            raise ValuesNotAdjacentError(f"'{first}' and '{second}' are not adjacent in '{self}'.")

        return connectivity

    def _initialize(self, data: Collection[Any]) -> None:
        # self._head: Node = Node(data.[0])
        self._head: Node = Node(next(iter(data)))
        self._head.next = self._head
        self._head.previous = self._head
        self._initialized = True
        self._length += 1

        for item in data[1:]:
            self.append(item)

    def append(self, data: Any) -> None:
        if not self._initialized:
            self._initialize([data])
        else:
            self._insert_after_node(self._head.previous, Node(data))

    def extend(self, data: Collection[Any]) -> None:
        try:
            for data_ in data:
                self.append(data=data_)
        except TypeError:
            raise InputNotIterableError(f"Input contains no data that can be appended to CDLL.")

    def insert(self, index: int, data: Any) -> None:
        if not self._initialized:
            self._initialize([data])
        else:
            self._insert(index, data)

    def clear(self) -> None:
        try:
            del self._head
        except AttributeError:
            # AttributeError arising from missing _head means that cdll head is already nonexistent,
            # which is the desired outcome, so the exception is caught here without further action.
            pass

        self._initialized = False
        self._length = 0

    def _remove_node(self, node: Node) -> None:
        node.previous.next = node.next
        node.next.previous = node.previous

        self._length -= 1

    def remove(self, data: Any) -> None:
        node: Node = self._node_with_unique(data=data, comparison=Comparison.IDENTITY)
        self._remove_node(node=node)

    def remove_first(self, data: Any) -> None:
        node: Node = self._node_with_first(data=data, comparison=Comparison.IDENTITY)
        self._remove_node(node=node)

    def pop(self, index: int) -> Any:
        node: Node = self._node_at_index(index=index)
        self._remove_node(node=node)
        return node.data

    # TODO: generalise shift head to take positive and negative
    def _shift_head_forwards(self, amount: int = 1) -> None:
        # TODO: raise exception when cdll does not have even length
        #       can't seem to remember reason why that would be necessary in all cases...
        if amount <= 0:
            raise ValueError(f"Amount to shift '{amount}' must be a positive integer")
        for _ in range(amount):
            self._head = self._head.next

    def _shift_head_backwards(self, amount: int = 1) -> None:
        # TODO: raise exception when cdll does not have even length
        #       can't seem to remember reason why that would be necessary in all cases...
        if amount <= 0:
            raise ValueError(f"Amount to shift '{amount}' must be a positive integer")
        for _ in range(amount):
            self._head = self._head.previous

    def rotate(self, amount: int = 0) -> None:
        if amount == 0:
            pass
        elif amount > 0:
            self._shift_head_backwards(amount=amount)
        elif amount < 0:
            self._shift_head_forwards(amount=abs(amount))

    def _node_at_index(self, index: int) -> Node:
        index = self._normalize_index(index=index)

        # When normalizing, this condition will never fail; also, it appears that no test was triggered by it...
        # if index < 0:
        #     raise NegativeIndexError(f"Index value of '{index}' is not valid")

        current_index: int = 0
        current_node: Node = self._head

        while current_index < index:
            current_node = current_node.next
            current_index += 1

        return current_node

    def _data_from_node_at_index(self, index: int) -> Any:
        data: Any = self._node_at_index(index).data
        return data

    def _insert_after_node(self, list_node: Node, new_node: Node) -> None:
        new_node.previous = list_node
        new_node.next = list_node.next

        list_node.next = new_node
        new_node.next.previous = new_node

        self._length += 1

    def _insert_before_node(self, list_node: Node, new_node: Node) -> None:
        self._insert_after_node(list_node.previous, new_node)

    @staticmethod
    def _replace_node(list_node: Node, new_node: Node) -> None:
        new_node.next = list_node.next
        new_node.previous = list_node.previous

        list_node.next.previous = new_node
        list_node.previous.next = new_node

        # length does not change with replacement
        # self._length += 0

    def _replace_at_index(self, index: int, data: Any) -> None:
        if not self._initialized and index == 0:
            self._initialize([data])
        else:
            node_current = self._node_at_index(index)
            node_new = Node(data)
            self._replace_node(node_current, node_new)
            if index == 0:
                self._head = node_new

    def _insert(self, index: int, data: Any) -> None:
        if not self._initialized and index == 0:
            self._initialize([data])
        else:
            node_current = self._node_at_index(index)
            node_new = Node(data)
            self._insert_before_node(node_current, node_new)
            if index == 0:
                self._head = node_new

    def insert_on_empty(self, index: int, data: Any) -> None:
        # TODO: evaluate whether this is intended to work as replace_on_empty rather than insert
        #       look at tests for hints
        if self[index] is EMPTY:
            self.insert(index=index, data=data)
        else:
            raise NotEmptyTypeError(f"Can not insert data to index "
                                    f"containing item '{self[index]}' "
                                    f"of type '{type(self[index])}' "
                                    f"instead of 'EMPTY'.")

    def set_to_empty(self, index: int) -> None:
        self.insert(index=index, data=EMPTY)

    def first_non_empty(self) -> Any:
        if len(self) == 0:
            raise EmptyCDLLError(f"CDLL with no values can not return a value.")

        try:
            first_data: Any = next(data for data in self if data is not EMPTY)
        except StopIteration:
            raise ValueNotFoundError(f"CDLL with only EMPTY values can not return a non-EMPTY value.")
        return first_data

    def __len__(self) -> int:
        return self._length

    def _normalize_index(self, index: int) -> int:
        length: int = self._length

        if index < -length or index >= length:
            # IndexError used by python loops to know when end of iterable has been reached
            raise IndexError(f"Index value of '{index}' is not in range of size '({-length}:)0:{length - 1}'")

        if index < 0:
            index = index % length

        return index

    def _wraparound_index(self, index: int) -> int:
        return index % len(self)

    def len_non_empty(self) -> int:
        length: int = 0

        if self._initialized:
            length = _count_nodes(start=self._head.next, end=self._head, dont_count=EMPTY)

        return length

    def __eq__(self, other: Self) -> bool:
        """
        This equality comparison depends on comparison methods of object types in the list.
        """

        # TODO: add tests for this method

        has_same_initialization: bool = self._initialized is other._initialized
        has_same_lengths: bool = len(self) == len(other)
        has_same_connections: bool = False

        logging.debug(f"cdll:__eq__: init self: {self._initialized}")
        logging.debug(f"cdll:__eq__: init other: {other._initialized}")
        logging.debug(f"cdll:__eq__: initialize same?: {has_same_initialization}")

        logging.debug(f"cdll:__eq__: length self: {len(self)}")
        logging.debug(f"cdll:__eq__: lengths other: {len(other)}")
        logging.debug(f"cdll:__eq__: lengths same?: {has_same_lengths}")

        if has_same_initialization and has_same_lengths:
            connections_compared: list = []

            for i in range(len(self)):
                # logging.debug(f"cdll:__eq__: self @ {i}: {self[i]}")
                # logging.debug(f"cdll:__eq__: other @ {i}: {other[i]}")

                connections_compared.append(self[i] == other[i])

            has_same_connections = all(connections_compared)

        logging.debug(f"cdll:__eq__: connections same?: {has_same_connections}")

        return has_same_initialization and \
               has_same_lengths and \
               has_same_connections

    def _eq_connection_types(self, other: Self) -> bool:
        # TODO: add tests for this method

        has_same_initialization: bool = self._initialized is other._initialized
        has_same_lengths: bool = len(self) == len(other)
        has_same_connections_types: bool = False

        logging.debug(f"cdll:__eq__: init self: {self._initialized}")
        logging.debug(f"cdll:__eq__: init other: {other._initialized}")
        logging.debug(f"cdll:__eq__: initialize same?: {has_same_initialization}")

        logging.debug(f"cdll:__eq__: length self: {len(self)}")
        logging.debug(f"cdll:__eq__: lengths other: {len(other)}")
        logging.debug(f"cdll:__eq__: lengths same?: {has_same_lengths}")

        if has_same_lengths:
            connections_compared: list = []

            for index in range(len(self)):
                # logging.debug(f"cdll:__eq__: self @ {index}: {self[index]}")
                # logging.debug(f"cdll:__eq__: other @ {index}: {other[index]}")

                connections_compared.append(isinstance(self[index], type(other[index])))

            has_same_connections_types = all(connections_compared)

        logging.debug(f"cdll:__eq__: connections same?: {has_same_connections_types}")

        return has_same_initialization and \
               has_same_lengths and \
               has_same_connections_types

    def _eq_rotated_mirrored(self, other: Self, compare_eq: bool = False) -> bool:
        # Uses id for comparison of values, not __eq__

        # TODO: Do I really need the mirrored part of the check?
        # TODO: seems like this is broken when there are multiple items of the same in a list, and it is rotated
        #       then there is no guarantee that the find_first picks the correct of the two
        #       there would have to be a find_all method and a test against all the following items
        #       from each starting point until confirmed match, failure and go to next, or all failure

        # TODO: Improve with options for setting IDENTITY or EQUALITY for comparisons

        self_length: int = len(self)

        if self_length == 0:
            return True

        # Shortcut for when both lists are uninitialized
        if not self._initialized and not other._initialized:
            return True

        has_same_initialization: bool = self._initialized is other._initialized
        has_same_lengths: bool = False
        has_same_items: bool = False

        if has_same_initialization:
            has_same_lengths: bool = self_length == len(other)

        if has_same_lengths:
            mirrored: bool = False
            connection_pair_equality: list[bool] = []

            start_item: Any = self.head
            other_start_index: int

            try:
                other_start_index = other.find_first(data=start_item, compare_eq=compare_eq)
            except ValueNotFoundError:
                return False

            # check start neighbors and their mirroring
            if self_length > 1:
                self_last: Any = self[-1]
                self_second: Any = self[1]

                other_last: Any = other[other._wraparound_index(other_start_index - 1)]
                other_second: Any = other[other._wraparound_index(other_start_index + 1)]

                all_none: bool = self_second is None and self_last is None and \
                                 other_second is None and other_last is None

                if self_second == other_last and self_last == other_second and not all_none:
                    mirrored = True

            connection_pairs: list[(Any, Any)] = []
            for index, element in enumerate(self):
                if mirrored:
                    index_other: int = other._wraparound_index(index=other_start_index - index)
                else:
                    index_other: int = other._wraparound_index(index=other_start_index + index)
                connection_pairs.append((self[index], other[index_other]))

            for element0, element1 in connection_pairs:
                connection_pair_equality.append(element0 == element1)

            has_same_items: bool = all(connection_pair_equality)

        return has_same_initialization and \
               has_same_lengths and \
               has_same_items

    def mirror(self, index: int = 0) -> None:
        # TODO: evaluate if the normalize call can be removed
        index = self._normalize_index(index=index)

        if index < 0:
            raise NegativeIndexError(f"Index '{index}' is not zero or greater")

        if index > 0:
            self._shift_head_forwards(amount=index)

        length: int = len(self)
        pair_amount: int = (length - 1) // 2
        # pairs are first and last remaining indexes after index 0, narrowing inwards,
        # until zero or one unassigned indexes remain
        index_pairs: list[tuple[int, int]] = [(1+index, length-1-index) for index in range(pair_amount)]

        for first, second in index_pairs:
            self.switch(index0=first, index1=second)

        if index > 0:
            self._shift_head_backwards(amount=index)

    def switch(self, index0: int, index1: int) -> None:
        self[index0], self[index1] = self[index1], self[index0]

    # def __getitem__(self, index: int | slice) -> Any | Self[Any]:
    def __getitem__(self, index: int | slice) -> Any:
        wraparound: bool = True
        if isinstance(index, int):
            value: Any = self._data_from_node_at_index(index)
        elif isinstance(index, slice):
            if wraparound:
                value: Self = self._get_slice_with_wraparound(slice_=index)
            else:
                value: Self = self._get_slice(slice_=index)
        else:
            raise ValueError(f"__getitem__ requires an integer or a slice, not a {type(index)}.")
        return value

    def __setitem__(self, index: int, value: Any) -> None:
        self._replace_at_index(index, value)

    # TODO: rename to before_and_after_unique ?
    def previous_and_next(self, data: Any) -> tuple[Any, Any]:
        if len(self) == 0:
            raise EmptyCDLLError("List is empty")
        # TODO: check that list is not shorter than 3 items

        try:
            node: Node = self._node_with_unique(data=data)
        except ValueNotFoundError as exception:
            raise exception
        except MultipleValuesFoundError as exception:
            raise exception

        previous_: Any = node.previous.data
        next_: Any = node.next.data

        return previous_, next_

    def _get_slice(self, slice_: slice) -> Self:
        cdll: CDLL = CDLL()

        start: int
        stop: int
        step: int

        if not slice_.start:
            start = 0
        else:
            start = slice_.start

            if start < -len(self):
                start = 0
            elif start < 0:
                start = self._wraparound_index(index=start)

        if not slice_.stop:
            stop = len(self)
        else:
            stop = slice_.stop

            if stop < -len(self):
                stop = 0
            if stop < 0:
                stop = self._wraparound_index(index=stop)
            elif stop > len(self):
                stop = len(self)

        if not slice_.step:
            step = 1
        else:
            step = slice_.step

        for index in range(start, stop, step):
            cdll.append(data=self[index])

        return cdll

    def _get_slice_with_wraparound(self, slice_: slice) -> Self:
        cdll: CDLL = CDLL()

        start: int
        stop: int
        step: int

        if not slice_.start:
            start = 0
        else:
            start = slice_.start

        if not slice_.stop:
            stop = len(self)
        else:
            stop = slice_.stop

        if not slice_.step:
            step = 1
        else:
            step = slice_.step

        start_wrapped: int = self._wraparound_index(index=start)

        start_after_stop: bool = start_wrapped > stop
        cross_tail_distance: int = len(self) if start_after_stop else 0
        distance_from_start: int = cross_tail_distance - start_wrapped
        distance_to_stop: int = stop - 1
        full_distance: int = distance_from_start + distance_to_stop
        distance: int = full_distance % len(self)

        current_node: Node = self._node_at_index(index=start_wrapped)
        cdll.append(current_node.data)

        for _ in range(0, distance, step):
            for _ in range(step):
                current_node = current_node.next
            cdll.append(current_node.data)

        return cdll

    def opposite(self, data: Any):
        if len(self) % 2 != 0:
            raise UnevenListLengthError(f"No opposite item in list of uneven length.")

        half_length: int = len(self) // 2
        data_index: int = self.find_unique(data=data)
        opposite_index: int = self._wraparound_index(index=data_index + half_length)

        opposite_data: Any = self[opposite_index]
        return opposite_data


CDLLPair = tuple[CDLL, CDLL]
CDLLPairs = list[CDLLPair]


def index_difference_between(cdll0: CDLL,
                             cdll1: CDLL,
                             data: Any,
                             comparison: Comparison) -> int:

    cdll0_index_of_data: int = cdll0.find_unique(data=data, comparison=comparison)
    cdll1_index_of_data: int = cdll1.find_unique(data=data, comparison=comparison)
    index_difference_amount: int = cdll0_index_of_data - cdll1_index_of_data

    return index_difference_amount


if __name__ == '__main__':
    pass
