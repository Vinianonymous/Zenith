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

class metrics(QObject):
    def __init__(self):
        super().__init__()
        self.handler = fileHandler()
        try:
            self.metricData = self.handler.read("metrics.json")
        except FileNotFoundError:
            self.metricData = {"total_time": {'hours':0, 'minutes':0, 'seconds':0}}
class metricsDialog(QDialog):
    def __init__(self, metricData: dict, parent=None):
        super().__init__(parent)

        layout = QGridLayout()
        self.setLayout(layout)

        time = metricData["total_time"]

        self.time_label = QLabel(
            f"Total Time: {time['hours']}h "
            f"{time['minutes']}m "
            f"{time['seconds']}s"
        )

        layout.addWidget(self.time_label)

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logic = Logic()
        self.settings = QSettings("For God Corp", "Zenith")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QGridLayout()
        central_widget.setLayout(self.layout)

        self._metrics = metrics()
        print(type(self._metrics.metricData))


 
        self.metrics_button = QPushButton("Metrics")
        self.layout.addWidget(self.metrics_button)
        self.metrics_button.clicked.connect(self.show_metrics)



        self.metrics_dialog = metricsDialog(self._metrics.metricData, self)
        
        self.show()


    def show_metrics(self):
        self.metrics_dialog.exec()
        


def main():
    app = QApplication([])
    main_window = mainWindow()
    app.exec()


if __name__ == "__main__":
    main()
