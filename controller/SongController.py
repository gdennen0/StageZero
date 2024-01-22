
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

class SongController:
    def __init__(self, main_controller):
        self.main_controller = main_controller  # Main controller reference
        self.model = main_controller.model  # Model reference
        self.view = main_controller.view  # View reference

    def print(self, function_type, string):
        print(f"[CONTROLLER][{function_type}] | {string}")

    def add_song(self):
        # Add a song
        file_path = DialogWindow.open_file(
            "Select Song", "", "Audio Files (*.mp3 *.wav);;All Files (*)"
        )
        song_name = DialogWindow.input_text("Enter Song Name", "Song Name")
        song_object = self.model.song.build_song_object(file_path, song_name)
        self.model.song.add_song_object_to_model(
            song_object
        )
        self.main_controller.stack_controller.create_stack(song_name)
        if self.model.song.loaded_song == None:
            self.load_song(song_name)
        else:
            self.main_controller.song_select_controller.update_dropdown()

    def load_song(self, song_name):
        # Load a song
        self.print("load_song", f"current selected song: {song_name}")
        # Change loaded_song to song_name
        self.model.song.loaded_song = song_name
        # Change loaded_stack to song_name
        self.model.stack.loaded_stack = song_name
        # load the frame qty for the stack
        self.main_controller.stack_controller.set_stack_frame_qty(song_name)
        self.print("load_song", f"Updating song Plot")
        # Update the Song Overview Plot
        self.main_controller.song_overview_controller.update_plot()
        # Reload all of the layer plots
        # self.main_controller.layer_controller.init_plot(song_name)
        self.main_controller.layer_controller.reload_layer_plot()
        # Load the audio into the playback controller
        self.main_controller.audio_playback_controller.load_song()
        # reset the audio playback
        self.main_controller.audio_playback_controller.stop()
        self.main_controller.audio_playback_controller.reset()
        # reload the song select dropdown menu
        self.main_controller.song_select_controller.update_dropdown()

    def add_filter_to_loaded_song(self, filter_type, filtered_data, sample_rate):
        # (filter_type, filtered_data, sample_rate)
        self.model.loaded_song.add_filtered_data(filter_type, filtered_data, sample_rate)

