from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QLabel,  # For displaying text or images
    QVBoxLayout,  # Box layout with a vertical direction
    QPushButton,  # Command button
)
from PyQt5.QtWidgets import QComboBox
from .OnsetFilterWidget import OnsetFilterWidget


class OnsetDetectionWidget(QWidget):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.onset_filter_widgets = {}
        self.initialize()

    def initialize(self):
        self.layout = QVBoxLayout(self)

        self.paint_to_song_overview_button = QPushButton(
            "Paint Onsets to SongOverview", self
        )
        self.remove_from_song_overview_button = QPushButton(
            "Remove Onsets from SongOverview", self
        )

        self.layout.addWidget(self.paint_to_song_overview_button)
        self.layout.addWidget(self.remove_from_song_overview_button)

        self.filter_type_dropdown = QComboBox(self)
        self.filter_type_dropdown.addItem("hi-pass")
        self.filter_type_dropdown.addItem("lo-pass")
        self.filter_type_dropdown.addItem("mid-pass")

        self.layout.addWidget(self.filter_type_dropdown)

    def add_filter(self, filter_type):
        # Create a new OnsetFilterWidget instance and add it to the dictionary
        self.onset_filter_widgets[filter_type] = OnsetFilterWidget(filter_type)

        # Add the new OnsetFilterWidget instance to the layout
        self.layout.addWidget(self.onset_filter_widgets[filter_type])
