
"""
Module: SongOverviewController

This module defines the SongOverviewController class, which is responsible for controlling the song overview of the application. 
It initializes the connections for the song overview and defines the actions to be performed when the song overview is interacted with.

Arguments:
    main_controller (object): The main controller of the application. It is used to access the model and view of the application.

Returns:
    None. This module is used to control the song overview of the application and does not return any value.

This module follows the Model-View-Controller (MVC) design pattern. It acts as the controller for the song overview of the application.
It initializes the connections for the song overview and defines the actions to be performed when the song overview is interacted with.
This includes generating ticks for the song, initializing the playhead, painting beat lines, removing beat lines, and updating the playhead position.
"""




import math
import numpy as np
import constants


class SongOverviewController:
    def __init__(self, main_controller):
        self.model = main_controller.model  # Model reference
        self.song_overview_widget = main_controller.view.main_window.song_overview  # Song overview widget reference
        self.main_controller = main_controller  # Main controller reference
        self.view = main_controller.view  # View reference

    def generate_ticks(self):
        # Generate ticks for the song
        song = self.model.loaded_song.name
        length_ms = self.model.song.objects[song].length_ms
        frame_qty = self.calculate_frame_quantity(length_ms, constants.PROJECT_FPS)
        song_data = self.model.song.objects[song].song_data
        sample_rate = self.model.song.objects[song].sample_rate
        samples_per_frame = sample_rate / constants.PROJECT_FPS

        frame_numbers = np.arange(len(song_data)) / samples_per_frame

        return frame_numbers

    def init_playhead(self):
        # Initialize the vertical line
        song_overview_widget = self.view.main_window.song_overview
        song_overview_widget.init_playhead()
        self.main_controller.audio_playback_controller.time_update_thread.time_updated.connect(
            self.update_playhead_position
        )

    def paint_beat_lines(self, beats):
        for beat in beats:
            song_overview_widget = self.view.main_window.song_overview
            song_overview_widget.paint_beat_line(beat)

    def remove_beat_lines(self):
        song_overview_widget = self.view.main_window.song_overview
        song_overview_widget.remove_beat_lines()

    def paint_onset_lines(self, onsets, onset_type):
        song_overview_widget = self.view.main_window.song_overview

        if onset_type == "all-pass":
            for onset in onsets:
                song_overview_widget.paint_onset_line(onset, "all-pass", 'r')
        if onset_type == "lo-pass":
            for onset in onsets:
                song_overview_widget.paint_onset_line(onset, "lo-pass", 'g')


    def remove_onset_lines(self, onset_type):
        song_overview_widget = self.view.main_window.song_overview
        song_overview_widget.remove_onset_lines(onset_type)




    def update_playhead_position(self, frame_number):
        # Update the position of the vertical line
        self.view.main_window.song_overview.playhead.setPos(float(frame_number))

    def calculate_frame_quantity(self, length_ms, fps):
        # Calculate the frame quantity and round up to the nearest whole frame
        frame_qty = math.ceil((length_ms / 1000) * fps)
        print(f"# of frames for {(length_ms / 1000)}seconds @ {fps}fps is {frame_qty}")
        return frame_qty

    def create_frames_array(self, frame_qty):  # create tick array
        print(f"Creating {frame_qty} frame array")
        return np.arange(frame_qty)

    def update_plot(self):
        # Update the plot
        ticks = self.generate_ticks()
        song_data = self.model.song.objects[self.model.song.loaded_song].song_data
        self.song_overview_widget.update_plot(ticks, song_data)
        self.init_playhead()
