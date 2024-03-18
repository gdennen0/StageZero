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

import pickle
from .song.SongModel import SongModel
from .stack.StackModel import StackModel
from .plugin import PluginModel
import os
from PopupManager import PopupManager
import json
import types


class MainModel:
    def __init__(self):
        self.project_name = None  # The name of the project
        self.save_path = None
        self.song = SongModel()  # The song model
        self.stack = StackModel()  # The stack model
        self.plugin = PluginModel()

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
            # print(
            #     f"accessed loaded stack property method trying to get object {self.stack.loaded_stack} {type(self.stack.objects[self.stack.loaded_stack])}"
            # )
            return self.stack.objects[self.stack.loaded_stack]
        else:
            print(f"ERROR: No stack loaded yet")  # Error message if no song is loaded]

    def get_song(self, song_name):
        try:
            return self.song.objects[song_name]
        except KeyError:
            print(f"ERROR: Song '{song_name}' not found")
            return None

    def add_events_to_layer(self, layer_name, events):
        # events should be a dictionary of frame numbers
        for event in events:
            self.loaded_stack.layers[layer_name].add(event)

    def add_filtered_data(self, filter_name, filtered_data):
        self.loaded_song.add_filtered_data(filter_name, filtered_data)

    def serialize_stack(self):
        serialized_stacks = {}
        for stack_name, stack in self.stack.objects.items():
            serialized_layers = {}
            for layer_key, layer_item in stack.layers.items():
                serialized_events = {}
                for event_key, event in layer_item.objects.items():
                    # Serialize each event, excluding the plot_layer_item
                    serialized_events[event_key] = event.to_dict()
                serialized_layers[layer_key] = {
                    "frame_qty": stack.frame_qty,
                    "events": serialized_events,
                }
            serialized_stacks[stack_name] = {
                "loaded_stack": stack_name == self.loaded_stack,
                "layers": serialized_layers,
            }
        return serialized_stacks

    def save(self):
        print(
            f"saving loaded stack {self.stack.loaded_stack} type {type(self.loaded_stack)}"
        )
        # self.prepare_stack_data_for_saving()
        model_data = {
            "song_model": {
                "objects": self.song.objects,
                "loaded_song": self.song.loaded_song,
            },
            "stack_model": {
                "objects": self.serialize_stack(),
                "loaded_stack": self.stack.loaded_stack,
            },
            "main_model": {
                "save_path": self.save_path,
            },
        }

        print(self.serialize_stack())

        if self.save_path:
            with open(self.save_path, "wb") as file:
                pickle.dump(model_data, file)
            PopupManager.show_info("Success", "Project successfully saved")

        else:
            PopupManager.show_error("Error!", "No valid save destination")

    def load(self, path):
        # Check if the file is empty
        if os.path.getsize(path) == 0:
            print(f"ERROR: The file {path} is empty.")
            return

        with open(path, "rb") as file:
            data_loaded = pickle.load(file)
        self.song.objects = data_loaded["song_model"]["objects"]
        self.song.loaded_song = data_loaded["song_model"]["loaded_song"]
        # self.stack.objects = data_loaded["stack_model"]["objects"]
        self.stack.set_loaded_stack(data_loaded["stack_model"]["loaded_stack"])
        self.stack.deserialize_stack(data_loaded["stack_model"]["objects"])

        # self.stack.set_loaded_stack(data_loaded["stack_model"]["loaded_stack"])
        self.save_path = data_loaded["main_model"]["save_path"]
        self.stack.generate_plot_data_items()
