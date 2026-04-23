from __future__ import annotations
import datetime
import time
import tkinter as tk
from tkinter import messagebox

from app.services.clock_service import ClockService
from app.services.alarm_service import AlarmService, Alarm
from app.infraestructure.ui.clock_widget import ClockWidget, BG_COLOR
from app.infraestructure.ui.alarm_panel import AlarmPanel

NEON_AMBER   = "#FF9900"
NEON_DIM     = "#C87000"
NEON_BRIGHT  = "#FFB340"
PANEL_BG     = "#111111"
DIVIDER      = "#1E1E1E"
HEADER_LINE  = "#FF9900"
TEXT_MUTED   = "#555555"


class ClockApp(tk.Tk):

    TICK_MS: int = 16

    def __init__(self) -> None:
        super().__init__()
        self.title("Vintage Clock")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)

        self._clock_service = ClockService()
        self._alarm_service = AlarmService()
        self._alarm_service.subscribe(self._on_alarm_fired)
        self._mode_12h = tk.BooleanVar(value=False)

        self._build_ui()
        self._schedule_tick()

    def _build_ui(self) -> None:
        self._build_header()
        self._build_clock()
        self._build_neon_divider()
        self._build_alarm_section()
        self._build_footer()

    def _build_header(self) -> None:
        header = tk.Frame(self, bg=BG_COLOR)
        header.pack(fill=tk.X, padx=24, pady=(18, 0))

        title_frame = tk.Frame(header, bg=BG_COLOR)
        title_frame.pack(side=tk.LEFT)

        tk.Label(
            title_frame,
            text="VINTAGE  CLOCK",
            bg=BG_COLOR, fg=NEON_AMBER,
            font=("Courier", 18, "bold"),
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="Circular Doubly Linked List",
            bg=BG_COLOR, fg=NEON_DIM,
            font=("Courier", 9),
        ).pack(anchor="w")

        toggle_frame = tk.Frame(header, bg=BG_COLOR)
        toggle_frame.pack(side=tk.RIGHT, anchor="n")

        tk.Label(
            toggle_frame, text="MODE",
            bg=BG_COLOR, fg=TEXT_MUTED,
            font=("Courier", 8),
        ).pack(anchor="e")

        tk.Checkbutton(
            toggle_frame,
            text=" 12H",
            variable=self._mode_12h,
            bg=BG_COLOR, fg=NEON_AMBER,
            selectcolor=BG_COLOR,
            activebackground=BG_COLOR,
            activeforeground=NEON_BRIGHT,
            font=("Courier", 11, "bold"),
            cursor="hand2",
        ).pack(anchor="e")

        tk.Frame(self, bg=HEADER_LINE, height=1).pack(fill=tk.X, pady=(10, 0))

    def _build_clock(self) -> None:
        wrapper = tk.Frame(self, bg=BG_COLOR)
        wrapper.pack()
        self._clock_widget = ClockWidget(wrapper)
        self._clock_widget.pack()

    def _build_neon_divider(self) -> None:
        div = tk.Frame(self, bg=BG_COLOR)
        div.pack(fill=tk.X, padx=20)

        tk.Frame(div, bg="#331A00", height=1).pack(fill=tk.X)
        tk.Frame(div, bg=NEON_AMBER, height=1).pack(fill=tk.X)
        tk.Frame(div, bg="#331A00", height=1).pack(fill=tk.X)

    def _build_alarm_section(self) -> None:
        self._alarm_panel = AlarmPanel(self, self._alarm_service)
        self._alarm_panel.pack(fill=tk.BOTH, expand=True)

    def _build_footer(self) -> None:
        tk.Frame(self, bg=DIVIDER, height=1).pack(fill=tk.X)
        footer = tk.Frame(self, bg="#0A0A0A")
        footer.pack(fill=tk.X)
        tk.Label(
            footer,
            text="  ◆  Jhonatan Mideros  ·  4th Semester  ·  Data Structures  ·  2026  ◆",
            bg="#0A0A0A", fg="#2A2A2A",
            font=("Courier", 8),
            pady=5,
        ).pack()

    def _schedule_tick(self) -> None:
        self._tick()
        self.after(self.TICK_MS, self._schedule_tick)

    def _tick(self) -> None:
        now = time.time()
        dt = datetime.datetime.fromtimestamp(now)

        h = dt.hour
        m = dt.minute
        s = dt.second + (dt.microsecond / 1_000_000)

        date_str = dt.strftime("%A  %d  %B  %Y").upper()

        self._clock_widget.update_time(h, m, s, date_str, self._mode_12h.get())
        self._alarm_service.check_alarms(dt.hour, dt.minute, dt.second)

    def _on_alarm_fired(self, alarm: Alarm) -> None:
        self._alarm_panel._refresh_list()
        self.after(0, lambda: messagebox.showinfo(
            "⏰  ALARM",
            f"  {alarm.hour:02d}:{alarm.minute:02d}  —  {alarm.label}",
        ))