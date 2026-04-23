from __future__ import annotations
import datetime
from app.domain.models.circular_doubly_linked_list import CircularDoublyLinkedList
from app.domain.models.node import Node


class ClockService:

    def __init__(self) -> None:
        self._seconds_ring: CircularDoublyLinkedList = CircularDoublyLinkedList()
        self._minutes_ring: CircularDoublyLinkedList = CircularDoublyLinkedList()
        self._hours_ring:   CircularDoublyLinkedList = CircularDoublyLinkedList()

        for s in range(60):
            self._seconds_ring.insert_at_end(s)
        for m in range(60):
            self._minutes_ring.insert_at_end(m)
        for h in range(24):
            self._hours_ring.insert_at_end(h)

        now = datetime.datetime.now()
        self._current_seconds: Node[int] = self._find_node(self._seconds_ring, now.second)
        self._current_minutes: Node[int] = self._find_node(self._minutes_ring, now.minute)
        self._current_hours:   Node[int] = self._find_node(self._hours_ring,   now.hour)


    def tick(self) -> None:
        """Advance clock by one second using CDLL navigation."""
        assert self._current_seconds.next is not None
        self._current_seconds = self._current_seconds.next

        if self._current_seconds.data == 0:
            assert self._current_minutes.next is not None
            self._current_minutes = self._current_minutes.next

            if self._current_minutes.data == 0:
                assert self._current_hours.next is not None
                self._current_hours = self._current_hours.next

    def sync_to_real_time(self) -> None:
        """Optional: use only once at startup or for resync."""
        now = datetime.datetime.now()
        self._current_seconds = self._find_node(self._seconds_ring, now.second)
        self._current_minutes = self._find_node(self._minutes_ring, now.minute)
        self._current_hours   = self._find_node(self._hours_ring,   now.hour)

    @property
    def seconds(self) -> int:
        return self._current_seconds.data

    @property
    def minutes(self) -> int:
        return self._current_minutes.data

    @property
    def hours(self) -> int:
        return self._current_hours.data

    @staticmethod
    def _find_node(ring: CircularDoublyLinkedList, value: int) -> Node[int]:
        node = ring.search(value)
        if node is None:
            raise ValueError(f"Value {value} not found in ring.")
        return node