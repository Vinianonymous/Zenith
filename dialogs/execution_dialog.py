from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton
from widgets import Stopwatch
class ExecutionPopup:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.logic.start_doing.connect(self.start)

    def start(self, task: dict):

        def finish(task):

            self.main_window.logic.delete_task(task)

            dialog.deleteLater()

        dialog = QDialog(self.main_window)

        layout = QGridLayout()

        dialog.setLayout(layout)

        self.time_spent = Stopwatch(self, 0)

        self.time_spent.start_stop()

        layout.addWidget(self.time_spent)

        task_name = QLabel(f"Executing: {task['name']}")

        layout.addWidget(task_name)

        cancel_button = QPushButton("Cancel")

        cancel_button.clicked.connect(dialog.deleteLater)

        layout.addWidget(cancel_button)

        finish_button = QPushButton("Finish")

        finish_button.clicked.connect(lambda: finish(task))

        layout.addWidget(finish_button)

        dialog.exec()

