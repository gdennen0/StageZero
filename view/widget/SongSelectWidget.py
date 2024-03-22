"""
Module: SongSelectWidget

This module defines a widget for song selection in a PyQt5 application. It is a subclass of QWidget, the base class for all user interface objects in PyQt5.

The SongSelectWidget consists of a horizontal layout (QHBoxLayout) containing three child widgets:
    - A QLabel for displaying the text "Select Song"
    - A QPushButton for adding a new song
    - A QComboBox for selecting a song from a dropdown list

Arguments: None

Returns: An instance of SongSelectWidget, ready to be added to a PyQt5 application.

The SongSelectWidget is initialized by calling its initialize() method, which sets up the layout and child widgets. The child widgets are then added to the layout in the order they should appear from left to right.
"""

from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QLabel,  # For displaying text or images
    QHBoxLayout,  # Box layout with a horizontal direction
    QPushButton,  # Command button
    QComboBox,  # Drop down selection box
)


class SongSelectWidget(QWidget):  # Widget for song selection
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()  # Initialize the widget

    def initialize(self):  # Initialize the widget
        self.layout = QHBoxLayout(self)  # Set the layout to horizontal box layout
        self.label = QLabel(f"Select Song")  # Label for song selection
        self.add_new_song = QPushButton("Add New Song", self)  # Button for adding a new song
        self.song_selector = QComboBox(self)  # Combo box for selecting a song
        self.layout.addWidget(self.label)  # Add the label to the layout
        self.layout.addWidget(self.song_selector)  # Add the song selector to the layout
        self.layout.addWidget(self.add_new_song)  # Add the add new song button to the layout
