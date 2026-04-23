from __future__ import annotations
from typing import Final, Tuple


class TimeFormatter:
    """Formats integer time units into zero-padded display strings."""

    _PAD_WIDTH: Final[int] = 2

    @classmethod
    def pad(cls, value: int) -> str:
        """Return a 2-digit zero-padded string for any 0-99 value."""
        return f"{value:0{cls._PAD_WIDTH}d}"

    @classmethod
    def to_display(cls, hours: int, minutes: int, seconds: int) -> str:
        """Return a HH:MM:SS formatted string in 24-hour mode."""
        return (
            f"{cls.pad(hours)}:"
            f"{cls.pad(minutes)}:"
            f"{cls.pad(seconds)}"
        )

    @classmethod
    def to_12h(cls, hours: int, minutes: int, seconds: int) -> Tuple[str, str]:
        """
        Return a (HH:MM:SS, period) tuple in 12-hour format.
        """
        period: Final[str] = "AM" if hours < 12 else "PM"
        h12: int = hours % 12 or 12
        time_str: str = cls.to_display(h12, minutes, seconds)
        return time_str, period

    @staticmethod
    def date_string(day_name: str, day: int, month_abbr: str, year: int) -> str:
        """Return a formatted date string e.g. 'MONDAY  21 APR 2026'."""
        return f"{day_name.upper()}  {day:02d} {month_abbr.upper()} {year}"