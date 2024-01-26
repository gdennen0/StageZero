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

from .window.LaunchWindow import LaunchWindow
from .window.MainWindow import MainWindow
from .window.ToolsWindow import ToolsWindow
from .window.GraphsWindow import GraphsWindow
from .menu.MainMenu import MainMenu
from .window.SongDataPreviewWindow import SongDataPreviewWindow
from .menu.MainMenu import MainMenu

from PyQt5.QtWidgets import QMainWindow, QApplication


class MainView(QMainWindow):  # Main view class
    def __init__(self):
        super().__init__()
        self.launch_window = LaunchWindow()  # Initialize launch window
        self.main_window = MainWindow()  # Initialize main window
        self.tools_window = ToolsWindow()
        self.graphs_window = GraphsWindow()
        self.main_menu = MainMenu()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("StageZeroDev")  # Set the application title in the menu bar
        self.setMenuBar(self.main_menu)  # Set the custom menu bar

    def open_main_window(self):
        # Set the main window as the central widget
        self.main_window.open()
        screen_resolution = QApplication.desktop().screenGeometry()
        self.main_window.resize(
            screen_resolution.width() / 1.5, screen_resolution.height() / 2
        )  # Set the window to half of the screen size
        self.main_window.move(
            (screen_resolution.width() - self.main_window.width()) / 2,
            (screen_resolution.height() - self.main_window.height()) / 2,
        )  # Center the window

    def open_launch_window(self):
        self.launch_window.open()

    def close_launch_window(self):
        self.launch_window.close()
