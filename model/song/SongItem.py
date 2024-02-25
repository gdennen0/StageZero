"""
Module: SongItem

This module defines the SongItem class, which is used to represent a song item in the application.
Each SongItem object encapsulates the details of a song, including its name, path, data, sample rate, length in milliseconds, and quantity of frames.

The SongItem class provides methods for loading song data, calculating the length of the song in milliseconds, and calculating the quantity of frames.

Arguments:
    name: The name of the song.
    path: The path to the song file.

Returns:
    An instance of the SongItem class.

"""

import librosa
import constants
import numpy as np
from ..pool.PoolModel import PoolModel


class SongItem:
    # Song Item Attributes
    def __init__(self, name, path):
        self.name = name  # The name of the song
        self.path = path  # The path to the song file
        self.song_data, self.sample_rate = self.load_song_data(
            path
        )  # Load the song data and sample rate
        (
            self.original_song_data,
            self.original_sample_rate,
        ) = self.get_original_song_data(path)
        self.length_ms = (
            self.calculate_length_ms()
        )  # Calculate the length of the song in milliseconds
        self.frame_qty = self.calculate_frame_qty()  # Calculate the quantity of frames
        self.filter = {}
        self.x_axis = self.generate_x_axis()
        self.pool = PoolModel()

    @staticmethod
    def load_song_data(path):
        # ingest song data & sample rate
        return librosa.load(
            path, sr=2000
        )  # Load the song data with a sample rate of 2000

    def calculate_length_ms(self):
        duration_sec = librosa.get_duration(
            y=self.song_data, sr=self.sample_rate
        )  # Get the duration of the song in seconds
        return duration_sec * 1000  # Convert the duration to milliseconds

    def calculate_frame_qty(self):
        frame_qty = round(
            self.length_ms / 1000 * constants.PROJECT_FPS
        )  # Calculate the quantity of frames
        return frame_qty

    def generate_x_axis(self):
        # Generate x axis items for the song
        samples_per_frame = self.sample_rate / constants.PROJECT_FPS
        x_axis_frame_numbers = np.arange(len(self.song_data)) / samples_per_frame

        return x_axis_frame_numbers

    def get_original_song_data(self, path):
        song_data, sample_rate = librosa.load(path)
        return song_data, sample_rate

    def add_filtered_data(self, filter_name, filtered_data):
        self.filter[filter_name] = FilterItem(filtered_data)
        print(f"Adding FilterItem {filter_name} ")

    @property
    def filtered_song_data(self, filter_type):
        if filter_type in self.filters:
            return self.filters[filter_type].data


class FilterItem:
    def __init__(self, filtered_data):
        self.filtered_data = filtered_data
