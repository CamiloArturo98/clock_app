from __future__ import annotations
from typing import Any, Iterator, Optional
from app.domain.models.node import Node


class CircularDoublyLinkedList:
    """
    A circular doubly linked list where:
    - Each node holds prev and next pointers.
    - The last node's next points back to head.
    - The head's prev points to the last node.

    This structure is used in the clock app to store the ring of
    time-frames (seconds 0-59, minutes 0-59, hours 0-23).
    """

    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self._size: int = 0

    # ------------------------------------------------------------------
    # Insertion
    # ------------------------------------------------------------------

    def insert_at_beginning(self, data: Any) -> None:
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            assert self.head.prev is not None
            last = self.head.prev
            new_node.next = self.head
            new_node.prev = last
            last.next = new_node
            self.head.prev = new_node
            self.head = new_node
        self._size += 1

    def insert_at_end(self, data: Any) -> None:
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            assert self.head.prev is not None
            last = self.head.prev
            last.next = new_node
            new_node.prev = last
            new_node.next = self.head
            self.head.prev = new_node
        self._size += 1

    # ------------------------------------------------------------------
    # Deletion
    # ------------------------------------------------------------------

    def delete(self, data: Any) -> bool:
        if self.head is None:
            return False

        current = self.head

        if current.data == data:
            if current.next is self.head:
                self.head = None
            else:
                assert current.next is not None
                assert current.prev is not None
                last = current.prev
                self.head = current.next
                self.head.prev = last
                last.next = self.head
            self._size -= 1
            return True

        while current.next is not self.head:
            assert current.next is not None
            if current.data == data:
                assert current.prev is not None
                current.prev.next = current.next
                current.next.prev = current.prev
                self._size -= 1
                return True
            current = current.next

        if current.data == data:
            assert current.prev is not None
            current.prev.next = self.head
            assert self.head is not None
            self.head.prev = current.prev
            self._size -= 1
            return True

        return False

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def print_list(self) -> None:
        if self.head is None:
            return
        current = self.head
        print(current.data)
        current = current.next
        while current is not self.head:
            assert current is not None
            print(current.data)
            current = current.next

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def search(self, data: Any) -> Optional[Node]:
        if self.head is None:
            return None
        current = self.head
        while True:
            if current.data == data:
                return current
            current = current.next
            if current is self.head:
                break
        return None

    def to_list(self) -> list[Any]:
        result: list[Any] = []
        if self.head is None:
            return result
        current = self.head
        while True:
            result.append(current.data)
            current = current.next
            if current is self.head:
                break
        return result

    def __iter__(self) -> Iterator[Any]:
        if self.head is None:
            return
        current = self.head
        while True:
            yield current.data
            current = current.next
            if current is self.head:
                break

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"CircularDoublyLinkedList({self.to_list()})"