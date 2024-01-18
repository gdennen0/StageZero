
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

from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QVBoxLayout,  # Box layout with a vertical direction
    QSizePolicy,  # Layout attribute describing horizontal and vertical resizing policy
)

from .SongSelectWidget import SongSelectWidget
from .SongOverviewWidget import SongOverviewWidget
from .AudioPlaybackCommandWidget import AudioPlaybackCommandWidget
from .LayerControlWidget import LayerControlWidget
from .StackWidget import StackWidget
from .PlaybackModeWidget import PlaybackModeWidget

class MainWidget(QWidget):  # Class for the main window
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()  # Initialize the main window

    def open(self, title):  # Open the main window with a given title
        self.label = title  # Set the window title
        self.setWindowTitle(self.label)  # Set the window title
        self.show()  # Show the window

    def close(self):  # Close the main window
        self.close()  # Close the window

    def initialize(self):  # Initialize the main window
        self.layout = QVBoxLayout(self)  # Set the layout to vertical box layout
        self.layout.setSpacing(0)  # Set spacing to zero

        self.song_select_menu = SongSelectWidget()  # Widget for song selection
        self.song_overview = SongOverviewWidget()  # Widget for displaying song overview
        self.audio_playback_command = AudioPlaybackCommandWidget()  # Widget for controlling audio playback
        self.layer_control = LayerControlWidget()  # Widget for controlling layers
        self.stack = StackWidget()  # Widget for displaying the stack of layers
        self.playback_mode = PlaybackModeWidget()  # Widget for selecting the playback mode

        # Set the size policy for song_select_menu and song_overview
        self.song_select_menu.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)  # Set the size policy for song_select_menu
        self.song_overview.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)  # Set the size policy for song_overview

        self.layout.addWidget(self.song_select_menu)  # Add the song_select_menu to the layout
        self.layout.addWidget(self.song_overview)  # Add the song_overview to the layout
        self.layout.addWidget(self.playback_mode)  # Add the playback_mode to the layout
        self.layout.addWidget(self.audio_playback_command)  # Add the audio_playback_command to the layout
        self.layout.addWidget(self.layer_control)  # Add the layer_control to the layout
        self.layout.addWidget(self.stack)  # Add the stack to the layout
