"""
Module: MainMenuController

This module defines the MainMenuController class, which is responsible for controlling the main menu of the application. 
It initializes the connections for the main menu and defines the actions to be performed when the tools and graphs options are selected from the menu.

Arguments:
main_controller (object): An instance of the main controller. It is used to access the view and initialize the connections for the main menu.

Returns:
None. This module is used to control the main menu of the application and does not return any value.
"""

from PyQt5.QtWidgets import QApplication

class MainMenuController:
    def __init__(self, main_controller):
        self.view = main_controller.view
        self.initialize_connections()

    def initialize_connections(self):
        self.view.main_menu.exit_action.triggered.connect(QApplication.instance().quit)
        self.view.main_menu.tools_action.triggered.connect(self.open_tools_window)
        self.view.main_menu.graphs_action.triggered.connect(self.open_graphs_window)

    def open_tools_window(self):
        print(f"Opening tools window")
        self.view.tools_window.open()

    def open_graphs_window(self):
        print(f"Opening graphs window")
        self.view.graphs_window.open()
        self.view.graphs_window.mel_spectrogram.plot_spe
