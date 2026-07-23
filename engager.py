import sys
import os
from pathlib import Path
from uuid import uuid4

from PyQt6.QtCore import QObject, QSettings, pyqtSignal, QUrl, QTimer, QDate
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from PyQt6.QtWidgets import (
    QDialogButtonBox,
    QGroupBox,
    QLineEdit,
    QSpinBox,
    QRadioButton,
    QTextEdit,
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QDialog,
    QLabel,
    QApplication,
    QGridLayout,
    QMainWindow,
    QPushButton,
    QWidget,
    QDateEdit,
)

from logic import Logic


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


class CycleTimer(QFrame):
    def __init__(
        self,
        cycle_time: int,
        cycle_alarm_enabled: bool,
        messages: list,
        cycle_amount: int,
        alarm_file: str,
    ):
        super().__init__()

        self.current_cycle = 1
        self.alarm_path = alarm_file
        self.messages = messages
        self.cycle_amount = cycle_amount

        self.cycle_counter = QLabel(f"Cycle: {self.current_cycle}")

        self.stopwatch = Stopwatch(
            self,
            cycle_time,
            cycle_enabled=cycle_alarm_enabled,
        )

        self.stopwatch.cycle_completed.connect(self.update_cycle_counter)

        layout = QHBoxLayout()
        layout.addWidget(self.cycle_counter)
        layout.addWidget(self.stopwatch)

        self.setLayout(layout)

    def start_timer(self):
        self.stopwatch.start_stop()

    def update_cycle_counter(self):
        self.current_cycle += 1

        self.cycle_counter.setText(f"Cycle: {self.current_cycle}")

        cycle_warn(
            self,
            (
                f"Cycle {self.current_cycle} completed! "
                f"{self.messages[self.current_cycle - 1]}"
            ),
            self.alarm_path,
        )

        if self.current_cycle == self.cycle_amount:
            cycle_warn(
                self,
                "All cycles completed! Good Job, take a rest.",
                self.alarm_path,
            )

            self.current_cycle = 1


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


class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        """
        Shows general settings about the app.
        """

        super().__init__(parent)

        self.settings = settings

        self.setWindowTitle("Settings")

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        buttons = (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        restart_label = QLabel(
            "Warning: A Restart is required for changes to take effect."
        )

        self.layout.addWidget(
            restart_label,
            0,
            0,
            1,
            2,
        )

        self.button_box = QDialogButtonBox(buttons)

        self.button_box.accepted.connect(self.accept)

        self.button_box.rejected.connect(self.reject)

        # Cycle settings

        self.cycle_group = QGroupBox("Cycle Alarm Settings")

        self.cycle_group_layout = QGridLayout()

        self.cycle_time_label = QLabel("Time Per Cycle (minutes):")

        self.cycle_group_layout.addWidget(
            self.cycle_time_label,
            1,
            1,
        )

        self.cycle_time_input = QSpinBox()

        self.cycle_time_input.setValue(
            int(self.settings.value("CycleTime", defaultValue=30))
        )

        self.cycle_group_layout.addWidget(
            self.cycle_time_input,
            1,
            2,
        )

        self.cycle_toggle = QRadioButton("Activate Cycle Alarm")

        self.cycle_toggle.setChecked(
            bool(self.settings.value("CycleEnabled", defaultValue=True))
        )

        self.cycle_group_layout.addWidget(
            self.cycle_toggle,
            1,
            3,
        )

        self.cycle_alarm_file_label = QLabel("Alarm Filepath:")

        self.cycle_alarm_file_input = QLineEdit()

        self.cycle_alarm_file_input.setText(
            self.settings.value("AlarmFile", defaultValue="alarm.mp3")
        )

        self.cycle_group_layout.addWidget(
            self.cycle_alarm_file_label,
            2,
            1,
        )

        self.cycle_group_layout.addWidget(
            self.cycle_alarm_file_input,
            2,
            2,
        )

        self.cycle_amount_label = QLabel("Number of Cycles:")

        self.cycle_amount_input = QSpinBox()

        self.cycle_amount_input.setValue(
            int(self.settings.value("CycleAmount", defaultValue=5))
        )

        self.cycle_group_layout.addWidget(
            self.cycle_amount_label,
            3,
            1,
        )

        self.cycle_group_layout.addWidget(
            self.cycle_amount_input,
            3,
            2,
        )

        self.cycle_messages_label = QLabel("Messages:")

        self.cycle_messages = QTextEdit()

        self.cycle_messages.setPlainText(
            "".join(
                self.settings.value(
                    "CycleMessages",
                    defaultValue=[
                        "Pray\n",
                        "Stretch, Hydrate and Look away from screens\n",
                        "Work in Hobbie\n",
                    ],
                )
            )
        )

        self.cycle_group_layout.addWidget(
            self.cycle_messages_label,
            4,
            1,
        )

        self.cycle_group_layout.addWidget(
            self.cycle_messages,
            4,
            2,
        )

        self.cycle_group.setLayout(self.cycle_group_layout)

        self.layout.addWidget(self.cycle_group)

        self.layout.addWidget(self.button_box)

    def accept(self):

        cycle_time = self.cycle_time_input.value()

        self.settings.setValue("CycleTime", cycle_time)

        self.settings.setValue("CycleEnabled", self.cycle_toggle.isChecked())

        self.settings.setValue("AlarmFile", self.cycle_alarm_file_input.text())

        self.settings.setValue("CycleAmount", self.cycle_amount_input.value())

        self.settings.setValue(
            "CycleMessages",
            [
                message + "\n"
                for message in self.cycle_messages.toPlainText().split("\n")
                if message
            ],
        )

        self.settings.sync()

        super().accept()

        # Restart application
        os.execl(sys.executable, sys.executable, *sys.argv)


class SettingsManager(QObject):
    def __init__(self, parent):

        super().__init__(parent)

        self.settings = QSettings("For God Corp", "Zenith")

        self.settings_dialog = SettingsDialog(self.settings, parent)

    def show(self):

        self.settings_dialog.exec()

        self.settings.sync()

        quit()


def cycle_warn(parent, message: str, audio_file: str = "alarm.mp3"):

    player = QMediaPlayer()
    audio_output = QAudioOutput()

    player.setAudioOutput(audio_output)

    player.setSource(QUrl.fromLocalFile(audio_file))

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

        self.time_spent = Stopwatch(self, 0, cycle_enabled=False)

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


class MainWindow(QMainWindow):
    def __init__(self):

        super().__init__()

        self.logic = Logic()

        self.settings_manager = SettingsManager(self)

        central_widget = QWidget()

        self.setCentralWidget(central_widget)

        layout = QGridLayout()

        central_widget.setLayout(layout)

        self.cycle_timer = CycleTimer(
            int(self.settings_manager.settings.value("CycleTime", defaultValue=30)),
            bool(
                self.settings_manager.settings.value("CycleEnabled", defaultValue=True)
            ),
            list(
                self.settings_manager.settings.value(
                    "CycleMessages",
                    defaultValue=[
                        "Pray\n",
                        "Stretch, Hydrate and Look away from screens\n",
                        "Work in Hobbie\n",
                    ],
                )
            ),
            int(self.settings_manager.settings.value("CycleAmount", defaultValue=5)),
            self.settings_manager.settings.value("AlarmFile", defaultValue="alarm.mp3"),
        )

        self.task_frame = TaskFrame(self.logic)

        self.task_frame.refresh(self.logic.tasks)

        self.add_button = QPushButton("Add Task")

        self.add_button.clicked.connect(self.prompt_add_task)

        self.config_button = QPushButton("Configure")

        self.config_button.clicked.connect(self.settings_manager.show)

        layout.addWidget(self.cycle_timer, 0, 0, 1, 2)

        layout.addWidget(self.task_frame, 1, 0, 1, 2)

        layout.addWidget(self.add_button, 2, 1)

        layout.addWidget(self.config_button, 2, 2)

        self.execution_popup = ExecutionPopup(self)

        self.cycle_timer.start_timer()

        self.show()

    def prompt_add_task(self):

        task = new_task_dialog(self)

        if task:
            self.logic.add_task(task)


def main():

    style = Path(__file__).parent / "styles.qss"

    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    app.setStyleSheet(style.read_text(encoding="utf-8"))

    window = MainWindow()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
