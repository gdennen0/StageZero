from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QLabel,  # For displaying text or images
    QVBoxLayout,  # Box layout with a vertical direction
    QPushButton,  # Command button
)

class OnsetFilterWidget(QWidget):
    def __init__(self, filter_type):
        super().__init__()  # Call the constructor of the parent class
        self.filter_type = filter_type
        self.initialize()

    def initialize(self):
        self.layout = QVBoxLayout(self)    
        self.filter_type_label = QLabel(str(self.filter_type))
        self.paint_to_song_overview_button = QPushButton(f"Paint {self.filter_type} Onsets to SongOverview", self)
        self.remove_from_song_overview_button = QPushButton(f"Remove {self.filter_type} Onsets from SongOverview", self)
        self.layout.addWidget(self.filter_type_label)
        self.layout.addWidget(self.paint_to_song_overview_button)
        self.layout.addWidget(self.remove_from_song_overview_button)
