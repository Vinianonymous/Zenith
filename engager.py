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
from PyQt6.QtCore import QObject, pyqtSignal
from uuid import uuid4


# ── Business Logic ─────────────────────────────────────────────────────────────
# Logic knows nothing about any widget. It only manages the task list
# and announces changes via signals.


class Logic(QObject):
    tasks_changed = pyqtSignal(list)  # emitted after every add / delete
    exec_started = pyqtSignal()  # emitted when the user hits Begin

    def __init__(self):
        super().__init__()
        self.tasks = []

    def addTask(self, task: dict):
        self.tasks.append(task)
        self.tasks_changed.emit(list(self.tasks))

    def deleteTask(self, task: dict):
        self.tasks.remove(task)
        self.tasks_changed.emit(list(self.tasks))

    def beginExec(self):
        self.exec_started.emit()


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
    date.setCalendarPopup(True)
    date.setDisplayFormat("yyyy-MM-dd")
    layout.addWidget(date, 3, 2, 1, 2)

    def confirm():
        pop_up.task = {
            "name": name.text(),
            "desc": desc.toPlainText(),
            "due": date.date(),
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

        do_button = QPushButton("Begin Task execution!")
        do_button.clicked.connect(self.logic.beginExec)
        layout.addWidget(do_button, 2, 1)

    def promptAddTask(self):
        task = newTaskDialog(self)
        if task:
            self.logic.addTask(task)


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

        self.logic.exec_started.connect(self.onExecStarted)
        self.show()

    def onExecStarted(self):
        # TODO: swap to QStackedWidget execution view here
        print("exec started — swap view here")


def main():
    app = QApplication([])
    main_window = mainWindow()
    app.exec()


if __name__ == "__main__":
    main()
