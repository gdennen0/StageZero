from PyQt5.QtCore import Qt  # Add this line to import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy

from .SongSelectWidget import SongSelectWidget
from .SongOverviewWidget import SongOverviewWidget
from .AudioPlaybackCommandWidget import AudioPlaybackCommandWidget
from .LayerControlWidget import LayerControlWidget
from .StackWidget import StackWidget
from .PlaybackModeWidget import PlaybackModeWidget

from ..UI_COLORS import UIColors


class StageWidget(QWidget):  # Inherit from QWidget
    def __init__(self, parent=None):
        super().__init__(parent)  # Call the constructor of QWidget
        self.initialize()  # Initialize the widget as before
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

    def initialize(self):

        self.stage_layout = QVBoxLayout()
        # Set the size policy to make the widget expandable
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.song_select_menu = SongSelectWidget()  # Widget for song selection
        self.song_overview = SongOverviewWidget()  # Widget for displaying song overview
        self.layer_control = LayerControlWidget()  # Widget for controlling layers
        self.stack = StackWidget()  # Widget for displaying the stack of layers
        self.audio_playback_command = AudioPlaybackCommandWidget()  # Widget for controlling audio playback
        self.playback_mode = PlaybackModeWidget()  # Widget for selecting the playback mode

        self.song_select_menu.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)  # Set the size policy for song_select_menu
        self.song_overview.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)  # Set the size policy for song_overview

        # playback layout
        self.playback_layout = QHBoxLayout()
        self.playback_layout.addWidget(self.playback_mode)  # Add the playback_mode to the playback_layout
        self.playback_layout.addWidget(self.audio_playback_command)  # Add the audio_playback_command to the playback_layout

        # Stage layout
        self.stage_layout.addWidget(self.song_select_menu)  # Add the song_overview to the layout
        self.stage_layout.addLayout(self.playback_layout)  # Add the playback_layout to the layout
        self.stage_layout.addWidget(self.song_overview)  # Add the song_overview to the layout
        self.stage_layout.addWidget(self.stack)  # Add the stack to the layout
        self.stage_layout.addWidget(self.layer_control)  # Add the layer_control to the layout

        self.setLayout(self.stage_layout)  # Set the layout on the widget

