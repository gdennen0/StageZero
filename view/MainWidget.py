
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
    QLabel,       # Provides a text or image display
    QListWidget,  # Provides a list view that can display items from a model
    QSplitter     # Provides a splitter that lets the user control the size of child widgets
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
        self.main_layout = QSplitter(Qt.Horizontal, self)  # Set the layout to vertical box layout

        self.song_select_menu = SongSelectWidget()  # Widget for song selection
        self.song_overview = SongOverviewWidget()  # Widget for displaying song overview
        self.layer_control = LayerControlWidget()  # Widget for controlling layers
        self.stack = StackWidget()  # Widget for displaying the stack of layers

        # playback layout
        self.playback_layout = QHBoxLayout()
        self.playback_mode = PlaybackModeWidget()  # Widget for selecting the playback mode
        self.playback_layout.addWidget(self.playback_mode)  # Add the playback_mode to the playback_layout
        self.audio_playback_command = AudioPlaybackCommandWidget()  # Widget for controlling audio playback
        self.playback_layout.addWidget(self.audio_playback_command)  # Add the audio_playback_command to the playback_layou
        
        # main program layout
        self.main_program_widget = QWidget()
        self.main_program_layout = QVBoxLayout()
        self.main_program_widget.setLayout(self.main_program_layout)
        self.main_program_layout.addWidget(self.song_select_menu)  # Add the song_overview to the layout
        self.main_program_layout.addLayout(self.playback_layout)  # Add the playback_layout to the layout
        self.main_program_layout.addWidget(self.song_overview)  # Add the song_overview to the layout
        self.main_program_layout.addWidget(self.stack)  # Add the stack to the layout
        self.main_program_layout.addWidget(self.layer_control)  # Add the layer_control to the layout
        self.main_layout.addWidget(self.main_program_widget)  # add to the main_layout

        self.song_filtered_data_widget = QWidget()
        self.song_filtered_data_layout = QVBoxLayout()
        self.song_filtered_data_widget.setLayout(self.song_filtered_data_layout)
        self.song_filtered_label = QLabel("Loaded Song's filtered data")
        self.song_filtered_data_layout.addWidget(self.song_filtered_label)
        self.song_filtered_data_list_widget = QListWidget()
        self.song_filtered_data_layout.addWidget(self.song_filtered_data_list_widget)


        self.side_bar_widget = QWidget()
        self.side_bar_layout = QVBoxLayout()
        self.side_bar_widget.setLayout(self.side_bar_layout)

        self.side_bar_layout.addLayout(self.song_filtered_data_layout)
        # add to main layout
        self.main_layout.addWidget(self.side_bar_widget)


        self.splitter_handle = self.main_layout.handle(1)  # Get the handle at the split position
        self.splitter_handle.setStyleSheet(
            "QSplitterHandle {background-color: darkgray;}"  # Set the handle color to dark gray to act as a marker
        )
         
        # Set the size policy for the main_program_widget to prevent it from collapsing
        self.main_program_widget.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))

        # Set the size policy for the side_bar_widget to allow it to be collapsible
        self.side_bar_widget.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred))

        self.main_layout.setSizes([1, 0])  # This will collapse the right side initially
