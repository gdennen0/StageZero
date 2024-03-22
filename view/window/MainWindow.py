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
    QMainWindow,
)

from ..widget.StageWidget import StageWidget
from ..widget.EventPropertiesWidget import EventPropertiesWidget
from ..widget.EventActionWidget import EventActionWidget
from ..widget.EventToolsWidget import EventToolsWidget


class MainWindow(QMainWindow):  # Class for the main window
    def __init__(self, main_menu):
        super().__init__()  # Call the constructor of the parent class
        self.setMenuBar(main_menu)  # Set the custom menu bar
        self.initialize()  # Initialize the main window

    def open(self):  # Open the main window with a given title
        self.setWindowTitle("StageZero Dev")  # Set the window title
        self.show()  # Show the window

    def close(self):  # Close the main window
        self.close()  # Close the window

    def initialize(self):  # Initialize the main window
        # Initialize and set the StageWidget as the central widget
        self.stage_widget = StageWidget(self)  # Pass self to set MainWindow as the parent of StageWidget
        self.setCentralWidget(self.stage_widget)

        # Initialize and dock the SidebarWidget
        self.event_properties_widget = EventPropertiesWidget("Event Properties", self)
        # self.event_tools_widget = EventToolsWidget("EventTools", self)
        self.event_action_widget = EventActionWidget("Event Actions", self)

        
        self.addDockWidget(Qt.RightDockWidgetArea, self.event_properties_widget)  # Dock the SidebarWidget to the right side
        self.addDockWidget(Qt.RightDockWidgetArea, self.event_action_widget)
        # self.addDockWidget(Qt.RightDockWidgetArea, self.event_tools_widget)  # Dock the SidebarWidget to the right side
