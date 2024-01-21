

"""
Module: MainModel

This module defines the MainModel class which serves as the central model for the application. It manages the 
SongModel and StackModel, which respectively handle the song and stack data. The MainModel class provides methods 
for accessing the currently loaded song and stack.

Arguments: None

Returns: 
    - get_loaded_stack: Returns the currently loaded stack from the StackModel.
    - loaded_song: Returns the currently loaded song from the SongModel. If no song is loaded, it prints an error message.

The MainModel class is initialized with a project name set to None, and instances of SongModel and StackModel. 
The project name can be updated later as required. The SongModel and StackModel instances are used to manage 
the song and stack data respectively.
"""

from .SongModel import SongModel
from .StackModel import StackModel

class MainModel:
    def __init__(self):
        self.project_name = None  # The name of the project
        self.song = SongModel()  # The song model
        self.stack = StackModel()  # The stack model

    def get_loaded_stack(self):
        # Returns the loaded stack
        return self.stack.loaded_stack

    @property
    def loaded_song(self):
        # Returns the loaded song
        if self.song.loaded_song:
            return self.song.objects[self.song.loaded_song]
        else:
            print(f"ERROR: No song loaded yet")  # Error message if no song is loaded

    @property
    def loaded_stack(self):
        if self.stack.loaded_stack:
            return self.stack.objects[self.stack.loaded_stack]
        else:
            print(f"ERROR: No stack loaded yet")  # Error message if no song is loaded

    
    def add_events_to_layer(self, layer_name, events):
        # events should be a dictionary of frame numbers
        layer_index = self.loaded_stack.get_layer_index(layer_name)
        for event in events:
            self.loaded_stack.layers[layer_index].add(event)
       

    # def add_new_layer(self, layer_name):
    #     layer_index = self.stack.objects[self.loaded_stack].layers.
