# 🕰️ Vintage Clock App — Circular Doubly Linked List

A desktop clock application built with **Python (Tkinter)** that visually demonstrates the use of a **Circular Doubly Linked List (CDLL)** to model real-world time and alarm systems.

This project combines **data structures**, **clean architecture**, and a **high-quality vintage UI design**.

---

## 📌 Features

### ⏱ Real-Time Clock

* Displays current system time (hours, minutes, seconds)
* Smooth hand movement using microsecond precision
* Supports **12H / 24H mode toggle**

### 🔔 Alarm System

* Add, remove, reset, and toggle alarms
* Visual alarm manager panel
* Observer pattern implementation for alarm triggering

### 🔁 Circular Doubly Linked List (Core Concept)

* Time (seconds, minutes, hours) modeled as circular rings
* Efficient forward/backward traversal
* Used for:

  * Clock time progression
  * Alarm navigation

### 🎨 UI / UX

* Vintage analog clock design
* Roman numerals
* Custom polygon-based clock hands (high precision, non-pixelated)
* Neon-dark modern interface shell

---

## 🧠 Architecture

The project follows a **layered architecture** with separation of concerns:

```
app/
│
├── domain/
│   └── models/
│       ├── node.py
│       └── circular_doubly_linked_list.py
│
├── services/
│   ├── clock_service.py
│   └── alarm_service.py
│
├── infraestructure/
│   └── ui/
│       ├── app.py
│       ├── clock_widget.py
│       └── alarm_panel.py
│
├── shared/
│   └── time_formatter.py
│
main.py
```

### Responsibilities

| Layer                  | Responsibility                    |
| ---------------------- | --------------------------------- |
| **domain**             | Core data structures (CDLL, Node) |
| **services**           | Business logic (time + alarms)    |
| **infraestructure/ui** | GUI (Tkinter components)          |
| **shared**             | Stateless utilities               |

---

## 🔧 Technologies

* Python 3.10+
* Tkinter (native GUI)
* Dataclasses
* Type hints (PEP 484 / modern typing)
* Object-Oriented Design
* Observer Pattern

---

## ▶️ How to Run

```bash
    python main.py
```

Make sure you execute from the project root so imports resolve correctly.

---

## ⚙️ Key Design Decisions

### 1. Circular Doubly Linked List for Time

Instead of using integers directly:

* Each unit (seconds/minutes/hours) is a **node in a circular ring**
* Advancing time = moving to `node.next`
* Natural wrap-around (59 → 0) handled automatically

### 2. Observer Pattern for Alarms

* UI subscribes to alarm events
* Decouples alarm logic from presentation

### 3. High-Fidelity Clock Rendering

* Custom geometry using `Canvas`
* Polygon-based hands (no blur)
* Real-time updates using system clock

---

## 📈 Improvements Implemented

* Smooth hand motion using microseconds
* Anti-pixelation via polygon geometry (no `smooth=True` blur)
* Clean import structure (absolute imports)
* Type-safe design with modern Python typing
* UI separation from logic (maintainable & scalable)

---

## 🚀 Possible Future Enhancements

* Persistent alarms (SQLite / JSON)
* Sound notifications
* Timezone support
* Theme switching (dark/light/vintage variants)
* Packaging as standalone executable

---

## 👨‍💻 Author

**Camilo Bolaños Arturo**
Software Engineering — Data Structures challenge (2026)

---

## 📜 License

This project is for educational purposes.
