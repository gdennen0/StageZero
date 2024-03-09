from PyQt5.QtCore import Qt  # Add this line to import Qt

from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QVBoxLayout,  # Box layout with a vertical direction
    QHBoxLayout,
    QSizePolicy,  # Layout attribute describing horizontal and vertical resizing policy
    QMainWindow,
)

from .SongSelectWidget import SongSelectWidget
from .SongOverviewWidget import SongOverviewWidget
from .AudioPlaybackCommandWidget import AudioPlaybackCommandWidget
from .LayerControlWidget import LayerControlWidget
from .StackWidget import StackWidget
from .PlaybackModeWidget import PlaybackModeWidget

from ..UI_COLORS import UIColors


class StageWidget(QWidget):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()  # Initialize the widget
        self.initialize_ui_colors()

    def initialize_ui_colors(self):
        # Define UI elements and their properties
        ui_elements = {
            # self.song_select_menu: {"dropdown": True},
            self.song_overview: {"widget": True},
            self.layer_control: {"widget": True},
            self.stack: {"widget": True},
            self.playback_mode: {"widget": True},
            self.audio_playback_command: {"widget": True},
        }

                # Apply colors to all UI elements
        UIColors.initialize_ui_colors(ui_elements)
    from ..UI_COLORS import UIColors

    def initialize(self): 

        self.stage_widget = QWidget()
        self.stage_layout = QVBoxLayout()

        self.song_select_menu = SongSelectWidget()  # Widget for song selection
        self.song_select_menu.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Fixed
        )  # Set the size policy for song_select_menu
        self.song_overview = SongOverviewWidget()  # Widget for displaying song overview
        self.song_overview.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Fixed
        )  # Set the size policy for song_overview
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

        # Stage layout
        self.stage_layout = QVBoxLayout()
        self.stage_layout.addWidget(
            self.song_select_menu
        )  # Add the song_overview to the layout
        self.stage_layout.addLayout(
            self.playback_layout
        )  # Add the playback_layout to the layout
        self.stage_layout.addWidget(
            self.song_overview
        )  # Add the song_overview to the layout
        self.stage_layout.addWidget(self.stack)  # Add the stack to the layout
        self.stage_layout.addWidget(
            self.layer_control
        )  # Add the layer_control to the layout

        self.setLayout(self.stage_layout)  # Set the stage_layout as the layout of the StageWidget