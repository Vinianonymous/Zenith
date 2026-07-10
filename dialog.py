from uuid import uuid4
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QDate, QTimer, QUrl
from PyQt6.QtWidgets import (
    QCalendarWidget,
    QDateEdit,
    QDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QWidget,
    QGridLayout
)

class stopwatch(QWidget):
    def __init__(self, parent, cycleTime, cycleEnabled=True):
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

        self.audio = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio)
        self.player.setSource(QUrl.fromLocalFile("alarm.mp3"))

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

        self.updateLabel()

        if self.cycle_enabled and self.timePassed["minutes"] % self.cycle_time == 0 and self.timePassed["seconds"] == 0:
            self.player.play()

    def updateLabel(self):
        hours = self.timePassed["hours"]
        minutes = self.timePassed["minutes"]
        seconds = self.timePassed["seconds"]
        self.timeLabel.setText(f"{hours:02}:{minutes:02d}:{seconds:02d}")



def newTaskDialog(parent) -> dict | None:
    pop_up = QDialog(parent)
    pop_up.setGeometry(0, 0, 500, 400)
    layout = QGridLayout()
    pop_up.setLayout(layout)

    layout.addWidget(QLabel("Task Name"), 1, 1, 1, 1)
    name = QLineEdit()
    layout.addWidget(name, 1, 2, 1, 2)

    layout.addWidget(QLabel("Task description:"), 2, 1, 1, 1)
    desc = QTextEdit()
    layout.addWidget(desc, 2, 2, 1, 2)

    layout.addWidget(QLabel("Due date:"), 3, 1, 1, 1)
    date = QDateEdit()
    date.setDate(QDate.currentDate())
    date.setCalendarPopup(True)
    date.setDisplayFormat("yyyy-MM-dd")
    layout.addWidget(date, 3, 2, 1, 2)

    def confirm():
        pop_up.task = {
            "name": name.text(),
            "desc": desc.toPlainText(),
            "due": date.date().toString("yyyy-MM-dd"),
            "id": str(uuid4()),
        }
        pop_up.accept()

    cancel = QPushButton("Cancel")
    cancel.clicked.connect(pop_up.reject)
    layout.addWidget(cancel, 4, 1, 1, 1)

    add = QPushButton("Add")
    add.clicked.connect(confirm)
    layout.addWidget(add, 4, 2, 1, 1)

    if pop_up.exec():
        return pop_up.task
    return None

# -- Execution Popup -------------------------------------------------connect
class executionPopup:
    def __init__(self, mw, cycle_time: int, cycle_enabled: bool = True) -> None:
        self.mw = mw
        self.cycle_time = cycle_time
        self.cycle_enabled = cycle_enabled
        self.mw.logic.start_doing.connect(self.start)

    def start(self, task: dict):
        def finish(task):
            self.mw.logic.deleteTask(task)
            dialog.deleteLater()

        dialog = QDialog(self.mw)
        layout = QGridLayout()
        dialog.setLayout(layout)

        self.timeSpent = stopwatch(self, self.cycle_time, self.cycle_enabled)
        self.timeSpent.startStop()
        layout.addWidget(self.timeSpent)
        task_name = QLabel(f"Executing: {task['name']}")
        layout.addWidget(task_name)

        def cancel():
            dialog.deleteLater()

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(lambda: cancel())
        layout.addWidget(cancel_button)

        finish_button = QPushButton("Finish")
        finish_button.clicked.connect(lambda: finish(task))
        layout.addWidget(finish_button)

        dialog.exec()
