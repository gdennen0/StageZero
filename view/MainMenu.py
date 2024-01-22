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

from PyQt5.QtWidgets import (
    QMenuBar,
    QAction,
)

class MainMenu(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_menu_bar()

    def init_menu_bar(self):
        # File Menu Dropdown
        self.file_menu = self.addMenu('&File')

        self.save_action = QAction('&Save', self)
        self.exit_action = QAction('&Exit', self)
        
        self.save_action.setShortcut('Ctrl+S')
        self.exit_action.setShortcut('Ctrl+Q')

        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.exit_action)

        # View Menu Dropdown
        self.view_menu = self.addMenu('&View')
        
        self.tools_action = QAction('&Tools', self)
        self.graphs_action = QAction('&Graphs', self)

        self.view_menu.addAction(self.tools_action)
        self.view_menu.addAction(self.graphs_action)

        # Filter Menu Dropdown
        self.filter_menu = self.addMenu('&Filter')
        self.edit_filters_action = QAction('&Edit Filters', self)
        self.filter_audio_action = QAction('&Filter Audio', self)

        self.filter_menu.addAction(self.edit_filters_action)
        self.filter_menu.addAction(self.filter_audio_action)
