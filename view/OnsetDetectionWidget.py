from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QLabel,  # For displaying text or images
    QVBoxLayout,  # Box layout with a vertical direction
    QPushButton,  # Command button
)

class OnsetDetectionWidget(QWidget):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()

    def initialize(self):
        self.layout = QVBoxLayout(self)    

        self.paint_to_song_overview_button = QPushButton("Paint Onsets to SongOverview", self)
        self.remove_from_song_overview_button = QPushButton("Remove Onsets from SongOverview", self)

        self.layout.addWidget(self.paint_to_song_overview_button)
        self.layout.addWidget(self.remove_from_song_overview_button)
