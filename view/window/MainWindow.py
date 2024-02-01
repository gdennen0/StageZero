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

from ..widget.SongSelectWidget import SongSelectWidget
from ..widget.SongOverviewWidget import SongOverviewWidget
from ..widget.AudioPlaybackCommandWidget import AudioPlaybackCommandWidget
from ..widget.LayerControlWidget import LayerControlWidget
from ..widget.StackWidget import StackWidget
from ..widget.PlaybackModeWidget import PlaybackModeWidget
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
            self.central_widget: {"widget": True},
            self.song_overview: {"widget": True},
            self.layer_control: {"widget": True},
            self.stack: {"widget": True},
            self.playback_mode: {"widget": True},
            self.audio_playback_command: {"widget": True},
            self.menuBar(): {"main-menu": True},
        }

        # Apply colors to all UI elements
        UIColors.initialize_ui_colors(ui_elements)

        # style_sheet = (
        #     f"background-color: {UIColors.BACKGROUND_COLOR};"
        #     f"QLabel {{ color: {UIColors.TEXT_COLOR}; }}"
        #     f"QPushButton {{ "
        #     f"background-color: {UIColors.BUTTON_COLOR}; "
        #     f"color: {UIColors.BUTTON_TEXT_COLOR}; "  # Set the text color for buttons
        #     f"}}"
        #     f"QWidget {{ "
        #     f"background-color: {UIColors.WIDGET_COLOR}; "
        #     f"}}"
        #     # f"QMenuBar {{ "
        #     # f"background-color: {UIColors.MENU_BAR_COLOR}; "
        #     # f"color: {UIColors.MENU_BAR_TEXT_COLOR}; "
        #     # f"}}"
        #     # f"QMenuBar::item {{ "
        #     # f"background-color: {UIColors.MENU_BAR_ITEM_COLOR}; "
        #     # f"color: {UIColors.MENU_BAR_ITEM_TEXT_COLOR}; "
        #     # f"}} "
        #     # f"QMenuBar::item:selected {{ "
        #     # f"background-color: {UIColors.MENU_BAR_ITEM_SELECTED_COLOR}; "
        #     # f"}} "
        #     # f"QMenuBar::item:pressed {{ "
        #     # f"background-color: {UIColors.MENU_BAR_ITEM_PRESSED_COLOR}; "
        #     # f"}} "
        # )

        # Apply the concatenated style sheet
        # self.setStyleSheet(style_sheet)

    def open(self):  # Open the main window with a given title
        self.setWindowTitle("StageZero Dev")  # Set the window title
        self.show()  # Show the window

    def close(self):  # Close the main window
        self.close()  # Close the window

    def initialize(self):  # Initialize the main window
        self.central_widget = QWidget()  # Create a central widget

        self.main_layout = QVBoxLayout()  # Set the layout to vertical box layout
        self.central_widget.setLayout(self.main_layout)  # Set the main_layout as the layout for the central widget
        self.setCentralWidget(self.central_widget)  # Set the central widget for the QMainWindow
        self.main_layout.setSpacing(0)  # Set the spacing between widgets to 0

        self.song_select_menu = SongSelectWidget()  # Widget for song selection
        self.song_overview = SongOverviewWidget()  # Widget for displaying song overview
        self.layer_control = LayerControlWidget()  # Widget for controlling layers
        self.stack = StackWidget()  # Widget for displaying the stack of layers

        # playback layout
        self.playback_layout = QHBoxLayout()
        self.playback_mode = (
            PlaybackModeWidget()
        )  # Widget for selecting the playback mode
        self.playback_layout.addWidget(
            self.playback_mode
        )  # Add the playback_mode to the playback_layout
        self.audio_playback_command = (
            AudioPlaybackCommandWidget()
        )  # Widget for controlling audio playback
        self.playback_layout.addWidget(
            self.audio_playback_command
        )  # Add the audio_playback_command to the playback_layou

        # main program layout
        self.main_program_layout = QVBoxLayout()
        self.main_program_layout.addWidget(
            self.song_select_menu
        )  # Add the song_overview to the layout
        self.main_program_layout.addLayout(
            self.playback_layout
        )  # Add the playback_layout to the layout
        self.main_program_layout.addWidget(
            self.song_overview
        )  # Add the song_overview to the layout
        self.main_program_layout.addWidget(self.stack)  # Add the stack to the layout
        self.main_program_layout.addWidget(
            self.layer_control
        )  # Add the layer_control to the layout
        self.main_layout.addLayout(self.main_program_layout)  # add to the main_layout

        # Set the size policy for song_select_menu and song_overview
        self.song_select_menu.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Fixed
        )  # Set the size policy for song_select_menu
        self.song_overview.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Fixed
        )  # Set the size policy for song_overview

        self.setLayout(
            self.main_layout
        )  # Set the main_layout as the layout for the widget
