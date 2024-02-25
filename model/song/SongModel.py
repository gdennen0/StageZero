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


class SongModel:
    # Manage Song Item Instances
    def __init__(self):
        self.objects = {}  # Dictionary to store song objects
        self.loaded_song = None  # The loaded song

    def load_model(song_model):
        # songs = song_model.objects
        # for song in
        pass

    # Method to take a file path and name and ingest the rest of the song item data
    @staticmethod
    def build_song_object(file_path, song_name):
        song_object = SongItem(song_name, file_path)  # Create a song object
        return song_object

    # Method to add song object to song dict
    def add_song_object_to_model(self, song_object):
        self.objects[song_object.name] = (
            song_object  # Add the song object to the dictionary
        )
        print(f"Added song '{song_object.name}' to model")
