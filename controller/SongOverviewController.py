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

class SongOverviewController:
    def __init__(self, main_controller):
        self.model = main_controller.model
        self.song_overview_widget = (main_controller.view.main_window.stage_widget.song_overview)
        self.view = main_controller.view

    def calculate_frame_quantity(self, length_ms, fps):
        # Calculate the frame quantity and round up to the nearest whole frame
        frame_qty = math.ceil((length_ms / 1000) * fps)
        print(f"# of frames for {(length_ms / 1000)}seconds @ {fps}fps is {frame_qty}")
        return frame_qty

    def create_frames_array(self, frame_qty):  # create tick array
        print(f"Creating {frame_qty} frame array")
        return np.arange(frame_qty)

    def refresh(self):
        x_axis = self.model.loaded_song.x_axis
        waveform_plot_item = self.model.loaded_song.waveform_plot_item
        self.song_overview_widget.reload_plot(x_axis, waveform_plot_item)
        
    def clear_plot_waveforms(self):
        if self.model.loaded_song:
            self.song_overview_widget.remove_waveform_data(self.model.loaded_song.waveform_plot_item)

    def show_lines(self, type):
        for line in self.model.loaded_song.lines:
            if line.type == type:
                self.song_overview_widget.song_plot.addItem(line)

    def remove_lines(self, type):
        for line in self.model.loaded_song.lines:
            print(f"[SongOverviewController][remove_lines] (type:{type}| line type: {line.type}")
            if line.type == type:
                self.song_overview_widget.song_plot.removeItem(line)