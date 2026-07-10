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
    QDialogButtonBox,
    QGroupBox,
    QRadioButton,
    QSpinBox
)
from PyQt6.QtCore import QObject, pyqtSignal, QDate, QTimer, QUrl, QSettings
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from uuid import uuid4
from filehandler import fileHandler


class Logic(QObject):
    # Class in which all of the backend is rendered.

    # Signal of alteration in the List so GUI can listen to it
    tasks_changed = pyqtSignal(list)  # emitted after every add / delete

    # Signal of task execution for the UI to pop up
    start_doing = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        """
        Initializes the task variable with either an empty list or the tasks in engager.json
        """

        self.tasks = []
        self.file_handler = fileHandler()
        self.tasks = self.file_handler.read("engager.json")

    def addTask(self, task: dict):
        """
        Adds the task dictionary to the list and emits an signal with said list for the UI to update.
        Writes the new tasklist to the file for storage

        """

        # Adds the tasks and emits signal with the TL
        self.tasks.append(task)
        self.tasks_changed.emit(list(self.tasks))

        self.file_handler.write("engager.json", self.tasks)

    def deleteTask(self, task: dict):
        """
        Removes the element with the values specified per the dict and emits a signal for the GUI
        Writes new list to the file for storage
        """
        self.tasks.remove(task)
        self.tasks_changed.emit(list(self.tasks))
        self.file_handler.write("engager.json", self.tasks)

    def beginExec(self, task: dict):
        self.start_doing.emit(task)

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

class stopwatch(QWidget):
    def __init__(self, parent, cycleTime, cycleEnabled=True):
        super().__init__()
        self.layout = QHBoxLayout()
        self.cycle_time = cycleTime
        self.cycle_enabled = cycleEnabled

        self.timeLabel = QLabel("00:00:00")
        self.layout.addWidget(self.timeLabel)
        self.setLayout(self.layout)
        self.timePassed = {"hours": 0, "minutes": 0, "seconds": 57}
        self.running = False
        self.timer = QTimer()

        self.timer.timeout.connect(self.updateTime)

        self.audio = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio)
        self.player.setSource(QUrl.fromLocalFile("alarm.mp3"))

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
        if self.timePassed["minutes"] > 59:
            self.timePassed["hours"] += 1
            self.timePassed["minutes"] = 0

        self.updateLabel()

        if self.cycle_enabled and self.timePassed["minutes"] % self.cycle_time == 0 and self.timePassed["seconds"] == 0:
            self.player.play()

    def updateLabel(self):
        hours = self.timePassed["hours"]
        minutes = self.timePassed["minutes"]
        seconds = self.timePassed["seconds"]
        self.timeLabel.setText(f"{hours:02}:{minutes:02d}:{seconds:02d}")


# -- Execution Popup -------------------------------------------------connect
class executionPopup:
    def __init__(self, mw, cycle_time: int, cycle_enabled: bool = True) -> None:
        self.mw = mw
        self.cycle_time = cycle_time
        self.cycle_enabled = cycle_enabled
        self.mw.logic.start_doing.connect(self.start)

    def start(self, task: dict):
        def finish(task):
            self.mw.logic.deleteTask(task)
            dialog.deleteLater()

        dialog = QDialog(self.mw)
        layout = QGridLayout()
        dialog.setLayout(layout)

        self.timeSpent = stopwatch(self, self.cycle_time, self.cycle_enabled)
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

# the ui for settings manager
class settingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        """
        Shows general settings about the app.
        """

        # Some UI boiler plate
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle("Settings")
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Define buttons using standard flags
        buttons = (
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        
        # Create the button box
        self.buttonBox = QDialogButtonBox(buttons)
        
        # Connect signals to slots
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        # Cycle alarm settings stuff
        self.cycle_group = QGroupBox("Cycle Alarm Settings")
        self.cycle_group_layout = QHBoxLayout()
        self.cycle_amount_label = QLabel("Time Per Cycle (minutes):")
        self.cycle_group_layout.addWidget(self.cycle_amount_label)

        self.cycle_amount_input = QSpinBox()
        self.cycle_amount_input.setValue(int(self.settings.value("CycleTime", defaultValue=30)))
        self.cycle_group_layout.addWidget(self.cycle_amount_input)

        self.cycle_toggle = QRadioButton("Activate Cycle Alarm")
        self.cycle_toggle.setChecked(bool(self.settings.value("CycleEnable", defaultValue=True)))
        self.cycle_group_layout.addWidget(self.cycle_toggle)
# 
        self.cycle_group.setLayout(self.cycle_group_layout)

        # Layout additions
        self.layout.addWidget(self.cycle_group)
        self.layout.addWidget(self.buttonBox)
    def accept(self):
        # Save the cycle amount
        cycle_time = self.cycle_amount_input.value()
        self.settings.setValue("CycleTime", cycle_time)
        self.settings.setValue("CycleEnable", self.cycle_toggle.isChecked())
        super().accept()


# Pretty damn good name, dare i say.
class settingsManager(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.settings = QSettings("For God Corp", "Zenith")
        self.settings_dialog = settingsDialog(self.settings, parent)
    def show(self):
        """
        Show the settings dialog.
        """
        self.settings_dialog.exec()
        self.settings.sync()
        

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

        layout.addWidget(self.task_frame, 1, 1)
        layout.addWidget(self.add_button, 2, 1)
        layout.addWidget(self.config_button, 2, 2)

        self.execution_popup = executionPopup(
            self,
            int(self.settings_manager.settings.value("CycleTime", defaultValue=30))
        )
        self.show()

    def promptAddTask(self):
        task = newTaskDialog(self)
        if task:
            self.logic.addTask(task)


def main():
    app = QApplication([])
    mainWindow()
    app.exec()


if __name__ == "__main__":
    main()
