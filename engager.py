import sys
from PyQt6.QtWidgets import QApplication, QGridLayout, QMainWindow, QPushButton, QWidget
from dialog import newTaskDialog, executionPopup
from logic_class import Logic
from settings import settingsManager
from widgets import taskFrame
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
        self.task_frame = taskFrame(self.logic)
        self.task_frame.refresh(self.logic.tasks)
        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.promptAddTask)

        self.config_button = QPushButton("Configure")
        self.config_button.clicked.connect(self.settings_manager.show)

        layout.addWidget(self.task_frame, 1, 1, 1, 2)
        layout.addWidget(self.add_button, 2, 1)
        layout.addWidget(self.config_button, 2, 2)

        self.execution_popup = executionPopup(
            self,
            int(self.settings_manager.settings.value("CycleTime", defaultValue=30)),
        )

        self.show()

    def promptAddTask(self):
        task = newTaskDialog(self)
        if task:
            self.logic.addTask(task)


def main():
    style = Path(__file__).parent / "styles.qss"
    # Added sys.argv for robust QApplication initialization
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(style.read_text(encoding="utf-8"))
    window = mainWindow()  # Kept a reference to prevent garbage collection
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
