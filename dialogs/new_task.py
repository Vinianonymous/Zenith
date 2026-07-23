from PyQt6.QtWidgets import QDialog, QGridLayout, QLineEdit, QLabel, QTextEdit, QDateEdit, QPushButton
from PyQt6.QtCore import QDate
from uuid import uuid4

def new_task_dialog(parent) -> dict | None:

    pop_up = QDialog(parent)

    pop_up.setGeometry(0, 0, 500, 400)

    layout = QGridLayout()

    pop_up.setLayout(layout)

    layout.addWidget(QLabel("Task Name"), 1, 1)

    name_input = QLineEdit()

    layout.addWidget(name_input, 1, 2, 1, 2)

    layout.addWidget(QLabel("Task description:"), 2, 1)

    description_input = QTextEdit()

    layout.addWidget(description_input, 2, 2, 1, 2)

    layout.addWidget(QLabel("Due date:"), 3, 1)

    date_input = QDateEdit()

    date_input.setDate(QDate.currentDate())

    date_input.setCalendarPopup(True)

    date_input.setDisplayFormat("yyyy-MM-dd")

    layout.addWidget(date_input, 3, 2, 1, 2)

    def confirm():

        pop_up.task = {
            "name": name_input.text(),
            "desc": description_input.toPlainText(),
            "due": date_input.date().toString("yyyy-MM-dd"),
            "id": str(uuid4()),
        }

        pop_up.accept()

    cancel_button = QPushButton("Cancel")

    cancel_button.clicked.connect(pop_up.reject)

    layout.addWidget(cancel_button, 4, 1)

    add_button = QPushButton("Add")

    add_button.clicked.connect(confirm)

    layout.addWidget(add_button, 4, 2)

    if pop_up.exec():
        return pop_up.task

    return None


