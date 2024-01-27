from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QLabel,  # For displaying text or images
    QVBoxLayout,  # Box layout with a vertical direction
    QPushButton,  # Command button
)


class LocalWindow(QWidget):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.setWindowTitle("Graphs")
        self.initialize()

    def initialize(self):
        self.layout = QVBoxLayout(self)

        self.count_button = QPushButton("Count", self)
        self.paint_to_song_overview_button = QPushButton("Paint to SongOverview", self)
        self.remove_from_song_overview_button = QPushButton(
            "Remove BPM from SongOverview", self
        )
        self.bpm_label = QLabel("BPM", self)

        self.layout.addWidget(self.count_button)
        self.layout.addWidget(self.paint_to_song_overview_button)
        self.layout.addWidget(self.remove_from_song_overview_button)
        self.layout.addWidget(self.bpm_label)

    def open(self):
        self.show()
