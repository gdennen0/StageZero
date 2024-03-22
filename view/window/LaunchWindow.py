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
from PyQt5.QtCore import QSize, Qt  # Import QSize for setting window size


class LaunchWindow(QWidget):  # Class for the launch window
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.setWindowTitle("StageZero Launch Window")  # Set the window title
        self.initialize()  # Initialize the launch window

    def initialize(self):  # Initialize the launch window
        self.layout = QVBoxLayout(self)  # Set the layout to vertical box layout
        self.layout.setAlignment(Qt.AlignCenter)  # Align the layout to center the buttons
        screen_size = QApplication.primaryScreen().size()  # Get the size of the screen
        button_size = QSize(screen_size.width() // 8, screen_size.height() // 48)  # Calculate the new button size
        # self.layout.addSpacing(screen_size.height() /64)

        self.new_project_button = QPushButton("New Project", self)  # Button for creating a new project
        self.new_project_button.setFixedSize(button_size)  # Set the fixed size for the new project button
        
        

        self.load_project_button = QPushButton("Load Project", self)  # Button for loading an existing project
        self.load_project_button.setFixedSize(button_size)  # Set the fixed size for the load project button

        self.layout.addWidget(self.new_project_button)  # Add the new project button to the layout

        self.layout.addSpacing(screen_size.height() // 128)  # Add some space between the buttons for better UI
        self.layout.addWidget(self.load_project_button)  # Add the load project button to the layout

    # Launch Window Structure
    def open(self):  # Open the launch window
        # calling the show method of the super class
        super().show()
        # Set the launch window size to 1/8 of the screen size
        screen_size = QApplication.primaryScreen().size()  # Get the size of the screen
        window_size = QSize(
            screen_size.width() // 5, screen_size.height() // 6
        )  # Calculate the new window size
        self.resize(window_size)  # Set the new window size

    def close(self):  # Close the launch window
        # calling the close method of the super class
        super().close()
