import pytest

from src.py_cdll.circular_doubly_linked_list import CDLL, EMPTY, \
    Connectivity
from src.py_cdll.node import Node
from src.py_cdll.compare import Comparison
from src.py_cdll.exceptions import InputNotIterableError, EmptyCDLLError, \
    MultipleValuesFoundError, ValueNotFoundError, NoAdjacentValueError, FirstValueNotFoundError, \
    SecondValueNotFoundError, ValuesNotAdjacentError, NotEmptyTypeError, UnevenListLengthError


########################################################################################################################


def test_init_without_data_length_empty_success():
    # Setup
    length: int = 3
    list0: CDLL = CDLL(empty_length=length)

    # Validation
    assert len(list0) == length
    assert list0[0] is EMPTY
    assert list0[1] is EMPTY
    assert list0[2] is EMPTY
    with pytest.raises(IndexError):
        _ = list0[3]


def test_init_with_data_length_empty_success():
    # Setup
    data0: str = "data0"
    length: int = 3
    list0: CDLL = CDLL(data=[data0], empty_length=length)

    # Validation
    assert len(list0) == length
    assert list0[0] is data0
    assert list0[1] is EMPTY
    assert list0[2] is EMPTY


def test_init_data_list_empty_success():
    # Setup
    datas0: list = []

    # Execution
    list0: CDLL = CDLL(data=datas0)

    # Validation
    assert len(list0) == 0


def test_init_data_list_one_item_success():
    # Setup
    data0: str = "data0"
    datas0: list = [data0]

    # Execution
    list0: CDLL = CDLL(data=datas0)

    # Validation
    assert len(list0) == 1


def test_init_data_list_four_items_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    datas0: list = [data0, data1, data2, data3]

    # Execution
    list0: CDLL = CDLL(data=datas0)

    # Validation
    assert len(list0) == 4


def test_init_data_list_three_items_with_length_six_success():
    # Setup
    length0: int = 6
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    datas0: list = [data0, data1, data2]

    # Execution
    list0: CDLL = CDLL(data=datas0, empty_length=length0)

    # Validation
    assert len(list0) == 6


########################################################################################################################


def test_get_length_of_empty_list_success():
    # Setup
    cdl_list: CDLL = CDLL()

    # Validation
    assert len(cdl_list) == 0


def test_length_with_one_item_success():
    # Setup
    list0: CDLL = CDLL(data=["data"])

    # Validation
    assert len(list0) == 1


def test_length_with_six_items_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    data5: str = "data5"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)
    list0.append(data5)

    # Validation
    assert len(list0) == 6


def test_length_with_111_items_success():
    # Setup
    data: range = range(111)
    list0: CDLL = CDLL()
    [list0.append(n) for n in data]

    # Validation
    assert len(list0) == 111


########################################################################################################################


def test_repr_with_no_data_success():
    # Setup
    list0: CDLL = CDLL()

    # Validation
    assert list0.__repr__() == "[]"


########################################################################################################################


def test_get_head_of_empty_list_failure():
    # Setup
    cdl_list: CDLL = CDLL()

    # Validation
    with pytest.raises(EmptyCDLLError):
        _ = cdl_list.head


def test_get_head_of_list_after_init_success():
    # Setup
    data: str = "data"
    list0 = CDLL(data=[data])

    # Validation
    assert list0.head == data
    assert list0.end == data


def test_getting_head_success():
    # Setup
    data0 = "data0"
    list0: CDLL = CDLL(data=[data0])

    # Validation
    assert list0.head == data0
    assert list0.end == data0


########################################################################################################################


def test_get_end_of_empty_list_failure():
    # Setup
    cdl_list: CDLL = CDLL()

    # Validation
    with pytest.raises(EmptyCDLLError):
        _ = cdl_list.end


def test_getting_end_success():
    # Setup
    data0: str = "head"
    data1: str = "end"
    list0: CDLL = CDLL(data=[data0])
    list0.append(data1)

    # Validation
    assert list0.head == data0
    assert list0.end == data1


########################################################################################################################


def test_append_to_end_of_empty_list_success():
    # Setup
    data: str = "data"
    list0: CDLL = CDLL()
    list0.append(data)

    # Validation
    assert list0.head == data
    assert list0.end == data


def test_append_to_end_of_list_success():
    # Setup
    head: str = "head"
    data: str = "data"
    list0: CDLL = CDLL(data=[head])
    list0.append(data)

    # Validation
    assert list0.head == head
    assert list0.end == data


def test_get_appended_success():
    # Setup
    head: str = "head"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL(data=[head])
    list0.append(data1)
    list0.append(data2)

    # Validation
    assert list0.head == head
    assert list0.end == data2
    assert list0[0] == head
    assert list0[1] == data1
    assert list0[2] == data2


########################################################################################################################


def test_extend_input_empty_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    datas0: list = []
    datas1: list[str] = [data0, data1, data2]
    list1: CDLL = CDLL(data=datas1)
    list2: CDLL = CDLL(data=datas1)

    # Execution
    list1.extend(data=datas0)

    # Validation
    assert list1 == list2


def test_extend_input_one_item_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    datas0: list[str] = [data3]
    datas1: list[str] = [data0, data1, data2]
    list1: CDLL = CDLL(data=datas1)
    list2: CDLL = CDLL(data=datas1 + datas0)

    # Execution
    list1.extend(data=datas0)

    # Validation
    assert list1 == list2


def test_extend_input_six_items_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    data5: str = "data5"
    data6: str = "data6"
    datas0: list[str] = [data6]
    datas1: list[str] = [data0, data1, data2, data3, data4, data5]
    list1: CDLL = CDLL(data=datas1)
    list2: CDLL = CDLL(data=datas1 + datas0)

    # Execution
    list1.extend(data=datas0)

    # Validation
    assert list1 == list2


def test_extend_input_non_valid_failure():
    # Setup
    data0: int = 9
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    data5: str = "data5"
    datas1: list[str] = [data0, data1, data2, data3, data4, data5]
    list1: CDLL = CDLL(data=datas1)

    # Validation
    with pytest.raises(InputNotIterableError):
        # noinspection PyTypeChecker
        list1.extend(data=data0)


########################################################################################################################


def test_get_index_out_of_range_failure():
    # Setup
    head: str = "head"
    list0: CDLL = CDLL(data=[head])

    # Validation
    assert list0.head == head
    assert list0.end == head
    assert list0[0] == head
    with pytest.raises(IndexError):
        _ = list0[1]


def test_get_index_of_empty_list_out_of_range_failure():
    # Setup
    list0: CDLL = CDLL()

    # Validation
    with pytest.raises(IndexError):
        _ = list0[0]


def test_negative_index_failure():
    # Setup
    data0: int = 100
    data1: int = 200
    data2: int = 300
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Validation
    assert list0[-1] == data2


########################################################################################################################


def test_replace_at_index_zero_with_empty_list_success():
    # Setup
    data0: str = "data0"
    list0: CDLL = CDLL()
    list0[0] = data0

    # Validation
    assert list0.head == data0
    assert list0.end == data0
    assert len(list0) == 1


def test_replace_at_index_with_empty_list_failure():
    # Setup
    data0: str = "data0"
    list0: CDLL = CDLL()

    # Validation
    with pytest.raises(IndexError):
        list0[2] = data0


def test_replace_at_index_greater_than_list_length_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    list0: CDLL = CDLL(data=[data0])
    list0.append(data1)

    # Validation
    with pytest.raises(IndexError):
        list0[2] = data0


def test_replace_at_index_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    list0: CDLL = CDLL(data=[data0])
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    data_new1: str = "inserted1"
    data_new2: str = "inserted2"
    list0[2] = data_new1
    list0[3] = data_new2

    # Validation
    assert list0[0] == data0
    assert list0[1] == data1
    assert list0[2] == data_new1
    assert list0[3] == data_new2
    assert len(list0) == 4


########################################################################################################################


def test_insert_at_index_with_empty_list_success():
    # Setup
    data_new: str = "inserted"
    list0: CDLL = CDLL()
    list0.insert(2, data_new)

    # Validation
    assert list0[0] == data_new
    with pytest.raises(IndexError):
        _ = list0[2]


def test_insert_at_index_greater_than_length_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data_new: str = "inserted"
    list0: CDLL = CDLL(data=[data0])
    list0.append(data1)

    # Validation
    assert list0[0] == data0
    assert list0[1] == data1
    assert list0.head == data0
    assert list0.end == data1
    assert len(list0) == 2
    with pytest.raises(IndexError):
        list0.insert(2, data_new)


def test_insert_at_index_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data_new: str = "inserted"
    list0: CDLL = CDLL(data=[data0])
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.insert(2, data_new)

    # Validation
    assert list0[0] == data0
    assert list0[1] == data1
    assert list0[2] == data_new
    assert list0[3] == data2
    assert list0[4] == data3
    assert len(list0) == 5


def test_insert_at_index_zero_updates_head_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data_new: str = "new_head"
    list0: CDLL = CDLL(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0[0] = data_new

    # Validation
    assert list0.head == data_new


def test_insert_at_index_zero_of_empty_list_success():
    # Setup
    data: str = "data"
    list0: CDLL = CDLL()
    list0[0] = data

    # Validation
    assert list0.head == data


########################################################################################################################


def test_equality_of_unequal_failure():
    # Setup
    list0: CDLL = CDLL("data")
    list1: CDLL = CDLL("other data")

    # Validation
    assert list0 != list1


def test_equality_of_equal_success():
    # Setup
    list0: CDLL = CDLL("data")
    list0.append("more data")
    list1: CDLL = CDLL("data")
    list1.append("more data")

    # Validation
    assert list0 == list1


########################################################################################################################


def test_insert_index_zero_in_empty_list_success():
    # Setup
    data0: str = "data0"
    list0: CDLL = CDLL()

    # Execution
    list0._insert(0, data0)

    # Validation
    assert list0[0] == data0


def test_insert_index_one_in_empty_list_failure():
    # Setup
    data0: str = "data0"
    list0: CDLL = CDLL()

    # Validation
    with pytest.raises(IndexError):
        list0._insert(1, data0)


def test_insert_index_zero_update_head_next_prev_connections_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    new_data: str = "new_data"
    list0: CDLL = CDLL(data=[data0])
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)
    list0._insert(0, new_data)

    # Validation
    assert list0.head == new_data
    assert list0._head.next.data == data0
    assert list0._head.previous.data == data4
    assert list0._head.next.previous.data == new_data
    assert list0._head.previous.next.data == new_data


########################################################################################################################


def test_replace_at_node_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    new_data: str = "new_data"
    list0: CDLL = CDLL(data=[data0])
    list0.append(data1)
    list0.append(data2)

    # Execution
    list0._replace_node(list0._head.next, Node(new_data))

    # Validation
    assert list0._head.next.data == new_data
    assert list0._head.next.next.data == data2
    assert list0._head.next.previous.data == data0


########################################################################################################################


def test_length_non_empty_with_nothing_success():
    # Setup
    list0: CDLL = CDLL()

    # Validation
    assert list0.len_non_empty() == 0


def test_length_non_empty_with_no_objects_success():
    # Setup
    list0: CDLL = CDLL()

    # Validation
    assert list0.len_non_empty() == 0


def test_length_non_empty_with_all_objects_success():
    # Setup
    list0: CDLL = CDLL()
    list0.append("data0")
    list0.append("data1")
    list0.append("data2")

    # Validation
    assert list0.len_non_empty() == 3


def test_length_non_empty_with_all_empty_success():
    # Setup
    length: int = 15
    list0: CDLL = CDLL(empty_length=length)

    # Validation
    assert list0.len_non_empty() == 0


def test_length_non_empty_with_some_empty_success():
    # Setup
    length: int = 5
    list0: CDLL = CDLL(empty_length=length)
    list0[0] = "data0"
    list0[1] = "data1"
    list0[2] = "data2"

    # Validation
    assert list0.len_non_empty() == 3


########################################################################################################################


def test_clear_empty_list_success():
    # Setup
    list0: CDLL = CDLL()

    # Execution
    list0.clear()

    # Validation
    assert list0._initialized is False
    assert len(list0) == 0
    with pytest.raises(AttributeError):
        _ = list0._head


def test_clear_list_with_empty_content_success():
    # Setup
    length: int = 5
    list0: CDLL = CDLL(empty_length=length)

    # Execution
    list0.clear()

    # Validation
    assert list0._initialized is False
    assert len(list0) == 0
    with pytest.raises(AttributeError):
        _ = list0._head


def test_clear_list_with_content_success():
    # Setup
    list0: CDLL = CDLL()
    list0.append("data0")
    list0.append("data1")
    list0.append("data2")

    # Execution
    list0.clear()

    # Validation
    assert list0._initialized is False
    assert len(list0) == 0
    with pytest.raises(AttributeError):
        _ = list0._head


########################################################################################################################


def test_shift_head_forwards_empty_failure():
    # Setup
    list0: CDLL = CDLL()

    # Validation
    with pytest.raises(AttributeError):
        list0._shift_head_forwards()


def test_shift_head_forwards_with_full_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Execution
    list0._shift_head_forwards()

    # Validation
    assert list0.head == data1
    assert list0.end == data0


def test_shift_head_forwards_multiple_with_full_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Execution
    list0._shift_head_forwards(5)

    # Validation
    assert list0.head == data2
    assert list0.end == data1


def test_shift_head_forwards_zero_amount_with_full_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Validation
    with pytest.raises(ValueError):
        list0._shift_head_forwards(0)


def test_shift_head_forwards_negative_amount_with_full_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Validation
    with pytest.raises(ValueError):
        list0._shift_head_forwards(-1)


########################################################################################################################


def test_shift_head_backwards_empty_failure():
    # Setup
    list0: CDLL = CDLL()

    # Validation
    with pytest.raises(AttributeError):
        list0._shift_head_backwards()


def test_shift_head_backwards_with_full_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Execution
    list0._shift_head_backwards()

    # Validation
    assert list0.head == data2
    assert list0.end == data1


def test_shift_head_backwards_multiple_with_full_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Execution
    list0._shift_head_backwards(5)

    # Validation
    assert list0.head == data1
    assert list0.end == data0


def test_shift_head_backwards_zero_amount_with_full_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Validation
    with pytest.raises(ValueError):
        list0._shift_head_backwards(0)


def test_shift_head_backwards_negative_amount_with_full_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Validation
    with pytest.raises(ValueError):
        list0._shift_head_backwards(-1)


########################################################################################################################


def test_rotate_none_success():
    # Setup
    data0: str = "0"
    data1: str = "1"
    data2: str = "2"
    data3: str = "3"
    data4: str = "4"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)
    list1: CDLL = CDLL()
    list1.append(data0)
    list1.append(data1)
    list1.append(data2)
    list1.append(data3)
    list1.append(data4)

    # Validation
    assert list0 == list1


def test_rotate_positive_one_success():
    # Setup
    data0: str = "0"
    data1: str = "1"
    data2: str = "2"
    data3: str = "3"
    data4: str = "4"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)
    list1: CDLL = CDLL()
    list1.append(data1)
    list1.append(data2)
    list1.append(data3)
    list1.append(data4)
    list1.append(data0)

    # Execution
    list1.rotate(amount=1)

    # Validation
    assert list0 == list1


def test_rotate_positive_two_success():
    # Setup
    data0: str = "0"
    data1: str = "1"
    data2: str = "2"
    data3: str = "3"
    data4: str = "4"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)
    list1: CDLL = CDLL()
    list1.append(data2)
    list1.append(data3)
    list1.append(data4)
    list1.append(data0)
    list1.append(data1)

    # Execution
    list1.rotate(amount=2)

    # Validation
    assert list0 == list1


def test_rotate_negative_one_success():
    # Setup
    data0: str = "0"
    data1: str = "1"
    data2: str = "2"
    data3: str = "3"
    data4: str = "4"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)
    list1: CDLL = CDLL()
    list1.append(data4)
    list1.append(data0)
    list1.append(data1)
    list1.append(data2)
    list1.append(data3)

    # Execution
    list1.rotate(amount=-1)

    # Validation
    assert list0 == list1


def test_rotate_negative_two_success():
    # Setup
    data0: str = "0"
    data1: str = "1"
    data2: str = "2"
    data3: str = "3"
    data4: str = "4"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)
    list1: CDLL = CDLL()
    list1.append(data3)
    list1.append(data4)
    list1.append(data0)
    list1.append(data1)
    list1.append(data2)

    # Execution
    list1.rotate(amount=-2)

    # Validation
    assert list0 == list1


########################################################################################################################


def test_node_with_unique_single_option_single_hit_identity_success():
    # Setup
    data0: str = "data0"
    datas0: list[str] = [data0]
    cdll0: CDLL = CDLL(data=datas0)

    # Execution
    node0: Node = cdll0._node_with_unique(data=data0, comparison=Comparison.IDENTITY)

    # Validation
    assert data0 is node0.data


def test_node_with_unique_single_option_single_hit_equality_success():
    # Setup
    data0: str = "data0"
    data1: str = "data0"
    datas0: list[str] = [data1]
    cdll0: CDLL = CDLL(data=datas0)

    # Execution
    node0: Node = cdll0._node_with_unique(data=data0, comparison=Comparison.EQUALITY)

    # Validation
    assert data0 == node0.data


def test_node_with_unique_multiple_options_multiple_equal_single_hit_identity_success():
    # Setup
    data0: list[str] = ["data0"]
    data1: list[str] = ["data0"]
    data2: list[str] = ["data0"]
    datas0: list[list[str]] = [data1, data2, data0]
    cdll0: CDLL = CDLL(data=datas0)

    # Execution
    node0: Node = cdll0._node_with_unique(data=data0, comparison=Comparison.IDENTITY)

    # Validation
    assert data0 is node0.data


def test_node_with_unique_multiple_options_single_hit_equality_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data0"
    datas0: list[str] = [data1, data2, data3, data4]
    cdll0: CDLL = CDLL(data=datas0)

    # Execution
    node0: Node = cdll0._node_with_unique(data=data0, comparison=Comparison.EQUALITY)

    # Validation
    assert data0 == node0.data


def test_node_with_unique_multiple_options_multiple_hits_identity_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data0"
    datas0: list[str] = [data1, data0, data2, data3, data0, data4]
    cdll0: CDLL = CDLL(data=datas0)

    # Validation
    with pytest.raises(MultipleValuesFoundError):
        cdll0._node_with_unique(data=data0, comparison=Comparison.IDENTITY)


def test_node_with_unique_multiple_options_multiple_hits_equality_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data0"
    datas0: list[str] = [data1, data4, data2, data3, data4, data4]
    cdll0: CDLL = CDLL(data=datas0)

    # Validation
    with pytest.raises(MultipleValuesFoundError):
        cdll0._node_with_unique(data=data0, comparison=Comparison.EQUALITY)


def test_node_with_unique_no_options_no_hits_failure():
    # Setup
    data0: str = "data0"
    datas0: list = []
    cdll0: CDLL = CDLL(data=datas0)

    # Validation
    with pytest.raises(EmptyCDLLError):
        cdll0._node_with_unique(data=data0)


def test_node_with_unique_single_option_no_hits_identity_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    datas0: list = [data1]
    cdll0: CDLL = CDLL(data=datas0)

    # Validation
    with pytest.raises(ValueNotFoundError):
        cdll0._node_with_unique(data=data0, comparison=Comparison.IDENTITY)


def test_node_with_unique_single_option_no_hits_equality_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    datas0: list = [data1]
    cdll0: CDLL = CDLL(data=datas0)

    # Validation
    with pytest.raises(ValueNotFoundError):
        cdll0._node_with_unique(data=data0, comparison=Comparison.EQUALITY)


def test_node_with_unique_multiple_options_no_hits_identity_failure():
    # Setup
    data0: list[str] = ["data0"]
    data1: list[str] = ["data1"]
    data2: list[str] = ["data2"]
    data3: list[str] = ["data0"]
    datas0: list[list[str]] = [data1, data3, data2, data3]
    cdll0: CDLL = CDLL(data=datas0)

    # Validation
    with pytest.raises(ValueNotFoundError):
        cdll0._node_with_unique(data=data0, comparison=Comparison.IDENTITY)


def test_node_with_unique_multiple_options_no_hits_equality_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    datas0: list = [data1, data2, data3]
    cdll0: CDLL = CDLL(data=datas0)

    # Validation
    with pytest.raises(ValueNotFoundError):
        cdll0._node_with_unique(data=data0, comparison=Comparison.EQUALITY)


########################################################################################################################


def test_find_unique_with_empty_list_failure():
    # Setup
    data0 = "data0"
    list0: CDLL = CDLL()

    # Validation
    with pytest.raises(EmptyCDLLError):
        list0.find_unique(data0)


def test_find_unique_with_single_option_single_hit_success():
    # Setup
    data0 = "data0"
    list0: CDLL = CDLL()
    list0.append(data0)

    # Validation
    assert list0.find_unique(data0) == 0


def test_find_unique_with_multiple_options_single_hit_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Validation
    assert list0.find_unique(data1) == 1


def test_find_unique_with_zero_hit_failure():
    # Setup
    data: str = "data"
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Validation
    with pytest.raises(ValueNotFoundError):
        list0.find_unique(data)


def test_find_unique_with_multiple_hits_failure():
    # Setup
    data: str = "data"
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data)
    list0.append(data0)
    list0.append(data)
    list0.append(data1)
    list0.append(data)
    list0.append(data2)
    list0.append(data)

    # Validation
    with pytest.raises(MultipleValuesFoundError):
        list0.find_unique(data)


def test_find_unique_with_single_option_single_hit_compare_equality_success():
    # Setup
    data0 = "data0"
    list0: CDLL = CDLL()
    list0.append(data0)

    # Validation
    assert list0.find_unique(data0, comparison=Comparison.EQUALITY) == 0


def test_find_unique_with_multiple_options_single_hit_compare_equality_success():
    # Setup
    data0: list = [1]
    data1: list = [2]
    data2: list = [3]
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Validation
    assert list0.find_unique(data1, comparison=Comparison.EQUALITY) == 1


def test_find_unique_with_zero_hit_compare_equality_failure():
    # Setup
    data: str = "data"
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Validation
    with pytest.raises(ValueNotFoundError):
        list0.find_unique(data, comparison=Comparison.EQUALITY)


def test_find_unique_with_multiple_hits_compare_equality_failure():
    # Setup
    data: str = "data"
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data)
    list0.append(data0)
    list0.append(data)
    list0.append(data1)
    list0.append(data)
    list0.append(data2)
    list0.append(data)

    # Validation
    with pytest.raises(MultipleValuesFoundError):
        list0.find_unique(data, comparison=Comparison.EQUALITY)


########################################################################################################################

def test_before_unique_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Validation
    assert list0.before_unique(data2) is data1


def test_before_unique_single_entry_list_failure():
    # Setup
    data0: str = "data0"
    list0: CDLL = CDLL()
    list0.append(data0)

    # Validation
    with pytest.raises(NoAdjacentValueError):
        list0.before_unique(data0)


def test_set_before_unique_overwrite_success():
    # Setup
    data: str = "data"
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Execution
    list0.set_before_unique(data0, data)

    # Validation
    assert list0.before_unique(data0) is data


def test_set_before_unique_single_entry_list_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    list0: CDLL = CDLL()
    list0.append(data0)

    # Validation
    with pytest.raises(NoAdjacentValueError):
        list0.set_before_unique(data0, data1)


########################################################################################################################


def test_after_unique_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Validation
    assert list0.after_unique(data2) is data0


def test_after_unique_single_entry_list_failure():
    # Setup
    data0: str = "data0"
    list0: CDLL = CDLL()
    list0.append(data0)

    # Validation
    with pytest.raises(NoAdjacentValueError):
        list0.after_unique(data0)


def test_set_after_unique_overwrite_success():
    # Setup
    data: str = "data"
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Execution
    list0.set_after_unique(data0, data)

    # Validation
    assert list0.after_unique(data0) is data


def test_set_after_unique_single_entry_list_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    list0: CDLL = CDLL()
    list0.append(data0)

    # Validation
    with pytest.raises(NoAdjacentValueError):
        list0.set_after_unique(data0, data1)


########################################################################################################################


def test_ordered_adjacent_correct_order_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    # Validation
    assert list0.ordered(data2, data3) == (data2, data3)


def test_ordered_adjacent_incorrect_order_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    # Validation
    assert list0.ordered(data3, data2) == (data2, data3)


def test_ordered_non_adjacent_correct_order_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    # Validation
    assert list0.ordered(data1, data4) == (data1, data4)


def test_ordered_non_adjacent_incorrect_order_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    # Validation
    assert list0.ordered(data4, data1) == (data1, data4)


########################################################################################################################


def test_ordered_occurrence_both_in_list_order_true_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    datas0: list[str] = [data0, data1, data2, data3]
    cdll0: CDLL = CDLL(data=datas0)

    # Execution
    bool0: bool = cdll0.ordered_occurrence(data_first=data0, data_second=data1)

    # Validation
    assert bool0


def test_ordered_occurrence_both_in_list_order_false_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    datas0: list[str] = [data0, data1, data2, data3]
    cdll0: CDLL = CDLL(data=datas0)

    # Execution
    bool0: bool = cdll0.ordered_occurrence(data_first=data2, data_second=data1)

    # Validation
    assert not bool0


def test_ordered_occurrence_first_not_in_list_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    datas0: list[str] = [data0, data1, data2, data3]
    cdll0: CDLL = CDLL(data=datas0)

    # Validation
    with pytest.raises(FirstValueNotFoundError):
        cdll0.ordered_occurrence(data_first=data4, data_second=data1)


def test_ordered_occurrence_second_not_in_list_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    datas0: list[str] = [data0, data1, data2, data3]
    cdll0: CDLL = CDLL(data=datas0)

    # Validation
    with pytest.raises(SecondValueNotFoundError):
        cdll0.ordered_occurrence(data_first=data1, data_second=data4)


########################################################################################################################


def test_adjacent_with_adjacent_correct_order_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    # Execution
    is_adjacent: bool = list0.adjacent(data2, data3)

    # Validation
    assert is_adjacent


def test_adjacent_with_adjacent_incorrect_order_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    # Validation
    assert list0.adjacent(data4, data3) is True


def test_adjacent_with_non_adjacent_correct_order_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    # Validation
    assert list0.adjacent(data1, data4) is False


def test_adjacent_with_non_adjacent_incorrect_order_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    # Validation
    assert list0.adjacent(data3, data0) is False


########################################################################################################################


def test_adjacency_direction_first_second_next_success():
    # Setup
    cdll0: CDLL = CDLL()
    data0: int = 0
    data1: int = 1
    cdll0.extend(data=[data0, data1])

    # Execution
    connectivity0: Connectivity = cdll0.adjacency_direction(first=data0, second=data1)

    # Validation
    assert connectivity0 is Connectivity.ADJACENT_NEXT


def test_adjacency_direction_second_first_previous_success():
    # Setup
    cdll0: CDLL = CDLL()
    data0: int = 0
    data1: int = 1
    data2: int = 2
    data3: int = 3
    cdll0.extend(data=[data0, data1, data2, data3])

    # Execution
    connectivity0: Connectivity = cdll0.adjacency_direction(first=data0, second=data3)

    # Validation
    assert connectivity0 is Connectivity.ADJACENT_PREVIOUS


def test_adjacency_direction_separate_first_second_failure():
    # Setup
    cdll0: CDLL = CDLL()
    data0: int = 0
    data1: int = 1
    data2: int = 2
    data3: int = 3
    data4: int = 4
    cdll0.extend(data=[data0, data1, data2, data3, data4])

    # Validation
    with pytest.raises(ValuesNotAdjacentError):
        cdll0.adjacency_direction(first=data1, second=data3)


def test_adjacency_direction_separate_second_first_failure():
    # Setup
    cdll0: CDLL = CDLL()
    data0: int = 0
    data1: int = 1
    data2: int = 2
    data3: int = 3
    data4: int = 4
    cdll0.extend(data=[data0, data1, data2, data3, data4])

    # Validation
    with pytest.raises(ValuesNotAdjacentError):
        cdll0.adjacency_direction(first=data4, second=data2)


def test_adjacency_direction_missing_first_failure():
    # Setup
    cdll0: CDLL = CDLL()
    data0: int = 0
    data1: int = 1
    data2: int = 2
    data3: int = 3
    data4: int = 4
    data_missing: str = "missing"
    cdll0.extend(data=[data0, data1, data2, data3, data4])

    # Validation
    with pytest.raises(FirstValueNotFoundError):
        cdll0.adjacency_direction(first=data_missing, second=data2)


def test_adjacency_direction_missing_second_failure():
    # Setup
    cdll0: CDLL = CDLL()
    data0: int = 0
    data1: int = 1
    data2: int = 2
    data3: int = 3
    data4: int = 4
    data_missing: str = "missing"
    cdll0.extend(data=[data0, data1, data2, data3, data4])

    # Validation
    with pytest.raises(SecondValueNotFoundError):
        cdll0.adjacency_direction(first=data2, second=data_missing)


########################################################################################################################

def test_insert_on_empty_with_empty_success():
    # Setup
    list0: CDLL = CDLL(empty_length=1)
    data0: str = "data0"

    # Execution
    list0.insert_on_empty(index=0, data=data0)

    # Validation
    assert list0[0] == data0


def test_insert_on_empty_with_filled_failure():
    # Setup
    list0: CDLL = CDLL(data="data", empty_length=1)
    data0: str = "data0"

    # Validation
    with pytest.raises(NotEmptyTypeError):
        list0.insert_on_empty(index=0, data=data0)


########################################################################################################################


def test_set_to_empty_success():
    # Setup
    list0: CDLL = CDLL()
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    # Execution
    list0.set_to_empty(2)

    # Validation
    assert list0[2] == EMPTY


########################################################################################################################


def test_first_non_empty_no_contents_failure():
    # Setup
    list0: CDLL = CDLL()

    # Validation
    with pytest.raises(EmptyCDLLError):
        list0.first_non_empty()


def test_first_non_empty_all_empty_failure():
    # Setup
    list0: CDLL = CDLL(empty_length=5)

    # Validation
    with pytest.raises(ValueNotFoundError):
        list0.first_non_empty()


def test_first_non_empty_data_first_success():
    # Setup
    data0: str = "data0"
    list0: CDLL = CDLL(data=[data0], empty_length=5)

    # Validation
    assert list0.first_non_empty() == data0


def test_first_non_empty_data_middle_success():
    # Setup
    data3: str = "data3"
    list0: CDLL = CDLL(empty_length=5)
    list0[2] = data3

    # Validation
    assert list0.first_non_empty() == data3


def test_first_non_empty_data_last_success():
    # Setup
    data5: str = "data5"
    list0: CDLL = CDLL(empty_length=5)
    list0[4] = data5

    # Validation
    assert list0.first_non_empty() == data5


########################################################################################################################


def test_replace_unique_present_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data_new: str = "data_new"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Execution
    list0.replace_unique(data1, data_new)

    # Validation
    assert list0[1] is data_new


def test_replace_unique_not_present_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data_find: str = "data_find"
    data_new: str = "data_new"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Validation
    with pytest.raises(ValueNotFoundError):
        list0.replace_unique(data_find, data_new)


def test_replace_unique_multiple_options_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data_new: str = "data_new"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data1)
    list0.append(data2)

    # Validation
    with pytest.raises(MultipleValuesFoundError):
        list0.replace_unique(data1, data_new)


########################################################################################################################


def test_mirror_empty_at_head_success():
    # Setup
    list0: CDLL = CDLL()

    # Validation
    with pytest.raises(IndexError):
        list0.mirror()


def test_mirror_single_item_at_head_success():
    # Setup
    data0: str = "data0"
    list0: CDLL = CDLL(data=[data0])

    # Execution
    list0.mirror()

    # Validation
    assert list0.head == data0


def test_mirror_five_items_at_head_success():
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL(data=[data0])

    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    # Execution
    list0.mirror()

    # Validation
    assert list(list0) == [data0, data4, data3, data2, data1]


def test_mirror_six_items_at_index_two_success():
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    data5: str = "data5"

    list0: CDLL = CDLL(data=[data0])

    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)
    list0.append(data5)

    index0: int = 2

    # Execution
    list0.mirror(index=index0)

    # Validation
    assert list(list0) == [data4, data3, data2, data1, data0, data5]


def test_mirror_six_items_at_index_minus_four_success():
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    data5: str = "data5"

    list0: CDLL = CDLL(data=[data0])

    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)
    list0.append(data5)

    index0: int = -4

    # Execution
    list0.mirror(index=index0)

    # Validation
    assert list(list0) == [data4, data3, data2, data1, data0, data5]


########################################################################################################################


def test_switch_with_empty_index_out_of_bounds_success():
    # Setup
    list0: CDLL = CDLL()

    # Validation
    with pytest.raises(IndexError):
        list0.switch(index0=0, index1=0)


def test_switch_with_index_out_of_bounds_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    list0: CDLL = CDLL(data=[data0])
    list0.append(data1)

    # Validation
    with pytest.raises(IndexError):
        list0.switch(index0=0, index1=2)


def test_switch_with_single_item_success():
    # Setup
    data0: str = "data0"
    list0: CDLL = CDLL(data=[data0])

    # Execution
    list0.switch(index0=0, index1=0)

    # Validation
    assert list0[0] == data0


def test_switch_with_two_items_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    list0: CDLL = CDLL(data=[data0])
    list0.append(data1)

    # Execution
    list0.switch(index0=0, index1=1)

    # Validation
    assert list(list0) == [data1, data0]


def test_switch_with_five_items_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    list0: CDLL = CDLL(data=[data0])
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    # Execution
    list0.switch(index0=1, index1=3)

    # Validation
    assert list(list0) == [data0, data3, data2, data1, data4]


def test_switch_twice_with_five_items_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    list0: CDLL = CDLL(data=[data0])
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    # Execution
    list0.switch(index0=1, index1=3)
    list0.switch(index0=2, index1=3)

    # Validation
    assert list(list0) == [data0, data3, data1, data2, data4]


########################################################################################################################


def test_equality_rotated_mirrored_empty_success():
    # Setup
    cdll0: CDLL = CDLL()
    cdll1: CDLL = CDLL()

    # Execution
    is_equal: bool = cdll0._eq_rotated_mirrored(other=cdll1)

    # Validation
    assert is_equal


def test_equality_rotated_mirrored_one_element_success():
    # Setup
    data0: str = "data0"
    cdll0: CDLL = CDLL(data=data0)
    cdll1: CDLL = CDLL(data=data0)

    # Execution
    is_equal: bool = cdll0._eq_rotated_mirrored(other=cdll1)

    # Validation
    assert is_equal


def test_equality_rotated_mirrored_two_elements_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    cdll0: CDLL = CDLL(data=data0)
    cdll0.append(data=data1)
    cdll1: CDLL = CDLL(data=data0)
    cdll1.append(data=data1)

    # Execution
    is_equal: bool = cdll0._eq_rotated_mirrored(other=cdll1)

    # Validation
    assert is_equal


def test_equality_rotated_mirrored_two_by_two_different_elements_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    cdll0: CDLL = CDLL(data=data0)
    cdll0.append(data=data1)
    cdll1: CDLL = CDLL(data=data2)
    cdll1.append(data=data3)

    # Execution
    is_equal: bool = cdll0._eq_rotated_mirrored(other=cdll1)

    # Validation
    assert not is_equal


def test_equality_rotated_mirrored_five_elements_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    cdll0: CDLL = CDLL(data=data0)
    cdll0.append(data=data1)
    cdll0.append(data=data2)
    cdll0.append(data=data3)
    cdll0.append(data=data4)
    cdll1: CDLL = CDLL(data=data0)
    cdll1.append(data=data1)
    cdll1.append(data=data2)
    cdll1.append(data=data3)
    cdll1.append(data=data4)

    # Execution
    is_equal: bool = cdll0._eq_rotated_mirrored(other=cdll1)

    # Validation
    assert is_equal


def test_equality_rotated_mirrored_two_elements_shifted_one_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    cdll0: CDLL = CDLL(data=[data0])
    cdll0.append(data=data1)
    cdll1: CDLL = CDLL(data=[data1])
    cdll1.append(data=data0)

    # Execution
    is_equal: bool = cdll0._eq_rotated_mirrored(other=cdll1)

    # Validation
    assert is_equal


def test_equality_rotated_mirrored_five_elements_shifted_three_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    cdll0: CDLL = CDLL(data=[data0])
    cdll0.append(data=data1)
    cdll0.append(data=data2)
    cdll0.append(data=data3)
    cdll0.append(data=data4)
    cdll1: CDLL = CDLL(data=[data3])
    cdll1.append(data=data4)
    cdll1.append(data=data0)
    cdll1.append(data=data1)
    cdll1.append(data=data2)

    # Execution
    is_equal: bool = cdll0._eq_rotated_mirrored(other=cdll1)

    # Validation
    assert is_equal


def test_equality_rotated_mirrored_seven_elements_shifted_four_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    data5: str = "data5"
    data6: str = "data6"
    cdll0: CDLL = CDLL(data=[data0])
    cdll0.append(data=data1)
    cdll0.append(data=data2)
    cdll0.append(data=data3)
    cdll0.append(data=data4)
    cdll0.append(data=data5)
    cdll0.append(data=data6)
    cdll1: CDLL = CDLL(data=[data4])
    cdll1.append(data=data5)
    cdll1.append(data=data6)
    cdll1.append(data=data0)
    cdll1.append(data=data1)
    cdll1.append(data=data2)
    cdll1.append(data=data3)

    # Execution
    is_equal: bool = cdll0._eq_rotated_mirrored(other=cdll1)

    # Validation
    assert is_equal


def test_equality_rotated_mirrored_three_elements_shifted_two_and_mirrored_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    cdll0: CDLL = CDLL(data=[data0])
    cdll0.append(data=data1)
    cdll0.append(data=data2)
    cdll1: CDLL = CDLL(data=[data2])
    cdll1.append(data=data1)
    cdll1.append(data=data0)

    # Execution
    is_equal: bool = cdll0._eq_rotated_mirrored(other=cdll1)

    # Validation
    assert is_equal


def test_equality_rotated_mirrored_five_elements_shifted_three_and_mirrored_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    cdll0: CDLL = CDLL(data=[data0])
    cdll0.append(data=data1)
    cdll0.append(data=data2)
    cdll0.append(data=data3)
    cdll0.append(data=data4)
    cdll1: CDLL = CDLL(data=[data3])
    cdll1.append(data=data2)
    cdll1.append(data=data1)
    cdll1.append(data=data0)
    cdll1.append(data=data4)

    # Execution
    is_equal: bool = cdll0._eq_rotated_mirrored(other=cdll1)

    # Validation
    assert is_equal


def test_equality_rotated_mirrored_seven_elements_shifted_five_and_mirrored_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    data5: str = "data5"
    data6: str = "data6"
    cdll0: CDLL = CDLL(data=[data0])
    cdll0.append(data=data1)
    cdll0.append(data=data2)
    cdll0.append(data=data3)
    cdll0.append(data=data4)
    cdll0.append(data=data5)
    cdll0.append(data=data6)
    cdll1: CDLL = CDLL(data=[data5])
    cdll1.append(data=data6)
    cdll1.append(data=data0)
    cdll1.append(data=data1)
    cdll1.append(data=data2)
    cdll1.append(data=data3)
    cdll1.append(data=data4)

    # Execution
    is_equal: bool = cdll0._eq_rotated_mirrored(other=cdll1)

    # Validation
    assert is_equal


########################################################################################################################


def test_find_first_single_element_single_hit_success():
    # Setup
    data0 = "data0"
    list0: CDLL = CDLL()
    list0.append(data0)

    # Validation
    assert list0.find_first(data0) == 0


def test_find_first_multiple_elements_single_hit_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Validation
    assert list0.find_first(data1) == 1


def test_find_first_multiple_elements_no_hits_failure():
    # Setup
    data: str = "data"
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Validation
    with pytest.raises(ValueNotFoundError):
        list0.find_first(data)


def test_find_first_multiple_elements_multiple_hits_success():
    # Setup
    data: str = "data"
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data)
    list0.append(data1)
    list0.append(data)
    list0.append(data2)

    # Validation
    assert list0.find_first(data) == 1
    # with pytest.raises(ValueError):
    #     list0.find_first(data)


########################################################################################################################


def test_normalize_index_value_zero_success():
    # Setup
    values0: range = range(5)
    list0: CDLL = CDLL()
    [list0.append(value) for value in values0]
    index0: int = 0

    # Execution
    index1: int = list0._normalize_index(index=index0)

    # Validation
    assert index0 == index1


def test_normalize_index_value_positive_success():
    # Setup
    values0: range = range(8)
    list0: CDLL = CDLL()
    [list0.append(value) for value in values0]
    index0: int = 4

    # Execution
    index1: int = list0._normalize_index(index=index0)

    # Validation
    assert index0 == index1


def test_normalize_index_value_negative_success():
    # range(11) = 0 1 2 3 4  5  6  7  8  9  10
    # negative indices:     -6 -5 -4 -3 -2 -1

    # Setup
    values0: range = range(11)
    list0: CDLL = CDLL()
    [list0.append(value) for value in values0]
    index0: int = -6
    index1: int = 5

    # Execution
    index2: int = list0._normalize_index(index=index0)

    # Validation
    assert index1 == index2


def test_normalize_index_value_positive_out_of_range_failure():
    # Setup
    values0: range = range(20)
    list0: CDLL = CDLL()
    [list0.append(value) for value in values0]
    index0: int = 25

    # Validation
    with pytest.raises(IndexError):
        list0._normalize_index(index=index0)


def test_normalize_index_value_negative_out_of_range_failure():
    # Setup
    values0: range = range(37)
    list0: CDLL = CDLL()
    [list0.append(value) for value in values0]
    index0: int = -45

    # Validation
    with pytest.raises(IndexError):
        list0._normalize_index(index=index0)


########################################################################################################################


def test_previous_and_next_three_items_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Execution
    previous0, next0 = list0.previous_and_next(data=data1)

    # Validation
    assert previous0 == data0 and next0 == data2


def test_previous_and_next_six_items_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    data5: str = "data5"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)
    list0.append(data5)

    # Execution
    previous0, next0 = list0.previous_and_next(data=data4)

    # Validation
    assert previous0 == data3 and next0 == data5


def test_previous_and_next_two_items_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)

    # Execution
    previous0, next0 = list0.previous_and_next(data=data1)

    # Validation
    assert previous0 == data0 and next0 == data0


def test_previous_and_next_one_item_success():
    # Setup
    data0: str = "data0"
    list0: CDLL = CDLL()
    list0.append(data0)

    # Execution
    previous0, next0 = list0.previous_and_next(data=data0)

    # Validation
    assert previous0 == data0 and next0 == data0


def test_previous_and_next_zero_items_failure():
    # Setup
    data0: str = "data0"
    list0: CDLL = CDLL()

    # Validation
    with pytest.raises(EmptyCDLLError):
        list0.previous_and_next(data=data0)


def test_previous_and_next_four_items_not_found_failure():
    # Setup
    data: str = "data"
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)

    # Validation
    with pytest.raises(ValueNotFoundError):
        list0.previous_and_next(data=data)


def test_previous_and_next_seven_items_multiple_found_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)
    list0.append(data3)
    list0.append(data3)

    # Validation
    with pytest.raises(MultipleValuesFoundError):
        list0.previous_and_next(data=data3)


########################################################################################################################


def test_get_slice_start_to_end_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data0)
    list1.append(data1)
    list1.append(data2)
    list1.append(data3)
    list1.append(data4)

    slice0: slice = slice(None)

    # Execution
    list2: CDLL = list0._get_slice(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_inside_to_end_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data2)
    list1.append(data3)
    list1.append(data4)

    slice0: slice = slice(2, None)

    # Execution
    list2: CDLL = list0._get_slice(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_start_to_inside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data0)
    list1.append(data1)
    list1.append(data2)

    slice0: slice = slice(None, 3)

    # Execution
    list2: CDLL = list0._get_slice(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_inside_to_inside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data2)
    list1.append(data3)

    slice0: slice = slice(2, 4)

    # Execution
    list2: CDLL = list0._get_slice(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_outside_to_inside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()

    slice0: slice = slice(9, 3)

    # Execution
    list2: CDLL = list0._get_slice(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_inside_to_outside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data2)
    list1.append(data3)
    list1.append(data4)

    slice0: slice = slice(2, 9)

    # Execution
    list2: CDLL = list0._get_slice(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_outside_to_outside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()

    slice0: slice = slice(7, 9)

    # Execution
    list2: CDLL = list0._get_slice(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_negative_inside_to_inside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data1)
    list1.append(data2)
    list1.append(data3)

    slice0: slice = slice(-4, 4)

    # Execution
    list2: CDLL = list0._get_slice(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_inside_to_negative_inside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data1)
    list1.append(data2)

    slice0: slice = slice(1, -2)

    # Execution
    list2: CDLL = list0._get_slice(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_negative_inside_to_negative_inside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data2)
    list1.append(data3)

    slice0: slice = slice(-3, -1)

    # Execution
    list2: CDLL = list0._get_slice(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_negative_outside_to_inside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data0)
    list1.append(data1)
    list1.append(data2)

    slice0: slice = slice(-9, 3)

    # Execution
    list2: CDLL = list0._get_slice(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_negative_inside_to_outside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data1)
    list1.append(data2)
    list1.append(data3)
    list1.append(data4)

    slice0: slice = slice(-4, 9)

    # Execution
    list2: CDLL = list0._get_slice(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_negative_outside_to_outside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data0)
    list1.append(data1)
    list1.append(data2)
    list1.append(data3)
    list1.append(data4)

    slice0: slice = slice(-9, 9)

    # Execution
    list2: CDLL = list0._get_slice(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_outside_to_negative_inside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()

    slice0: slice = slice(9, -4)

    # Execution
    list2: CDLL = list0._get_slice(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_inside_to_negative_outside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()

    slice0: slice = slice(2, -9)

    # Execution
    list2: CDLL = list0._get_slice(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_outside_to_negative_outside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()

    slice0: slice = slice(9, -9)

    # Execution
    list2: CDLL = list0._get_slice(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_negative_outside_to_negative_inside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data0)
    list1.append(data1)

    slice0: slice = slice(-9, -3)

    # Execution
    list2: CDLL = list0._get_slice(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_negative_inside_to_negative_outside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()

    slice0: slice = slice(-3, -9)

    # Execution
    list2: CDLL = list0._get_slice(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_negative_outside_to_negative_outside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()

    slice0: slice = slice(-6, -9)

    # Execution
    list2: CDLL = list0._get_slice(slice_=slice0)

    # Validation
    assert list1 == list2


########################################################################################################################


def test_get_slice_with_wraparound_start_to_end_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data0)
    list1.append(data1)
    list1.append(data2)
    list1.append(data3)
    list1.append(data4)

    slice0: slice = slice(None)

    # Execution
    list2: CDLL = list0._get_slice_with_wraparound(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_with_wraparound_inside_to_end_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data2)
    list1.append(data3)
    list1.append(data4)

    slice0: slice = slice(2, None)

    # Execution
    list2: CDLL = list0._get_slice_with_wraparound(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_with_wraparound_start_to_inside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data0)
    list1.append(data1)
    list1.append(data2)

    slice0: slice = slice(None, 3)

    # Execution
    list2: CDLL = list0._get_slice_with_wraparound(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_with_wraparound_inside_to_inside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data2)
    list1.append(data3)

    slice0: slice = slice(2, 4)

    # Execution
    list2: CDLL = list0._get_slice_with_wraparound(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_with_wraparound_outside_to_inside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data4)
    list1.append(data0)
    list1.append(data1)
    list1.append(data2)

    slice0: slice = slice(9, 3)

    # Execution
    list2: CDLL = list0._get_slice_with_wraparound(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_with_wraparound_inside_to_outside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data2)
    list1.append(data3)

    slice0: slice = slice(2, 9)

    # Execution
    list2: CDLL = list0._get_slice_with_wraparound(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_with_wraparound_outside_to_outside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data2)
    list1.append(data3)

    slice0: slice = slice(7, 9)

    # Execution
    list2: CDLL = list0._get_slice_with_wraparound(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_with_wraparound_negative_inside_to_inside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data1)
    list1.append(data2)
    list1.append(data3)

    slice0: slice = slice(-4, 4)

    # Execution
    list2: CDLL = list0._get_slice_with_wraparound(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_with_wraparound_inside_to_negative_inside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data1)
    list1.append(data2)

    slice0: slice = slice(1, -2)

    # Execution
    list2: CDLL = list0._get_slice_with_wraparound(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_with_wraparound_negative_inside_to_negative_inside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data2)
    list1.append(data3)

    slice0: slice = slice(-3, -1)

    # Execution
    list2: CDLL = list0._get_slice_with_wraparound(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_with_wraparound_negative_outside_to_inside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data1)
    list1.append(data2)

    slice0: slice = slice(-9, 3)

    # Execution
    list2: CDLL = list0._get_slice_with_wraparound(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_with_wraparound_negative_inside_to_outside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data1)
    list1.append(data2)
    list1.append(data3)

    slice0: slice = slice(-4, 9)

    # Execution
    list2: CDLL = list0._get_slice_with_wraparound(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_with_wraparound_negative_outside_to_outside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data1)
    list1.append(data2)
    list1.append(data3)

    slice0: slice = slice(-9, 9)

    # Execution
    list2: CDLL = list0._get_slice_with_wraparound(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_with_wraparound_outside_to_negative_inside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data4)
    list1.append(data0)

    slice0: slice = slice(9, -4)

    # Execution
    list2: CDLL = list0._get_slice_with_wraparound(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_with_wraparound_inside_to_negative_outside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data2)
    list1.append(data3)
    list1.append(data4)
    list1.append(data0)

    slice0: slice = slice(2, -9)

    # Execution
    list2: CDLL = list0._get_slice_with_wraparound(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_with_wraparound_outside_to_negative_outside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data4)
    list1.append(data0)

    slice0: slice = slice(9, -9)

    # Execution
    list2: CDLL = list0._get_slice_with_wraparound(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_with_wraparound_negative_outside_to_negative_inside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data1)

    slice0: slice = slice(-9, -3)

    # Execution
    list2: CDLL = list0._get_slice_with_wraparound(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_with_wraparound_negative_inside_to_negative_outside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data2)
    list1.append(data3)
    list1.append(data4)
    list1.append(data0)

    slice0: slice = slice(-3, -9)

    # Execution
    list2: CDLL = list0._get_slice_with_wraparound(slice_=slice0)

    # Validation
    assert list1 == list2


def test_get_slice_with_wraparound_negative_outside_to_negative_outside_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)
    list0.append(data3)
    list0.append(data4)

    list1: CDLL = CDLL()
    list1.append(data4)
    list1.append(data0)

    slice0: slice = slice(-6, -9)

    # Execution
    list2: CDLL = list0._get_slice_with_wraparound(slice_=slice0)

    # Validation
    assert list1 == list2


########################################################################################################################


def test_add_empty_and_empty_success():
    # Setup
    list0: CDLL = CDLL()
    list1: CDLL = CDLL()
    list2: CDLL = CDLL()

    # Execution
    list3: CDLL = list0 + list1

    # Validation
    assert list3 == list2


def test_add_item_and_empty_success():
    # Setup
    data0: str = "data0"
    list0: CDLL = CDLL([data0])
    list1: CDLL = CDLL()
    list2: CDLL = CDLL([data0])

    # Execution
    list3: CDLL = list0 + list1

    # Validation
    assert list3 == list2


def test_add_empty_and_item_success():
    # Setup
    data0: str = "data0"
    list0: CDLL = CDLL()
    list1: CDLL = CDLL([data0])
    list2: CDLL = CDLL([data0])

    # Execution
    list3: CDLL = list0 + list1

    # Validation
    assert list3 == list2


def test_add_item_and_item_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    list0: CDLL = CDLL([data0])
    list1: CDLL = CDLL([data1])
    list2: CDLL = CDLL([data0, data1])

    # Execution
    list3: CDLL = list0 + list1

    # Validation
    assert list3 == list2


def test_add_two_items_and_five_items_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    data5: str = "data5"
    data6: str = "data6"
    list0: CDLL = CDLL([data0, data1])
    list1: CDLL = CDLL([data2, data3, data4, data5, data6])
    list2: CDLL = CDLL([data0, data1, data2, data3, data4, data5, data6])

    # Execution
    list3: CDLL = list0 + list1

    # Validation
    assert list3 == list2


def test_add_three_items_and_four_items_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    data5: str = "data5"
    data6: str = "data6"
    list0: CDLL = CDLL([data0, data1, data2])
    list1: CDLL = CDLL([data3, data4, data5, data6])
    list2: CDLL = CDLL([data0, data1, data2, data3, data4, data5, data6])

    # Execution
    list3: CDLL = list0 + list1

    # Validation
    assert list3 == list2


def test_add_cdll_tuple_failure():
    # Setup
    list0: CDLL = CDLL()
    list1: tuple = tuple()

    # Validation
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        list0 + list1


def test_add_cdll_list_failure():
    # Setup
    list0: CDLL = CDLL()
    list1: list = list()

    # Validation
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        list0 + list1


def test_add_cdll_set_failure():
    # Setup
    list0: CDLL = CDLL()
    list1: set = set()

    # Validation
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        list0 + list1


########################################################################################################################


def test_mul_zero_empty_success():
    # Setup
    multiplier0: int = 0

    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    list1: CDLL = CDLL()

    # Execution
    list2: CDLL = list0 * multiplier0

    # Validation
    assert list1 == list2


def test_mul_one_same_success():
    # Setup
    multiplier0: int = 1

    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    list1: CDLL = CDLL()
    list1.append(data0)
    list1.append(data1)
    list1.append(data2)

    # Execution
    list2: CDLL = list0 * multiplier0

    # Validation
    assert list1 == list2


def test_mul_two_double_success():
    # Setup
    multiplier0: int = 2

    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    list1: CDLL = CDLL()
    list1.append(data0)
    list1.append(data1)
    list1.append(data2)
    list1.append(data0)
    list1.append(data1)
    list1.append(data2)

    # Execution
    list2: CDLL = list0 * multiplier0

    # Validation
    assert list1 == list2


def test_mul_five_quintuple_success():
    # Setup
    multiplier0: int = 5

    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    list1: CDLL = CDLL()
    list1.append(data0)
    list1.append(data1)
    list1.append(data2)
    list1.append(data0)
    list1.append(data1)
    list1.append(data2)
    list1.append(data0)
    list1.append(data1)
    list1.append(data2)
    list1.append(data0)
    list1.append(data1)
    list1.append(data2)
    list1.append(data0)
    list1.append(data1)
    list1.append(data2)

    # Execution
    list2: CDLL = list0 * multiplier0

    # Validation
    assert list1 == list2


def test_mul_minus_one_empty_success():
    # Setup
    multiplier0: int = -1

    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"

    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    list1: CDLL = CDLL()

    # Execution
    list2: CDLL = list0 * multiplier0

    # Validation
    assert list1 == list2


########################################################################################################################


def test_opposite_two_items_from_zero_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"

    list0: CDLL = CDLL()
    list0.append(data=data0)
    list0.append(data=data1)

    # Execution
    data2: str = list0.opposite(data=data0)

    # Validation
    assert data2 == data1


def test_opposite_four_items_from_one_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"

    list0: CDLL = CDLL()
    list0.append(data=data0)
    list0.append(data=data1)
    list0.append(data=data2)
    list0.append(data=data3)

    # Execution
    data4: str = list0.opposite(data=data1)

    # Validation
    assert data4 == data3


def test_opposite_sixteen_items_from_thirteen_across_zero_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    data5: str = "data5"
    data6: str = "data6"
    data7: str = "data7"
    data8: str = "data8"
    data9: str = "data9"
    data10: str = "data10"
    data11: str = "data11"
    data12: str = "data12"
    data13: str = "data13"
    data14: str = "data14"
    data15: str = "data15"

    list0: CDLL = CDLL()
    list0.append(data=data0)
    list0.append(data=data1)
    list0.append(data=data2)
    list0.append(data=data3)
    list0.append(data=data4)
    list0.append(data=data5)
    list0.append(data=data6)
    list0.append(data=data7)
    list0.append(data=data8)
    list0.append(data=data9)
    list0.append(data=data10)
    list0.append(data=data11)
    list0.append(data=data12)
    list0.append(data=data13)
    list0.append(data=data14)
    list0.append(data=data15)

    # Execution
    data16: str = list0.opposite(data=data13)

    # Validation
    assert data16 == data5


def test_opposite_empty_list_data_not_found_error_failure():
    # Setup
    data0: str = "data0"

    list0: CDLL = CDLL()

    # Validation
    with pytest.raises(EmptyCDLLError):
        list0.opposite(data=data0)


def test_opposite_one_item_failure():
    # Setup
    data0: str = "data0"

    list0: CDLL = CDLL()
    list0.append(data=data0)

    # Validation
    with pytest.raises(UnevenListLengthError):
        list0.opposite(data=data0)


def test_opposite_five_items_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data0"
    data2: str = "data0"
    data3: str = "data0"
    data4: str = "data0"

    list0: CDLL = CDLL()
    list0.append(data=data0)
    list0.append(data=data1)
    list0.append(data=data2)
    list0.append(data=data3)
    list0.append(data=data4)

    # Validation
    with pytest.raises(UnevenListLengthError):
        list0.opposite(data=data1)


def test_opposite_thirteen_items_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data0"
    data2: str = "data0"
    data3: str = "data0"
    data4: str = "data0"
    data5: str = "data0"
    data6: str = "data0"
    data7: str = "data0"
    data8: str = "data0"
    data9: str = "data0"
    data10: str = "data0"
    data11: str = "data0"
    data12: str = "data0"

    list0: CDLL = CDLL()
    list0.append(data=data0)
    list0.append(data=data1)
    list0.append(data=data2)
    list0.append(data=data3)
    list0.append(data=data4)
    list0.append(data=data5)
    list0.append(data=data6)
    list0.append(data=data7)
    list0.append(data=data8)
    list0.append(data=data9)
    list0.append(data=data10)
    list0.append(data=data11)
    list0.append(data=data12)

    # Validation
    with pytest.raises(UnevenListLengthError):
        list0.opposite(data=data9)


def test_opposite_six_items_data_not_found_failure():
    # Setup
    data: str = "data"
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    data5: str = "data5"

    list0: CDLL = CDLL()
    list0.append(data=data0)
    list0.append(data=data1)
    list0.append(data=data2)
    list0.append(data=data3)
    list0.append(data=data4)
    list0.append(data=data5)

    # Validation
    with pytest.raises(ValueNotFoundError):
        list0.opposite(data=data)


def test_opposite_six_items_multiple_data_instances_found_failure():
    # Setup
    data: str = "data"
    data0: str = "data0"
    data1: str = "data"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data"
    data5: str = "data5"

    list0: CDLL = CDLL()
    list0.append(data=data0)
    list0.append(data=data1)
    list0.append(data=data2)
    list0.append(data=data3)
    list0.append(data=data4)
    list0.append(data=data5)

    # Validation
    with pytest.raises(MultipleValuesFoundError):
        list0.opposite(data=data)


########################################################################################################################


if __name__ == '__main__':
    pass
