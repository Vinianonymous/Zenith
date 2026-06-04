from PyQt6.QtWidgets import (
    QMainWindow,
    QDialog,
    QGridLayout,
    QApplication,
    QPushButton,
    QWidget,
    QTextEdit,
    QDateEdit,
    QLabel,
    QLineEdit,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import QObject, pyqtSignal, QDate, QTimer
from uuid import uuid4


# ── Business Logic ─────────────────────────────────────────────────────────────
# Logic knows nothing about any widget. It only manages the task list
# and announces changes via signals.


class Logic(QObject):
    tasks_changed = pyqtSignal(list)  # emitted after every add / delete
    start_doing = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.tasks = []

    def addTask(self, task: dict):
        self.tasks.append(task)
        self.tasks_changed.emit(list(self.tasks))

    def deleteTask(self, task: dict):
        self.tasks.remove(task)
        self.tasks_changed.emit(list(self.tasks))

    def beginExec(self, task: dict):
        self.start_doing.emit(task)


# ── Dialog (standalone function) ───────────────────────────────────────────────
# Lives in the UI layer. Returns a task dict or None. No reference to Logic.


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


# ── taskWidget ─────────────────────────────────────────────────────────────────
# Emits delete_requested instead of calling Logic directly.
# No reference to Logic at all.


class taskWidget(QWidget):
    delete_requested = pyqtSignal(dict)
    execution_started = pyqtSignal(dict)

    def __init__(self, task: dict):
        super().__init__()
        self.task = task
        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel(task["name"]))

        info_button = QPushButton("Info")
        info_button.clicked.connect(self.showInformation)
        layout.addWidget(info_button)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_requested.emit(self.task))
        layout.addWidget(delete_button)

        do_button = QPushButton("<Execute>")
        do_button.clicked.connect(self.engage)
        layout.addWidget(do_button)

    def showInformation(self):
        pop_up = QDialog(self)
        layout = QGridLayout()
        pop_up.setLayout(layout)

        layout.addWidget(QLabel("Description:"), 0, 0)
        layout.addWidget(QLabel("Due date:"), 1, 0)
        layout.addWidget(QLabel("Id (Debug):"), 2, 0)

        layout.addWidget(QLabel(self.task["desc"]), 0, 1)
        layout.addWidget(QLabel(str(self.task["due"])), 1, 1)
        layout.addWidget(QLabel(self.task["id"]), 2, 1)

        ok = QPushButton("Acknowledge")
        ok.clicked.connect(pop_up.accept)
        layout.addWidget(ok, 3, 1)
        pop_up.exec()

    def engage(self):
        self.execution_started.emit(self.task)


# ── taskFrame ──────────────────────────────────────────────────────────────────
# Subscribes to Logic.tasks_changed and redraws itself.


class taskFrame(QFrame):
    def __init__(self, logic: Logic):
        super().__init__()
        self.logic = logic
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.logic.tasks_changed.connect(self.refresh)

    def refresh(self, tasks: list):
        for i in reversed(range(self.vbox.count())):
            w = self.vbox.itemAt(i).widget()
            if w:
                w.deleteLater()
        for task in tasks:
            w = taskWidget(task)
            w.delete_requested.connect(self.logic.deleteTask)
            w.execution_started.connect(self.logic.beginExec)
            self.vbox.addWidget(w)


# ── manageFrame ────────────────────────────────────────────────────────────────
# Owns the dialog call. Passes the result to Logic.


class manageFrame(QWidget):
    def __init__(self, logic: Logic, parent=None):
        super().__init__(parent)
        self.logic = logic
        layout = QGridLayout()
        self.setLayout(layout)

        add_button = QPushButton("Add Task")
        add_button.clicked.connect(self.promptAddTask)
        layout.addWidget(add_button, 1, 1)

    def promptAddTask(self):
        task = newTaskDialog(self)
        if task:
            self.logic.addTask(task)


# Timer
class stopwatch(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.layout = QHBoxLayout()

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
        elif self.timePassed["minutes"] > 59:
            self.timePassed["hours"] += 1
            self.timePassed["minutes"] = 0

        self.updateLabel()

    def updateLabel(self):
        hours = self.timePassed["hours"]
        minutes = self.timePassed["minutes"]
        seconds = self.timePassed["seconds"]
        self.timeLabel.setText(f"{hours:02}:{minutes:02d}:{seconds:02d}")


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

        self.timeSpent = stopwatch(self)
        self.timeSpent.startStop()
        layout.addWidget(self.timeSpent)
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


# ── mainWindow ─────────────────────────────────────────────────────────────────
# Single wiring point. Everything connects here.


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logic = Logic()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout()
        central_widget.setLayout(layout)

        self.task_frame = taskFrame(self.logic)
        self.manage_frame = manageFrame(self.logic, parent=self)

        layout.addWidget(self.task_frame, 1, 1)
        layout.addWidget(self.manage_frame, 2, 1)

        self.execution_popup = executionPopup(self)

        self.show()


def main():
    app = QApplication([])
    main_window = mainWindow()
    app.exec()


if __name__ == "__main__":
    main()
