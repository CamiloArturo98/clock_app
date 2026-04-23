from __future__ import annotations

from app.infraestructure.ui.app import ClockApp


def main() -> None:
    app = ClockApp()
    app.mainloop()


if __name__ == "__main__":
    main()