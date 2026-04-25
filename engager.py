from PyQt6.QtWidgets import QMainWindow, QDialog,QGridLayout, QApplication, QPushButton, QWidget, QMessageBox, QTextEdit, QDateEdit, QLabel, QLineEdit, QFrame, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import QDateTime,QDate
from uuid import uuid4 

class manageFrame(QWidget):
    def __init__(self, logicObject): #This is called composition. I am inheriting indirectly only what I need from mainwindow
        super().__init__()
        self.logic_object = logicObject
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.addButton = QPushButton("Add Task")
        self.addButton.clicked.connect(self.add)
        self.layout.addWidget(self.addButton, 1, 1, 1, 1)

    def add(self):
        self.logic_object.addTask()



class IHandler():
    def __init__(self, mw):
        self.mw = mw

    @classmethod
    def newTask(self, window) -> dict:
        """
        Takes the main window as arguement. Returns the task dictionary. 

        """
        #Boiler plate to set up geometry and layout
        pop_up = QDialog(window)
        pop_up.setGeometry(0, 0, 500, 400)
        layout = QGridLayout()
        pop_up.setLayout(layout) 

        #Input section
        n_label = QLabel("Task Name")
        layout.addWidget(n_label, 1, 1, 1, 1)
        name = QLineEdit()
        layout.addWidget(name, 1, 2, 1, 2)
        
        desc_label = QLabel("Task description: ")
        layout.addWidget(desc_label, 2, 1, 1, 1)
        desc = QTextEdit()
        layout.addWidget(desc, 2, 2, 1, 2)

        
        date_label = QLabel("Due date: ")
        layout.addWidget(date_label, 3, 1, 1, 1)
        date = QDateEdit()
        date.setCalendarPopup(True)
        date.setDisplayFormat("yyyy-MM-dd")
        layout.addWidget(date, 3, 2, 1, 2)

        def addTask():
            #Gets the input in the text boxes
            taskName = name.text()
            taskDesc = desc.toPlainText()
            taskDue = date.date()
            
            #Generates the task dictionary
            pop_up.task = {
                "name": taskName,
                "desc": taskDesc,
                "due": taskDue,
                "id": f"{uuid4()}"
            }
            pop_up.accept()


        #Action section
        cancel = QPushButton("cancel")
        layout.addWidget(cancel, 4, 1, 1, 1)
        cancel.clicked.connect(pop_up.reject)#If the button is clicked, a signal is sent to end the whole pop up

        add = QPushButton("Add")
        layout.addWidget(add, 4, 2, 1, 1)
        add.clicked.connect(addTask) 

        #If the pop up has been properly executed. The main thread is blocked until popup.accept or reject are given. 
        if pop_up.exec():
            #Return the task
            return pop_up.task
        #Else return nothing
        return None
        
    def update(self):
        """
        Updates the task Frame display.
        """

        #Clearing section: We first remove all the elements to avoid doubling
        for i in reversed(range(self.mw.task_frame.layout.count())): #For I in the reversed count of each widget in it the TF
            widget = self.mw.task_frame.layout.itemAt(i).widget() #Gets the widget
            if widget: #If it is not none, then the widget gets deleted
                widget.deleteLater()
        
        #Adding sectionHandler.showInfo(self.task)
        #For each task in the task List, create a widget and append it to the task frame layout
        for task in self.mw.logic.tasks:
            task_widget = taskWidget(task)
            self.mw.task_frame.layout.addWidget(task_widget)
    def showInfo(self, task):
        pop_up = QDialog(self.mw)


class taskWidget(QWidget):
    def __init__(self, task):
        #Boiler plate
        super().__init__()
        self.task = task
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        #Task name
        self.name = QLabel(task["name"])
        self.layout.addWidget(self.name)

        #Show the information: Description, Due date and UUID
        self.info_button = QPushButton("Info")
        self.layout.addWidget(self.info_button)
        self.info_button.clicked.connect(self.showInformation)
    
    def showInformation(self):
        IHandler.showInfo(self.task)
        


class Logic():
    def __init__(self, main):
        self.mw = main
        self.tasks = []

    def addTask(self):
        """
        Prompts the Ihandler for a popup, appends it to list, updates the display.
        """
        task = self.mw.i_handler.newTask(self.mw)
        if task:
            self.tasks.append(task)
            self.mw.i_handler.update()
            print(task)

    
class taskFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Apparently I have to set a central widget and give layout to that instead of the mainwindow
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QGridLayout()
        central_widget.setLayout(self.layout)

        self.logic = Logic(self)
        self.i_handler = IHandler(self)

        self.task_frame = taskFrame()
        self.layout.addWidget(self.task_frame, 1, 1, 2, 2)

        self.manage_frame = manageFrame(self.logic)
        self.layout.addWidget(self.manage_frame, 2, 1, 1, 1)


        self.show()

def main():
    app = QApplication([])
    main_window = mainWindow()
    app.exec()

if __name__ == "__main__":
    main()