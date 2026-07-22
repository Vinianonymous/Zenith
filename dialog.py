from uuid import uuid4
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QDate, QUrl
from PyQt6.QtWidgets import (
    QDateEdit,
    QDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
)
from stopwatch import stopwatch


def cycleWarn(parent, message: str, audioFile: str = "alarm.mp3"):
    player = QMediaPlayer()
    audio_output = QAudioOutput()
    player.setAudioOutput(audio_output)
    audio_file = QUrl.fromLocalFile(audioFile)
    player.setSource(audio_file)

    dialog = QDialog(parent)
    dialog.setWindowTitle("Cycle Completed")
    layout = QGridLayout()
    dialog.setLayout(layout)
    layout.addWidget(QLabel(message), 0, 0)
    ok_button = QPushButton("OK")
    ok_button.clicked.connect(dialog.accept)
    layout.addWidget(ok_button, 1, 0)
    dialog.exec()
    player.play()


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
    def __init__(self, mw) -> None:
        self.mw = mw
        self.mw.logic.start_doing.connect(self.start)

    def start(self, task: dict):
        def finish(task):
            self.mw.logic.deleteTask(task)
            dialog.deleteLater()

        dialog = QDialog(self.mw)
        layout = QGridLayout()
        dialog.setLayout(layout)

        self.timeSpent = stopwatch(self, 0, cycleEnabled=False)
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
