
"""
Module: BPMToolWidget

This module defines the BPMToolWidget class, which is a QWidget subclass. It serves as a widget for handling 
BPM (Beats Per Minute) related operations in the application. The widget includes buttons for counting BPM, 
painting BPM to the SongOverview, and removing BPM from the SongOverview. It also includes a label to display 
the BPM value.

Arguments:
    None

Returns:
    An instance of the BPMToolWidget class.

"""



from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QLabel,  # For displaying text or images
    QVBoxLayout,  # Box layout with a vertical direction
    QPushButton,  # Command button
)

class BpmToolWidget(QWidget):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()

    def initialize(self):
        self.layout = QVBoxLayout(self)    

        self.count_button = QPushButton("Count", self)
        self.paint_to_song_overview_button = QPushButton("Paint to SongOverview", self)
        self.remove_from_song_overview_button = QPushButton("Remove BPM from SongOverview", self)
        self.bpm_label = QLabel("BPM", self)

        self.layout.addWidget(self.count_button)
        self.layout.addWidget(self.paint_to_song_overview_button)
        self.layout.addWidget(self.remove_from_song_overview_button)
        self.layout.addWidget(self.bpm_label)
