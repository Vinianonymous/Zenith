import sys
from pathlib import Path

from PyQt6.QtWidgets import (

    QApplication,
    QGridLayout,
    QMainWindow,
    QPushButton,
    QWidget,
)

from logic import Logic
from widgets import (
    CycleTimer,
    TaskFrame
)
from dialogs import ExecutionPopup, new_task_dialog
from settings import SettingsManager

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
