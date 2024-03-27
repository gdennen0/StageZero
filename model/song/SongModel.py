"""
Module: SongModel

This module defines the SongModel class, which is responsible for managing SongItem instances. 
It provides methods to build song objects from file paths and song names, and to add these objects to a dictionary for easy retrieval.

Arguments: 
    file_path (str): The path to the song file.
    song_name (str): The name of the song.

Returns: 
    build_song_object: Returns a SongItem object.
    add_song_object_to_model: No return value. Adds the SongItem object to the dictionary of song objects.

The SongModel class is initialized with a class type of "MODEL", an empty dictionary to store song objects, and a None value for the loaded song.
The build_song_object method takes a file path and song name, creates a SongItem object, and returns it.
The add_song_object_to_model method takes a SongItem object and adds it to the dictionary of song objects, using the song name as the key.
"""

from .SongItem import SongItem
from pyqtgraph import InfiniteLine, mkPen  # For customizing plots

class SongModel:
    # Manage Song Item Instances
    def __init__(self):
        self.objects = {}  # Dictionary to store song objects
        self.loaded_song = None  # The loaded song
        self.playhead = InfiniteLine(angle=90, movable=True, pen=mkPen(color="w", width=2))

    def deserialize_songs(self, song_data):
        for song_name, song in song_data.items():
            self.objects[song_name] = SongItem()
            self.objects[song_name].deserialize(song)

    # Method to take a file path and name and ingest the rest of the song item data
    @staticmethod
    def build_song_object(file_path, song_name):
        song_object = SongItem()  # Create a song object
        song_object.build_data(song_name, file_path)

        return song_object
    
    def add_new_song(self, file_path, song_name):
        song_object = self.build_song_object(file_path, song_name)
        self.add_song_object_to_model(song_object)

    # Method to add song object to song dict
    def add_song_object_to_model(self, song_object):
        self.objects[song_object.name] = (
            song_object  # Add the song object to the dictionary
        )
        print(f"Added song '{song_object.name}' to model")
