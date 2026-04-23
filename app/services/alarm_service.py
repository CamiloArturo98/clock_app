from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Optional

from app.domain.models.circular_doubly_linked_list import CircularDoublyLinkedList
from app.domain.models.node import Node


@dataclass(slots=True)
class Alarm:
    hour: int
    minute: int
    label: str = "Alarm"
    active: bool = True
    fired: bool = False

    def matches(self, hour: int, minute: int, second: int) -> bool:
        return (
            self.active
            and not self.fired
            and second == 0
            and self.hour == hour
            and self.minute == minute
        )

    def reset(self) -> None:
        self.fired = False

    def __str__(self) -> str:
        status = "ON " if self.active and not self.fired else "OFF"
        return f"[{status}]  {self.hour:02d}:{self.minute:02d}  —  {self.label}"


class AlarmService:

    def __init__(self) -> None:
        self._alarm_ring: CircularDoublyLinkedList = CircularDoublyLinkedList()
        self._observers: list[Callable[[Alarm], None]] = []
        self._cursor: Optional[Node[Alarm]] = None

    # ------------------------------------------------------------------
    # Observer pattern
    # ------------------------------------------------------------------

    def subscribe(self, callback: Callable[[Alarm], None]) -> None:
        self._observers.append(callback)

    def unsubscribe(self, callback: Callable[[Alarm], None]) -> None:
        if callback in self._observers:
            self._observers.remove(callback)

    def _notify(self, alarm: Alarm) -> None:
        for callback in self._observers:
            callback(alarm)

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def add_alarm(self, hour: int, minute: int, label: str = "Alarm") -> None:
        alarm = Alarm(hour=hour, minute=minute, label=label)
        self._alarm_ring.insert_at_end(alarm)
        if self._cursor is None and self._alarm_ring.head is not None:
            self._cursor = self._alarm_ring.head  # type: ignore[assignment]

    def remove_alarm(self, alarm: Alarm) -> bool:
        result = self._alarm_ring.delete(alarm)
        self._cursor = self._alarm_ring.head  # type: ignore[assignment]
        return result

    def toggle_alarm(self, alarm: Alarm) -> None:
        alarm.active = not alarm.active

    def reset_alarm(self, alarm: Alarm) -> None:
        alarm.reset()

    def get_all(self) -> list[Alarm]:
        return list(self._alarm_ring)

    def count(self) -> int:
        return len(self._alarm_ring)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def next_alarm(self) -> Optional[Alarm]:
        if self._cursor is None:
            return None
        assert self._cursor.next is not None
        self._cursor = self._cursor.next
        return self._cursor.data

    def prev_alarm(self) -> Optional[Alarm]:
        if self._cursor is None:
            return None
        assert self._cursor.prev is not None
        self._cursor = self._cursor.prev
        return self._cursor.data

    @property
    def current_alarm(self) -> Optional[Alarm]:
        if self._cursor is None:
            return None
        return self._cursor.data

    # ------------------------------------------------------------------
    # Tick
    # ------------------------------------------------------------------

    def check_alarms(self, hour: int, minute: int, second: int) -> None:
        for alarm in self._alarm_ring:
            if isinstance(alarm, Alarm) and alarm.matches(hour, minute, second):
                alarm.fired = True
                self._notify(alarm)