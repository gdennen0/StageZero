"""
Module: LaunchWindow
This module defines the LaunchWindow class which is a QWidget. The LaunchWindow is the initial window that is displayed when the application is launched.
It contains two buttons: "New Project" and "Load Project". The "New Project" button is for creating a new project and the "Load Project" button is for loading an existing project.

Arguments: None
This module does not take any arguments. It initializes the buttons and layout in the constructor and has methods to open and close the window.

Returns: None
This module does not return any values. It is used for its side effects of creating the launch window, opening it, and closing it.
"""

from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QVBoxLayout,  # Box layout with a vertical direction
    QPushButton,  # Command button
)
from PyQt5.QtWidgets import QApplication  # Import QApplication for screen size
from PyQt5.QtCore import QSize  # Import QSize for setting window size
from ..UI_COLORS import UIColors


class LaunchWindow(QWidget):  # Class for the launch window
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.setWindowTitle("StageZero Launch Window")  # Set the window title
        self.initialize()  # Initialize the launch window
        self.initialize_ui_colors()

    def initialize_ui_colors(self):
        # Define UI elements and their properties
        ui_elements = {
            # self.song_select_menu: {"dropdown": True},
            self.layout: {"widget": True},
            self.new_project_button: {"button": True},
            self.load_project_button: {"button": True},
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

    def initialize(self):  # Initialize the launch window
        self.layout = QVBoxLayout(self)  # Set the layout to vertical box layout

        self.new_project_button = QPushButton(
            "New Project", self
        )  # Button for creating a new project
        self.load_project_button = QPushButton(
            "Load Project", self
        )  # Button for loading an existing project

        self.layout.addWidget(
            self.new_project_button
        )  # Add the new project button to the layout
        self.layout.addWidget(
            self.load_project_button
        )  # Add the load project button to the layout

    # Launch Window Structure
    def open(self):  # Open the launch window
        # calling the show method of the super class
        super().show()
        # Set the launch window size to 1/8 of the screen size
        screen_size = QApplication.primaryScreen().size()  # Get the size of the screen
        window_size = QSize(
            screen_size.width() // 4, screen_size.height() // 8
        )  # Calculate the new window size
        self.resize(window_size)  # Set the new window size

    def close(self):  # Close the launch window
        # calling the close method of the super class
        super().close()
