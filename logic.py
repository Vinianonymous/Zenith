from PyQt6.QtCore import QObject, pyqtSignal
from file_handler import save_tasks, load_tasks

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
        self.tasks = load_tasks()

    def add_task(self, task: dict):
        """
        Adds the task dictionary to the list and emits an signal with said list for the UI to update.
        Writes the new tasklist to the file for storage

        """
        # Adds the tasks and emits signal with the TL
        self.tasks.append(task)
        self.save()

    def delete_task(self, task: dict):
        """
        Removes the element with the values specified per the dict and emits a signal for the GUI
        Writes new list to the file for storage
        """
        self.tasks.remove(task)
        self.tasks_changed.emit(list(self.tasks))
        self.save()

    def begin_exec(self, task: dict):
        self.start_doing.emit(task)

    def save(self):
        save_tasks(self.tasks)
        self.tasks_changed.emit(list(self.tasks))
