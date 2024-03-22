"""
Module: PlaybackModeWidget

This module defines a widget for selecting the playback mode in a PyQt5 application. 
The widget is a combination of a QLabel and a QComboBox. The QLabel serves as a 
label for the widget, and the QComboBox allows the user to select the playback mode.

Arguments: None

The PlaybackModeWidget class does not take any arguments. It initializes itself 
with a QHBoxLayout, a QLabel, and a QComboBox. The QHBoxLayout is used to arrange 
the QLabel and the QComboBox horizontally. The QLabel is set with the text 
"Playback Mode", and the QComboBox is populated with the options "Play", "Edit", 
and "Record".

Returns: None

The PlaybackModeWidget class does not return any values. It is a QWidget, and its 
main function is to be displayed in a PyQt5 application and allow the user to 
select a playback mode.
"""

from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QLabel,  # For displaying text or images
    QHBoxLayout,  # Box layout with a horizontal direction
    QComboBox,  # Drop down selection box
)
from PyQt5.QtWidgets import QSizePolicy


class PlaybackModeWidget(QWidget):  # Widget for selecting the playback mode
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()  # Initialize the widget

    def initialize(self):  # Initialize the widget
        self.layout = QHBoxLayout(self)  # Set the layout to horizontal box layout
        self.label = QLabel("Playback Mode", self)  # Label for the playback mode
        self.playback_mode_selector = QComboBox(self)  # Combo box for selecting the playback mode
        self.playback_mode_selector.addItems(["Play", "Edit", "Record"])  # Add the playback modes to the combo box
        self.layout.addWidget(self.label)  # Add the label to the layout
        self.layout.addWidget(self.playback_mode_selector)  # Add the playback mode selector to the layout
        self.layout.addStretch(1)
