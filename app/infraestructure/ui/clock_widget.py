from __future__ import annotations
import tkinter as tk
import math
from app.shared.time_formatter import TimeFormatter

BG_COLOR     = "#0D0D0D"
FACE_BG      = "#F7EDD0"
TICK_MAJOR   = "#4A2E00"
TICK_MINOR   = "#9A7040"
NUMERAL_CLR  = "#2A1500"

HOUR_FILL    = "#1A0E00"
HOUR_OUTLINE = "#4A3010"

MIN_FILL     = "#2A1800"
MIN_OUTLINE  = "#5A4020"

SEC_HAND     = "#CC2200"

CENTER_OUTER = "#C8920A"
CENTER_INNER = "#F0C030"

DATE_FG      = "#C8920A"
MODE_FG      = "#FF9900"

ROMAN = {
    1:"I", 2:"II", 3:"III", 4:"IV", 5:"V", 6:"VI",
    7:"VII", 8:"VIII", 9:"IX", 10:"X", 11:"XI", 12:"XII",
}


class VintageClockFace(tk.Canvas):

    SIZE = 360

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        super().__init__(
            parent,
            width=self.SIZE,
            height=self.SIZE,
            bg=BG_COLOR,
            highlightthickness=0,
            **kwargs,
        )
        self._cx = self.SIZE // 2
        self._cy = self.SIZE // 2
        self._r  = 160

        self._draw_face()
        self._create_hands()

    def _draw_face(self) -> None:
        cx, cy, r = self._cx, self._cy, self._r

        self.create_oval(cx-r, cy-r, cx+r, cy+r, fill=FACE_BG, outline="")

        for i in range(60):
            angle = math.radians(i * 6 - 90)
            outer = r - 5
            inner = outer - (12 if i % 5 == 0 else 6)

            self.create_line(
                cx + outer * math.cos(angle),
                cy + outer * math.sin(angle),
                cx + inner * math.cos(angle),
                cy + inner * math.sin(angle),
                fill=TICK_MAJOR if i % 5 == 0 else TICK_MINOR,
                width=2 if i % 5 == 0 else 1,
                capstyle=tk.ROUND,
            )

        num_r = r - 30
        for h in range(1, 13):
            angle = math.radians(h * 30 - 90)
            self.create_text(
                cx + num_r * math.cos(angle),
                cy + num_r * math.sin(angle),
                text=ROMAN[h],
                fill=NUMERAL_CLR,
                font=("Georgia", 12, "bold"),
            )

    def _create_hands(self) -> None:
        self._hour_hand = self.create_polygon(
            0,0,0,0,0,0,0,0,0,0,
            fill=HOUR_FILL,
            outline=HOUR_OUTLINE,
            width=1,
            joinstyle=tk.ROUND,
        )

        self._min_hand = self.create_polygon(
            0,0,0,0,0,0,0,0,0,0,
            fill=MIN_FILL,
            outline=MIN_OUTLINE,
            width=1,
            joinstyle=tk.ROUND,
        )

        self._sec_hand = self.create_line(
            0,0,0,0,
            fill=SEC_HAND,
            width=2,
            capstyle=tk.ROUND,
        )

        cx, cy = self._cx, self._cy
        self.create_oval(cx-7, cy-7, cx+7, cy+7, fill=CENTER_OUTER, outline="")
        self.create_oval(cx-4, cy-4, cx+4, cy+4, fill=CENTER_INNER, outline="")

    def update_hands(self, hours: int, minutes: int, seconds: float) -> None:
        cx, cy, r = self._cx, self._cy, self._r

        h_angle = math.radians((hours % 12 + minutes/60 + seconds/3600) * 30 - 90)
        m_angle = math.radians((minutes + seconds/60) * 6 - 90)
        s_angle = math.radians(seconds * 6 - 90)

        self._update_hour(cx, cy, h_angle, r)
        self._update_min(cx, cy, m_angle, r)

        self.coords(
            self._sec_hand,
            cx, cy,
            cx + r*0.85 * math.cos(s_angle),
            cy + r*0.85 * math.sin(s_angle),
        )

    def _update_hour(self, cx, cy, angle, r):
        length = r * 0.45
        back   = r * 0.12
        width  = 10

        self.coords(
            self._hour_hand,
            *self._leaf_shape(cx, cy, angle, length, back, width)
        )

    def _update_min(self, cx, cy, angle, r):
        length = r * 0.70
        back   = r * 0.10
        width  = 7

        self.coords(
            self._min_hand,
            *self._leaf_shape(cx, cy, angle, length, back, width)
        )

    def _leaf_shape(self, cx, cy, angle, length, back, width):
        perp = angle + math.pi / 2

        tip = (
            cx + length * math.cos(angle),
            cy + length * math.sin(angle)
        )

        mid = (
            cx + (length * 0.6) * math.cos(angle),
            cy + (length * 0.6) * math.sin(angle)
        )

        base = (
            cx - back * math.cos(angle),
            cy - back * math.sin(angle)
        )

        lx = width * math.cos(perp)
        ly = width * math.sin(perp)

        return [
            tip[0], tip[1],
            mid[0] + lx, mid[1] + ly,
            base[0] + lx, base[1] + ly,
            base[0] - lx, base[1] - ly,
            mid[0] - lx, mid[1] - ly,
        ]


class ClockWidget(tk.Frame):

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        super().__init__(parent, bg=BG_COLOR, **kwargs)

        self._face = VintageClockFace(self)
        self._face.pack()

        self._date_label = tk.Label(self, bg=BG_COLOR, fg=DATE_FG)
        self._date_label.pack()

        self._mode_label = tk.Label(self, bg=BG_COLOR, fg=MODE_FG)
        self._mode_label.pack()

    def update_time(
        self,
        hours: int, minutes: int, seconds: int,
        date_str: str, mode_12h: bool = False,
    ) -> None:
        import datetime

        now = datetime.datetime.now()
        seconds_precise = now.second + now.microsecond / 1_000_000

        if mode_12h:
            _, period = TimeFormatter.to_12h(hours, minutes, int(seconds))
            self._mode_label.config(text=period)
        else:
            self._mode_label.config(text="24H")

        self._face.update_hands(hours, minutes, seconds_precise)
        self._date_label.config(text=date_str)