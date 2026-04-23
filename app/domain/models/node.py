from __future__ import annotations
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class Node(Generic[T]):
    """
    A single node in a doubly circular linked list.

    Attributes:
        data: The value stored in this node.
        prev: Reference to the previous node in the circular chain.
        next: Reference to the next node in the circular chain.
    """

    def __init__(self, data: T) -> None:
        self.data: T = data
        self.prev: Optional[Node[T]] = None
        self.next: Optional[Node[T]] = None

    def __repr__(self) -> str:
        return f"Node({self.data!r})"