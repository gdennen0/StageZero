

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

class SongItem:
    # Song Item Attributes
    def __init__(self, name, path):
        self.name = name  # The name of the song
        self.path = path  # The path to the song file
        self.song_data, self.sample_rate = self.load_song_data(path)  # Load the song data and sample rate
        self.length_ms = self.calculate_length_ms()  # Calculate the length of the song in milliseconds
        self.frame_qty = self.calculate_frame_qty()  # Calculate the quantity of frames

    @staticmethod
    def load_song_data(path):
        # ingest song data & sample rate
        return librosa.load(path, sr=2000)  # Load the song data with a sample rate of 2000

    def calculate_length_ms(self):
        duration_sec = librosa.get_duration(y=self.song_data, sr=self.sample_rate)  # Get the duration of the song in seconds
        return duration_sec * 1000  # Convert the duration to milliseconds

    def calculate_frame_qty(self):
        frame_qty = round(self.length_ms / 1000 * constants.PROJECT_FPS)  # Calculate the quantity of frames
        return frame_qty

