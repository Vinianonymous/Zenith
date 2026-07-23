from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel
)
from PyQt6.QtCore import QTimer, pyqtSignal

class Stopwatch(QWidget):
    cycle_completed = pyqtSignal(int)

    def __init__(self, parent, cycle_time: int, cycle_enabled=False):
        super().__init__()

        self.layout = QGridLayout()
        self.cycle_time = cycle_time
        self.cycle_enabled = cycle_enabled

        self.time_label = QLabel("00:00:00")
        self.layout.addWidget(self.time_label)
        self.setLayout(self.layout)

        self.time_passed = {
            "hours": 0,
            "minutes": 0,
            "seconds": 0,
        }

        self.running = False
        self.timer = QTimer()

        self.timer.timeout.connect(self.update_time)

    def start_stop(self):
        if not self.running:
            self.running = True
            self.timer.start(1000)
        else:
            self.running = False
            self.timer.stop()

    def reset(self):
        for key in self.time_passed:
            self.time_passed[key] = 0

    def update_time(self):
        self.time_passed["seconds"] += 1

        if self.time_passed["seconds"] > 59:
            self.time_passed["minutes"] += 1
            self.time_passed["seconds"] = 0

        if self.time_passed["minutes"] > 59:
            self.time_passed["hours"] += 1
            self.time_passed["minutes"] = 0

        if (
            self.time_passed["minutes"] == self.cycle_time
            and self.time_passed["seconds"] == 0
            and self.cycle_enabled
        ):
            self.cycle_completed.emit(0)

        self.update_label()

    def update_label(self):
        hours = self.time_passed["hours"]
        minutes = self.time_passed["minutes"]
        seconds = self.time_passed["seconds"]

        self.time_label.setText(f"{hours:02}:{minutes:02}:{seconds:02}")


