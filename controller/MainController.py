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

from .ProjectController import ProjectController
from .SongController import SongController
from .StackController import StackController
from .LayerController import LayerController
from .SongOverviewController import SongOverviewController
from .SongSelectController import SongSelectController
from .EventController import EventController
from .PlaybackModeController import PlaybackModeController
from .AudioPlaybackController import AudioPlaybackController
from .MainMenuController import MainMenuController
from .PlayheadController import PlayheadController
from .FilterEditorController import FilterEditorController
from .FilterAudioController import FilterAudioController
from .PluginWindowController import PluginWindowController
from click.ActionEngine import Action


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
        self.playback_mode_controller = PlaybackModeController(self)  # Creating an instance of PlaybackModeController
        self.main_menu_controller = MainMenuController(self)
        self.playhead_controller = PlayheadController(self)
        self.audio_playback_controller = AudioPlaybackController(self)  # Creating an instance of AudioPlaybackController
        self.filter_editor_controller = FilterEditorController()
        self.filter_audio_controller = FilterAudioController(self)
        self.plugin_window_controller = PluginWindowController(self)
        self.action = Action(self)

    def initialize_app(self):
        # Open the main window
        self.view.open_launch_window()  # Opening the launch window
        self.model.plugin.load_plugins(self)
        # Connect the launch windows new project button click signal to connect to project controller new project method

    def open_main_window(self):
        self.view.open_main_window()  # Opening the main window with the project name
        self.view.close_launch_window()

    def close_main_window(self):
        self.view.close_main_window()
