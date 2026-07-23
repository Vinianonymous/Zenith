from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
QWidget,
QPushButton,
QHBoxLayout,
QLabel,
QDialog,
QGridLayout,
QFrame,
QVBoxLayout
)


class TaskWidget(QWidget):
    delete_requested = pyqtSignal(dict)
    execution_started = pyqtSignal(dict)

    def __init__(self, task: dict):
        super().__init__()

        self.task = task

        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel(task["name"]))

        info_button = QPushButton("Info")
        info_button.clicked.connect(self.show_information)
        layout.addWidget(info_button)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_requested.emit(self.task))
        layout.addWidget(delete_button)

        execute_button = QPushButton("<Execute>")
        execute_button.clicked.connect(self.engage)

        layout.addWidget(execute_button)

    def show_information(self):
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


class TaskFrame(QFrame):
    def __init__(self, logic: Logic):
        super().__init__()

        self.logic = logic

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.logic.tasks_changed.connect(self.refresh)

    def refresh(self, tasks: list):

        for i in reversed(range(self.vbox.count())):
            widget = self.vbox.itemAt(i).widget()

            if widget:
                widget.deleteLater()

        for task in tasks:
            widget = TaskWidget(task)

            widget.delete_requested.connect(self.logic.delete_task)

            widget.execution_started.connect(self.logic.begin_exec)

            self.vbox.addWidget(widget)
