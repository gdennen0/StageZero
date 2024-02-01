"""
Module: AudioPlaybackCommandWidget

This module defines the AudioPlaybackCommandWidget class, a QWidget subclass that provides a user interface for controlling audio playback.
The widget includes a horizontal layout containing four elements: a "Play" button, a "Pause" button, a "Reset" button, and a label displaying the current frame.

Arguments:
    None

Returns:
    An instance of the AudioPlaybackCommandWidget class.

The AudioPlaybackCommandWidget class is initialized with no arguments. Upon initialization, it calls the initialize() method to set up the widget's layout and elements.
The initialize() method creates a QHBoxLayout, sets its margins, and creates the four elements (Play button, Pause button, Reset button, and time label). 
These elements are then added to the layout in the order they were created.
"""


from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QLabel,  # For displaying text or images
    QHBoxLayout,  # Box layout with a horizontal direction
    QPushButton,  # Command button
)
from ..UI_COLORS import UIColors


class AudioPlaybackCommandWidget(QWidget):  # Widget for controlling audio playback
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()  # Initialize the widget
        self.initialize_ui_colors()

    def initialize_ui_colors(self):
        # Define UI elements and their properties
        ui_elements = {
            self.play_button: {"button": True},
            self.pause_button: {"button": True},
            self.reset_button: {"button": True},
            self.time_label: {"text": True},
        }

        # Apply colors to all UI elements
        UIColors.initialize_ui_colors(ui_elements)

        style_sheet = (
            f"background-color: {UIColors.BACKGROUND_COLOR};"
            f"QLabel {{ color: {UIColors.TEXT_COLOR}; }}"
            f"QPushButton {{ "
            f"background-color: {UIColors.BUTTON_COLOR}; "
            f"color: {UIColors.BUTTON_TEXT_COLOR}; "  # Set the text color for buttons
            f"}}"
            f"QWidget {{ background-color: {UIColors.WIDGET_COLOR}; }}"
        )

        # Apply the concatenated style sheet
        self.setStyleSheet(style_sheet)

    def initialize(self):  # Initialize the widget
        self.layout = QHBoxLayout(self)  # Set the layout to horizontal box layout
        # self.layout.setContentsMargins(1, 1, 1, 1)  # Set half as much padding

        self.play_button = QPushButton("Play", self)  # Button for playing the audio
        self.pause_button = QPushButton("Pause", self)  # Button for pausing the audio
        self.reset_button = QPushButton("Reset", self)  # Button for resetting the audio
        self.time_label = QLabel(
            "Frame: ", self
        )  # Label for displaying the current frame

        self.layout.addWidget(self.time_label)  # Add the time label to the layout
        self.layout.addWidget(self.play_button)  # Add the play button to the layout
        self.layout.addWidget(self.pause_button)  # Add the pause button to the layout
        self.layout.addWidget(self.reset_button)  # Add the reset button to the layout
