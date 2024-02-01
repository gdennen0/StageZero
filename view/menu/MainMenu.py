"""
Module: MainMenu
This module defines the main menu bar of the application. It inherits from QMenuBar, a PyQt5 widget that provides a horizontal menu bar.

Arguments: 
parent (QWidget, optional): The parent widget of this menu bar. Defaults to None.

Returns: 
MainMenu object: An instance of the MainMenu class, which is a QMenuBar with predefined actions and shortcuts.

The MainMenu class has two main dropdowns: 'File' and 'View'. 
The 'File' dropdown contains 'Save' and 'Exit' actions, with shortcuts 'Ctrl+S' and 'Ctrl+Q' respectively.
The 'View' dropdown contains 'Tools' and 'Plots' actions.

Each action is an instance of QAction, a PyQt5 class for an abstract user interface action that can be inserted into widgets.
"""

from PyQt5.QtWidgets import QMenuBar
from .FileMenu import FileMenu
from .ViewMenu import ViewMenu
from .FilterMenu import FilterMenu


class MainMenu(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_menu = FileMenu(self)
        self.view_menu = ViewMenu(self)
        self.filter_menu = FilterMenu(self)
