"""
Module: MainWidget

This module defines the MainWidget class, which is a QWidget. The MainWidget is the main window of the application, 
containing several other widgets for different functionalities such as song selection, song overview, audio playback 
control, layer control, stack display, and playback mode selection.

Arguments: None

Returns: None

The MainWidget class inherits from the QWidget base class. It initializes the main window and sets up the layout and 
widgets. The layout is a QVBoxLayout, which arranges the widgets vertically. Each widget is added to the layout in 
the initialize() method. The size policy for the song_select_menu and song_overview widgets is set to Preferred and 
Fixed respectively, meaning they will resize in a way that takes up as much space as they can without squishing other 
widgets, but their size will not change when the window is resized.

The open() method sets the window title and shows the window, while the close() method closes the window.
"""
from PyQt5.QtCore import Qt  # Add this line to import Qt
from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QVBoxLayout,  # Box layout with a vertical direction
    QHBoxLayout,
    QSizePolicy,  # Layout attribute describing horizontal and vertical resizing policy
    QMainWindow,
)

from ..widget.StageWidget import StageWidget
from ..UI_COLORS import UIColors
 
class MainWindow(QMainWindow):  # Class for the main window
    def __init__(self, main_menu):
        super().__init__()  # Call the constructor of the parent class
        self.setMenuBar(main_menu)  # Set the custom menu bar
        self.initialize()  # Initialize the main window
        self.initialize_ui_colors()

    def initialize_ui_colors(self):
        # Define UI elements and their properties
        ui_elements = {
            # self.song_select_menu: {"dropdown": True},
            self.main_widget: {"widget": True},
            self.menuBar(): {"main-menu": True},
        }

        # Apply colors to all UI elements
        UIColors.initialize_ui_colors(ui_elements)

    def open(self):  # Open the main window with a given title
        self.setWindowTitle("StageZero Dev")  # Set the window title
        self.show()  # Show the window

    def close(self):  # Close the main window
        self.close()  # Close the window

    def initialize(self):  # Initialize the main window

        self.main_widget = QWidget()  # Create a central widget
        self.main_layout = QHBoxLayout()  # Set the layout to vertical box layout
        self.main_widget.setLayout(self.main_layout)  # Set the main_layout as the layout for the central widget
        self.setCentralWidget(self.main_widget)  # Set the central widget for the QMainWindow
        self.main_layout.setSpacing(0)  # Set the spacing between widgets to 0

        self.stage_widget= StageWidget()
        self.main_layout.addWidget(self.stage_widget)  # add to the main_layout

        # self.setLayout(
        #     self.main_layout
        # )  # Set the main_layout as the layout for the widget
