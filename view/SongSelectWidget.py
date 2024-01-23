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

from .UI_COLORS import UIColors


class SongSelectWidget(QWidget):  # Widget for song selection
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()  # Initialize the widget
        self.initialize_ui_colors()

    def initialize_ui_colors(self):
        # Define UI elements and their properties
        ui_elements = {
            self.layout: {'background': True},
            self.label: {'text': True},
            self.add_new_song: {'button': True},
            self.song_selector: {'dropdown': True},
        }

        # Apply colors to all UI elements
        UIColors.initialize_ui_colors(ui_elements)

        style_sheet = (
            f"background-color: {UIColors.BACKGROUND_COLOR};"
            f"QLabel {{ color: {UIColors.TEXT_COLOR}; }}"
            f"QPushButton {{ background-color: {UIColors.BUTTON_COLOR}; }}"
            f"QWidget {{ background-color: {UIColors.WIDGET_COLOR}; }}"
        )
        
        # Apply the concatenated style sheet
        self.setStyleSheet(style_sheet)
        
    def initialize(self):  # Initialize the widget
        self.layout = QHBoxLayout(self)  # Set the layout to horizontal box layout
        self.label = QLabel(f"Select Song")  # Label for song selection
        self.add_new_song = QPushButton("Add New Song", self)  # Button for adding a new song
        self.song_selector = QComboBox(self)  # Combo box for selecting a song

        # Place the child widgets within the SongSelectWidget layout
        self.layout.addWidget(self.label)  # Add the label to the layout
        self.layout.addWidget(self.song_selector)  # Add the song selector to the layout
        self.layout.addWidget(self.add_new_song)  # Add the add new song button to the layout

