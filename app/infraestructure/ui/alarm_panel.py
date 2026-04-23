from __future__ import annotations
import tkinter as tk
from tkinter import messagebox
from typing import Callable
from app.services.alarm_service import AlarmService, Alarm

# Neon amber palette (matches app.py)
PANEL_BG    = "#0D0D0D"
SECTION_BG  = "#111111"
INPUT_BG    = "#161616"
BORDER      = "#1E1E1E"
NEON        = "#FF9900"
NEON_DIM    = "#C87000"
NEON_BRIGHT = "#FFB340"
LABEL_FG    = "#555555"
WHITE       = "#E8E8E8"
RED         = "#CC2200"
RED_DIM     = "#1A0500"
GREEN       = "#00CC66"
GREEN_DIM   = "#001A0D"
SEL_BG      = "#FF9900"
SEL_FG      = "#000000"


class AlarmPanel(tk.Frame):
    """Modern neon alarm manager panel."""

    def __init__(self, parent: tk.Widget, alarm_service: AlarmService, **kwargs) -> None:
        super().__init__(parent, bg=PANEL_BG, **kwargs)
        self._service = alarm_service
        self._build_ui()
        self._refresh_list()

    def _build_ui(self) -> None:
        title_bar = tk.Frame(self, bg="#0A0A0A")
        title_bar.pack(fill=tk.X)

        tk.Label(
            title_bar,
            text="  ⏰   ALARM  MANAGER",
            bg="#0A0A0A", fg=NEON,
            font=("Courier", 12, "bold"),
            pady=8, anchor="w",
        ).pack(side=tk.LEFT)

        self._count_label = tk.Label(
            title_bar,
            text="0 in ring",
            bg="#0A0A0A", fg=NEON_DIM,
            font=("Courier", 9),
            pady=8,
        )
        self._count_label.pack(side=tk.RIGHT, padx=12)

        input_section = tk.Frame(self, bg=SECTION_BG)
        input_section.pack(fill=tk.X, padx=12, pady=(10, 0))

        row1 = tk.Frame(input_section, bg=SECTION_BG)
        row1.pack(fill=tk.X, padx=10, pady=10)

        self._make_label(row1, "HOUR").grid(row=0, column=0, padx=(0, 4))
        self._hour_var = tk.StringVar(value="07")
        self._make_spinbox(row1, self._hour_var, 0, 23).grid(row=0, column=1, padx=(0, 16))

        self._make_label(row1, "MIN").grid(row=0, column=2, padx=(0, 4))
        self._min_var = tk.StringVar(value="00")
        self._make_spinbox(row1, self._min_var, 0, 59).grid(row=0, column=3, padx=(0, 16))

        self._make_label(row1, "LABEL").grid(row=0, column=4, padx=(0, 4))
        self._label_var = tk.StringVar(value="Wake up")
        entry = tk.Entry(
            row1,
            textvariable=self._label_var,
            width=16,
            bg=INPUT_BG, fg=WHITE,
            insertbackground=NEON,
            relief="flat",
            font=("Courier", 11),
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=NEON,
        )
        entry.grid(row=0, column=5, padx=(0, 16), ipady=4)

        tk.Button(
            row1,
            text="＋  ADD",
            bg=NEON, fg="#000000",
            activebackground=NEON_BRIGHT,
            activeforeground="#000000",
            relief="flat",
            font=("Courier", 10, "bold"),
            padx=14, pady=4,
            cursor="hand2",
            command=self._add_alarm,
        ).grid(row=0, column=6)

        nav_row = tk.Frame(self, bg=PANEL_BG)
        nav_row.pack(fill=tk.X, padx=12, pady=(8, 4))

        nav_left = tk.Frame(nav_row, bg=PANEL_BG)
        nav_left.pack(side=tk.LEFT)

        self._make_nav_btn(nav_left, "◀  PREV", self._prev_alarm).pack(side=tk.LEFT, padx=(0, 6))
        self._make_nav_btn(nav_left, "NEXT  ▶", self._next_alarm).pack(side=tk.LEFT)

        nav_right = tk.Frame(nav_row, bg=PANEL_BG)
        nav_right.pack(side=tk.RIGHT)

        tk.Button(
            nav_right, text="↺  RESET",
            bg=GREEN_DIM, fg=GREEN,
            activebackground="#003319", activeforeground=GREEN,
            relief="flat", font=("Courier", 9, "bold"),
            padx=10, pady=3, cursor="hand2",
            command=self._reset_selected,
        ).pack(side=tk.RIGHT, padx=(6, 0))

        tk.Button(
            nav_right, text="✕  REMOVE",
            bg=RED_DIM, fg=RED,
            activebackground="#330800", activeforeground=RED,
            relief="flat", font=("Courier", 9, "bold"),
            padx=10, pady=3, cursor="hand2",
            command=self._remove_selected,
        ).pack(side=tk.RIGHT)

        list_frame = tk.Frame(self, bg=PANEL_BG)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(4, 12))

        scrollbar = tk.Scrollbar(
            list_frame, orient=tk.VERTICAL,
            bg=PANEL_BG, troughcolor="#0A0A0A",
            activebackground=NEON, width=8,
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._listbox = tk.Listbox(
            list_frame,
            bg=INPUT_BG, fg=NEON,
            selectbackground=SEL_BG, selectforeground=SEL_FG,
            font=("Courier", 11),
            relief="flat", borderwidth=0,
            activestyle="none",
            yscrollcommand=scrollbar.set,
            height=5,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=NEON,
        )
        self._listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self._listbox.yview)

    def _make_label(self, parent: tk.Widget, text: str) -> tk.Label:
        return tk.Label(
            parent, text=text,
            bg=SECTION_BG, fg=LABEL_FG,
            font=("Courier", 8, "bold"),
        )

    def _make_spinbox(self, parent: tk.Widget, var: tk.StringVar,
                      from_: int, to: int) -> tk.Spinbox:
        return tk.Spinbox(
            parent, from_=from_, to=to,
            textvariable=var, width=4, format="%02.0f",
            bg=INPUT_BG, fg=NEON,
            buttonbackground=INPUT_BG,
            insertbackground=NEON,
            relief="flat",
            font=("Courier", 11, "bold"),
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=NEON,
        )

    def _make_nav_btn(self, parent: tk.Widget, text: str, cmd: Callable[[], None]) -> tk.Button:
        return tk.Button(
            parent, text=text,
            bg=INPUT_BG, fg=NEON,
            activebackground="#1E1E1E", activeforeground=NEON_BRIGHT,
            relief="flat", font=("Courier", 9, "bold"),
            padx=10, pady=3, cursor="hand2",
            command=cmd,
        )

    def _add_alarm(self) -> None:
        try:
            hour   = int(self._hour_var.get())
            minute = int(self._min_var.get())
        except ValueError:
            messagebox.showerror("Error", "Hour and minute must be numbers.")
            return
        if not (0 <= hour <= 23) or not (0 <= minute <= 59):
            messagebox.showerror("Error", "Hour: 0-23  |  Minute: 0-59")
            return
        label = self._label_var.get().strip() or "Alarm"
        self._service.add_alarm(hour, minute, label)
        self._refresh_list()

    def _remove_selected(self) -> None:
        sel = self._listbox.curselection()
        if not sel:
            return
        alarms = self._service.get_all()
        if sel[0] < len(alarms):
            self._service.remove_alarm(alarms[sel[0]])
            self._refresh_list()

    def _reset_selected(self) -> None:
        sel = self._listbox.curselection()
        if not sel:
            return
        alarms = self._service.get_all()
        if sel[0] < len(alarms):
            self._service.reset_alarm(alarms[sel[0]])
            self._refresh_list()

    def _next_alarm(self) -> None:
        alarm = self._service.next_alarm()
        if alarm:
            self._highlight(alarm)

    def _prev_alarm(self) -> None:
        alarm = self._service.prev_alarm()
        if alarm:
            self._highlight(alarm)

    def _highlight(self, alarm: Alarm) -> None:
        alarms = self._service.get_all()
        if alarm in alarms:
            idx = alarms.index(alarm)
            self._listbox.selection_clear(0, tk.END)
            self._listbox.selection_set(idx)
            self._listbox.see(idx)

    def _refresh_list(self) -> None:
        self._listbox.delete(0, tk.END)
        for alarm in self._service.get_all():
            icon = "✓" if alarm.fired else ("●" if alarm.active else "○")
            self._listbox.insert(tk.END, f"   {icon}   {alarm}")
        total = self._service.count()
        self._count_label.config(text=f"{total} in ring")