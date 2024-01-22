"""
Module: BPMTool

This module defines the BpmToolController class, which is responsible for handling the BPM (Beats Per Minute) tool in the application. 
The BpmToolController class is initialized with a main controller object and sets up connections between the BPM tool's UI elements and their corresponding functions.

Arguments:
    main_controller (object): The main controller object of the application. It provides access to the model, view, and other controllers.

Returns:
    None. The BpmToolController object is created to set up and handle interactions with the BPM tool in the application.

The BpmToolController class has several methods for handling different interactions with the BPM tool. These include estimating the BPM of a loaded song, updating the BPM label in the UI, adding beat lines to the song overview, and removing beat lines from the song overview. 
The BPM estimation is done using a separate tools module, and the results are used to update the UI and song overview accordingly.
"""

import tools

class BpmToolController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.stack = main_controller.model.stack
        self.model = main_controller.model
        self.view = main_controller.view
        self.init_connections()

    def init_connections(self):
        self.view.tools_window.bpm.count_button.clicked.connect(self.estimate_bpm)
        self.view.tools_window.bpm.paint_to_song_overview_button.clicked.connect(self.add_beats_to_song_overview)
        self.view.tools_window.bpm.remove_from_song_overview_button.clicked.connect(self.remove_beats_from_song_overview)
    
    def estimate_bpm(self):
        song_object = self.model.loaded_song
        tempo, beats = tools.estimate_bpm(song_object)
        # tempo is returned as a float
        # beats is returned as an np.ndarray

        self.update_time_label(int(tempo))

    def update_time_label(self, bpm):
        # Update the time label
        bpm_tool_widget = self.view.tools_window.bpm

        bpm_label_string = f"Tempo: {bpm}"
        print(bpm_label_string)

        bpm_tool_widget.bpm_label.setText(bpm_label_string)

    def add_beats_to_song_overview(self):
        song_object = self.model.loaded_song
        _, beats = tools.estimate_bpm(song_object)
        self.main_controller.song_overview_controller.paint_beat_lines(beats)

    def remove_beats_from_song_overview(self):
        self.main_controller.song_overview_controller.remove_beat_lines()


