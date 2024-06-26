"""
Module: SongController

This module defines the SongController class, which is responsible for managing the songs in the application. 
It provides functionalities to add and load songs, and interacts with other controllers to update the view and model components accordingly.

Arguments:
    main_controller: A reference to the main controller. It is used to access the model and view components, and other controllers.

Returns:
    None. This class does not return anything but modifies the model and view components through its methods.

The SongController class has methods to add and load songs. When a song is added, it opens a dialog window for the user to select a song file and enter a song name. 
The song object is then built and added to the model. If no song is currently loaded, it loads the newly added song. Otherwise, it updates the song select dropdown menu.

When a song is loaded, it updates the loaded song and stack in the model, sets the stack frame quantity, updates the song overview plot, reloads the layer plot, 
loads the audio into the playback controller, resets the audio playback, and reloads the song select dropdown menu.
"""

from view import DialogWindow
import re
from PopupManager import PopupManager


class SongController:
    def __init__(self, main_controller):
        self.main_controller = main_controller  # Main controller reference
        self.model = main_controller.model  # Model reference
        self.view = main_controller.view  # View reference

    def initialize(self):
        self.main_controller.audio_playback_controller.load_song(self.model.loaded_song)  # Load the song into audio playback

    def print(self, function_type, string):
        print(f"[CONTROLLER][{function_type}] | {string}")

    def add_song(self):
        file_path = DialogWindow.open_file("Select Song", "", "Audio Files (*.mp3 *.wav);;All Files (*)")
        if not file_path:
            PopupManager.show_error("Error", "No file selected. Please select a file.")
            return
        song_name = DialogWindow.input_text("Enter Song Name", "Song Name")
        if not re.match("^[a-zA-Z0-9_ -]+$", song_name):
            PopupManager.show_error(
                "Error",
                "Invalid song name. Please use only letters, numbers, spaces, hyphens, and underscores.",
            )
            return
        self.model.song.add_new_song(file_path, song_name)
        self.main_controller.stack_controller.create_stack(song_name)

        if self.model.song.loaded_song == None:
            self.load_song(song_name)
        else:
            self.main_controller.song_select_controller.refresh()

    def load_song(self, song_name):
        print(f"[SongController][load_plot]| song_name: {song_name}")
        print(f"loading song {song_name}".center(100,"*"))
        self.main_controller.song_overview_controller.clear_plot_waveforms() # Clear existing data
        self.main_controller.event_controller.clear_plot_events()
        self.model.song.loaded_song = song_name # Switch loaded song to new selected song
        self.model.stack.loaded_stack = song_name # Switch loaded stack to new selected song
        self.main_controller.song_overview_controller.refresh()
        self.main_controller.layer_controller.refresh()
        self.main_controller.audio_playback_controller.refresh()
        self.main_controller.song_select_controller.refresh()

    def add_filter_to_loaded_song(self, filter_type, filtered_data, sample_rate):
        self.model.loaded_song.add_filtered_data(filter_type, filtered_data, sample_rate)
