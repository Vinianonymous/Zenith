from PyQt6.QtWidgets import (
    QDialog,
    QGridLayout,
    QDialogButtonBox,
    QGroupBox,
    QLineEdit,
    QLabel,
    QSpinBox,
    QRadioButton,
    QTextEdit,
)
from PyQt6.QtCore import QObject, QSettings
import sys
import os


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
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        # Restart warning
        restart_label = QLabel(
            "Warning: A Restart is required for changes to take effect."
        )
        self.layout.addWidget(restart_label, 0, 0, 1, 2)

        # Create the button box
        self.buttonBox = QDialogButtonBox(buttons)

        # Connect signals to slots
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Cycle alarm settings stuff
        self.cycle_group = QGroupBox("Cycle Alarm Settings")
        self.cycle_group_layout = QGridLayout()
        self.cycle_amount_label = QLabel("Time Per Cycle (minutes):")
        self.cycle_group_layout.addWidget(self.cycle_amount_label, 1, 1)

        self.cycle_amount_input = QSpinBox()
        self.cycle_amount_input.setValue(
            int(self.settings.value("CycleTime", defaultValue=30))
        )
        self.cycle_group_layout.addWidget(self.cycle_amount_input, 1, 2)

        self.cycle_toggle = QRadioButton("Activate Cycle Alarm")
        self.cycle_toggle.setChecked(
            bool(self.settings.value("CycleEnabled", defaultValue=True))
        )
        self.cycle_group_layout.addWidget(self.cycle_toggle, 1, 3)

        self.cycle_alarm_filepath_label = QLabel("Alarm Filepath: ")
        self.cycle_alarm_filepath = QLineEdit("Alarm Sound Filepath")
        self.cycle_alarm_filepath.setText(
            self.settings.value("AlarmFile", defaultValue="alarm.mp3")
        )
        self.cycle_group_layout.addWidget(self.cycle_alarm_filepath_label, 2, 1)
        self.cycle_group_layout.addWidget(self.cycle_alarm_filepath, 2, 2)

        self.cycle_amount_label = QLabel("Number of Cycles:")
        self.cycle_group_layout.addWidget(self.cycle_amount_label, 3, 1)

        self.cycle_amount_input = QSpinBox()
        self.cycle_amount_input.setValue(
            int(self.settings.value("CycleAmount", defaultValue=5))
        )
        self.cycle_group_layout.addWidget(self.cycle_amount_input, 3, 2)

        self.cycle_messages_label = QLabel("Messages: ")
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
        self.cycle_group_layout.addWidget(self.cycle_messages_label, 4, 1)
        self.cycle_group_layout.addWidget(self.cycle_messages, 4, 2)

        self.cycle_group.setLayout(self.cycle_group_layout)

        # Layout additions
        self.layout.addWidget(self.cycle_group)
        self.layout.addWidget(self.buttonBox)

    def accept(self):
        # Save the cycle amount
        cycle_time = self.cycle_amount_input.value()
        self.settings.setValue("CycleTime", cycle_time)
        self.settings.setValue("CycleEnabled", self.cycle_toggle.isChecked())
        self.settings.setValue("AlarmFile", self.cycle_alarm_filepath.text())
        self.settings.setValue("CycleAmount", self.cycle_amount_input.value())
        self.settings.setValue(
            "CycleMessages",
            [
                msg + "\n"
                for msg in self.cycle_messages.toPlainText().split("\n")
                if msg
            ]
        )
        self.settings.sync()
        super().accept()

        # Restarts the app for changes to take effect
        os.execl(sys.executable, sys.executable, *sys.argv)


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
        quit()
