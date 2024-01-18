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
class LaunchWindow(QWidget):  # Class for the launch window
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()  # Initialize the launch window

    def initialize(self):  # Initialize the launch window
        self.layout = QVBoxLayout(self)  # Set the layout to vertical box layout

        self.new_project_button = QPushButton("New Project", self)  # Button for creating a new project
        self.load_project_button = QPushButton("Load Project", self)  # Button for loading an existing project

        self.layout.addWidget(self.new_project_button)  # Add the new project button to the layout
        self.layout.addWidget(self.load_project_button)  # Add the load project button to the layout

    # Launch Window Structure
    def open(self):  # Open the launch window
        # calling the show method of the super class
        super().show()

    def close(self):  # Close the launch window
        # calling the close method of the super class
        super().close()
