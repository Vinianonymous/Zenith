from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtCore import QTimer, QUrl, pyqtSignal


class stopwatch(QWidget):
    cycleCompleted = pyqtSignal(int)
    def __init__(self, parent, cycleTime: int, cycleEnabled=False):
        super().__init__()
        self.layout = QGridLayout()
        self.cycle_time = cycleTime
        self.cycle_enabled = cycleEnabled

        self.timeLabel = QLabel("00:00:00")
        self.layout.addWidget(self.timeLabel)
        self.setLayout(self.layout)
        self.timePassed = {"hours": 0, "minutes": 0, "seconds": 0}
        self.running = False
        self.timer = QTimer()

        self.timer.timeout.connect(self.updateTime)

    def startStop(self):
        if not self.running:
            self.running = True
            self.timer.start(1000)
        else:
            self.running = False
            self.timer.stop()

    def reset(self):
        for key in self.timePassed:
            self.timePassed[key] = 0

    def updateTime(self):
        self.timePassed["seconds"] += 1
        if self.timePassed["seconds"] > 59:
            self.timePassed["minutes"] += 1
            self.timePassed["seconds"] = 0
        if self.timePassed["minutes"] > 59:
            self.timePassed["hours"] += 1
            self.timePassed["minutes"] = 0

        if self.timePassed["minutes"] == self.cycle_time and self.timePassed["seconds"] == 0 and self.cycle_enabled:
            self.cycleCompleted.emit(0)

        self.updateLabel()


    def updateLabel(self):
        hours = self.timePassed["hours"]
        minutes = self.timePassed["minutes"]
        seconds = self.timePassed["seconds"]
        self.timeLabel.setText(f"{hours:02}:{minutes:02d}:{seconds:02d}")
