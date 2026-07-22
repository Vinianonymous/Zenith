import sys
from PyQt6.QtWidgets import QApplication, QGridLayout, QMainWindow, QPushButton, QWidget
from dialog import newTaskDialog, executionPopup
from logic_class import Logic
from settings import settingsManager
from widgets import taskFrame, cycleTimer
from pathlib import Path


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logic = Logic()
        self.settings_manager = settingsManager(self)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout()
        central_widget.setLayout(layout)
        self.cycle_timer = cycleTimer(
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
            self.settings_manager.settings.value("AlarmFile", defaultValue="alarm.mp3")
        )
        self.task_frame = taskFrame(self.logic)
        self.task_frame.refresh(self.logic.tasks)
        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.promptAddTask)

        self.config_button = QPushButton("Configure")
        self.config_button.clicked.connect(self.settings_manager.show)

        layout.addWidget(self.cycle_timer, 0, 0, 1, 2)
        layout.addWidget(self.task_frame, 1, 0, 1, 2)
        layout.addWidget(self.add_button, 2, 1)
        layout.addWidget(self.config_button, 2, 2)

        self.execution_popup = executionPopup(self)

        self.cycle_timer.start_timer()
        self.show()

    def promptAddTask(self):
        task = newTaskDialog(self)
        if task:
            self.logic.addTask(task)


def main():
    # This comment was added from the TTY interface lmao, hello future me,

    style = Path(__file__).parent / "styles.qss"
    # Added sys.argv for robust QApplication initialization
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(style.read_text(encoding="utf-8"))
    window = mainWindow()  # Kept a reference to prevent garbage collection
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
