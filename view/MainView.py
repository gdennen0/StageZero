"""
Module: MainView

This module is responsible for managing the main view of the application. It imports and initializes all the necessary windows and widgets, 
including the LaunchWindow, MainWidget, ToolsWindow, GraphsWindow, and MainMenu. It also sets up the user interface and provides methods 
to open the main window and the launch window.

Arguments: None

Returns: None

The MainView class inherits from QMainWindow, which is the base class for all the main application windows. The class constructor initializes 
all the windows and widgets, and calls the init_ui method to set up the user interface. The init_ui method sets the application title and 
the custom menu bar. The open_main_window and open_launch_window methods are used to set the main window and the launch window as the central 
widget, respectively, and display them.
"""

from .LaunchWindow import LaunchWindow
from .MainWidget import MainWidget
from .ToolsWindow import ToolsWindow
from .GraphsWindow import GraphsWindow
from .MainMenu import MainMenu

from PyQt5.QtWidgets import QMainWindow


class MainView(QMainWindow):  # Main view class
    def __init__(self):
        super().__init__()
        self.launch_window = LaunchWindow()  # Initialize launch window
        self.main_window = MainWidget()  # Initialize main window
        self.tools_window = ToolsWindow()
        self.graphs_window = GraphsWindow()
        self.main_menu = MainMenu()
        self.init_ui()

    def init_ui(self):
        # Set the application title in the menu bar
        self.setWindowTitle('StageZeroDev')
        # Set the custom menu bar
        self.setMenuBar(self.main_menu)

    def open_main_window(self):
        # Set the main window as the central widget
        self.setCentralWidget(self.main_window)
        self.show()

    def open_launch_window(self):
        self.setCentralWidget(self.launch_window)
        self.show()

    # def refresh_layer_plot(self, layer_name):
    #     self.main_window.stack.layer_widget.