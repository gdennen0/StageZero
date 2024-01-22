"""
Module: MainController

This module defines the MainController class, which is the central hub for all the other controllers in the application. 
It is responsible for initializing and managing the instances of all other controllers, and connecting them with the model and view components.

Arguments:
    model: The model component of the MVC architecture. It holds the data and the logic of the application.
    view: The view component of the MVC architecture. It is responsible for the user interface and the presentation of the data.

Returns:
    An instance of the MainController class, which can be used to control and manage the entire application.

The MainController class has an __init__ method that takes a model and a view as arguments, and assigns them to instance variables. 
It then initializes all the other controllers, passing itself as an argument to their constructors. 
This allows the other controllers to access the model and view through the MainController.

The MainController also has an initialize_app method, which opens the main window of the application and connects the new project button click signal to the project controller's new project method.
"""

from .Project import ProjectController
from .Song import SongController
from .Stack import StackController
from .Layer import LayerController
from .SongOverview import SongOverviewController
from .SongSelect import SongSelectController
from .Event import EventController
from .PlaybackMode import PlaybackModeController
from .AudioPlayback import AudioPlaybackController
from .MainMenu import MainMenuController
from .GraphWindow import GraphWindowController
from .ToolWindowController import BpmToolController, OnsetDetectionToolController, KicksToolController
from .FilterEditorController import FilterEditorController
from .FilterAudioController import FilterAudioController

class MainController:
    def __init__(self, model, view):
        self.model = model  # Assigning the model
        self.view = view  # Assigning the view

        # Centralize All of the controllers
        self.project_controller = ProjectController(self)  # Creating an instance of ProjectController
        self.song_controller = SongController(self)  # Creating an instance of SongController
        self.stack_controller = StackController(self)  # Creating an instance of StackController
        self.layer_controller = LayerController(self)  # Creating an instance of LayerController
        self.song_overview_controller = SongOverviewController(self)  # Creating an instance of SongOverviewController
        self.song_select_controller = SongSelectController(self)  # Creating an instance of SongSelectController
        self.event_controller = EventController(self)  # Creating an instance of EventController
        self.audio_playback_controller = AudioPlaybackController(self)  # Creating an instance of AudioPlaybackController
        self.playback_mode_controller = PlaybackModeController(self)  # Creating an instance of PlaybackModeController
        self.main_menu_controller = MainMenuController(self)
        self.bpm_tool_controller = BpmToolController(self)
        self.onset_detection_tool_controller = OnsetDetectionToolController(self)
        self.graph_window_controller = GraphWindowController(self)
        self.kicks_tool_controller = KicksToolController(self)
        self.filter_editor_controller = FilterEditorController()
        self.filter_audio_controller = FilterAudioController(self)

    def initialize_app(self):
        # Open the main window
        self.view.open_launch_window()  # Opening the launch window
        # Connect the launch windows new project button click signal to connect to project controller new project method
