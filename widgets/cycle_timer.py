from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtWidgets import (
    QDialog,
    QGridLayout,
    QLabel,
    QPushButton,
    QFrame,
    QHBoxLayout,
)

from .stopwatch import Stopwatch


def cycle_warn(
    parent,
    message: str,
    audio_file: str = "alarm.mp3"
):
    player = QMediaPlayer()
    audio_output = QAudioOutput()

    player.setAudioOutput(audio_output)

    player.setSource(
        QUrl.fromLocalFile(audio_file)
    )

    dialog = QDialog(parent)
    dialog.setWindowTitle("Cycle Completed")

    layout = QGridLayout()
    dialog.setLayout(layout)

    layout.addWidget(
        QLabel(message),
        0,
        0
    )

    ok_button = QPushButton("OK")
    ok_button.clicked.connect(dialog.accept)

    layout.addWidget(
        ok_button,
        1,
        0
    )

    dialog.exec()

    player.play()


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

        self.cycle_counter = QLabel(
            f"Cycle: {self.current_cycle}"
        )

        self.stopwatch = Stopwatch(
            self,
            cycle_time,
            cycle_enabled=cycle_alarm_enabled,
        )

        self.stopwatch.cycle_completed.connect(
            self.update_cycle_counter
        )

        layout = QHBoxLayout()

        layout.addWidget(
            self.cycle_counter
        )

        layout.addWidget(
            self.stopwatch
        )

        self.setLayout(layout)


    def start_timer(self):
        self.stopwatch.start_stop()


    def update_cycle_counter(self):

        self.current_cycle += 1

        self.cycle_counter.setText(
            f"Cycle: {self.current_cycle}"
        )

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