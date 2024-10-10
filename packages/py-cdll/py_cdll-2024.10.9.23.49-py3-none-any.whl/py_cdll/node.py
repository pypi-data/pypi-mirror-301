from typing import Any

EXCEPT = object()


class Node:
    def __init__(self, data):
        self.data = data
        self.next: Node | None = None
        self.previous: Node | None = None


# TODO: refactor dont_count into a ?container? that can hold multiple items
def _count_nodes(start: Node, end: Node, dont_count: Any = EXCEPT) -> int:
    length: int = 0

    if start.data != dont_count:
        length += 1

    while start != end:
        if start.data != dont_count:
            length += 1
        start = start.next

    return length
