import librosa
import pyqtgraph as pg
from pyqtgraph import PlotDataItem, mkPen
from PyQt5.QtCore import Qt




import constants

# =========================================================================================================================================
# Model Classes
# =========================================================================================================================================


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
            print(f"ERROR: No file loaded yet")  # Error message if no song is loaded


class SongModel:
    # Manage Song Item Instances
    def __init__(self):
        self.CLASS_TYPE = "MODEL"  # Class type
        self.objects = {}  # Dictionary to store song objects
        self.loaded_song = None  # The loaded song

    # Method to take a file path and name and ingest the rest of the song item data
    @staticmethod
    def build_song_object(file_path, song_name):
        song_object = SongItem(song_name, file_path)  # Create a song object
        return song_object

    # Method to add song object to song dict
    def add_song_object_to_model(self, song_object):
        self.objects[song_object.name] = song_object  # Add the song object to the dictionary


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


class StackModel:
    def __init__(self):
        # Init the stack dict
        self.objects = {}  # Dictionary to store stack objects
        self.loaded_stack = None  # The loaded stack

    # add a new stack
    def create_stack(self, stack_name):
        self.objects[stack_name] = LayerModel()  # Create a new layer model and add it to the dictionary

    def get_loaded_stack(self):
        # Returns the loaded stack
        return self.loaded_stack

    def set_frame_qty(self, stack_name, frame_qty):
        self.objects[stack_name].frame_qty = frame_qty  # Set the quantity of frames for the stack


class LayerModel:
    # Manage Layer Item Instances and events item instances
    def __init__(self):
        # Init the layers dict
        self.layers = []  # List to store layer objects
        self.frame_qty = None  # The quantity of frames
        # objet global frame_qty

    def get_layer_index(self, layer_name):
        for index, layer in enumerate(self.layers):
            print(f"There are {len(self.layers)} layers in the list.")  # Print the quantity of layers
            print(f"Checking layer at index: {index} whose name is {layer.name}")  # Print the index and name of the current layer
            if layer.name == layer_name:
                print(
                    f"[MODEL][LAYERMODEL][get_layer_index] | Matched layer named: {layer_name} to index {index}"
                )  # Print a message if the layer name matches
                return index
        print(
            f"[MODEL][LAYERMODEL][get_layer_index] | No matched layer named: {layer_name}"
        )  # Print a message if no layer name matches
        return None

    def get_layer_qty(self):
        return len(self.layers)  # Returns the quantity of layers

    def create_layer(self, layer_name):
        self.add_layer_to_model(layer_name)  # Add a layer to the model

    def add_layer_to_model(self, layer_name, index=None):
        layer = EventModel(layer_name)  # Create a new event model
        # Add a layer item to the layers dict
        if index is None:
            self.layers.append(layer)  # Append the layer to the list
            print(f"[MODEL] appended Layer Object {layer_name}")  # Print a message
        else:
            self.layers.insert(index, layer)  # Insert the layer at the specified index
            print(f"[MODEL] inserted Layer Object at index: {index}")  # Print a message
            self.update_layer_indices()  # Update the indices of the layers

    def set_event_data(self, layer_name, object_data):
        index = self.get_layer_index(layer_name)  # Get the index of the layer
        self.layers[index].objects = object_data  # Set the event data for the layer

    def create_layer_plot_data_item(self, layer_name):
        index = self.get_layer_index(layer_name)  # Get the index of the layer
        self.layers[index].plot_data_item = ClickablePlotDataItem()  # Create a new clickable plot data item for the layer

    def set_event_plot_data_item(self, layer_name, plot_data):
        index = self.get_layer_index(layer_name)  # Get the index of the layer
        self.layers[index].plot_data_item = ClickablePlotDataItem(
            plot_data, symbol="o", pen=None
        )  # Create a new clickable plot data item with the specified plot data

    def remove_layer_from_model(self, layer_name):
        # Filter out the layer with the given layer_name
        layer_index = self.get_layer_index(layer_name)  # Get the index of the layer
        del self.layers[layer_index]  # Delete the layer
        # self.update_layer_indices()

    def move_layer_to_index(self, layer_name, new_index):
        # Find the layer with the given layer_name
        layer_to_move = next(
            (layer for layer in self.layers if layer["layer_name"] == layer_name), None
        )  # Find the layer with the specified name
        # If the layer exists, proceed
        if layer_to_move is not None:
            # Remove the layer from its current position
            self.layers.remove(layer_to_move)
            # Insert the layer at the new index
            self.layers.insert(new_index, layer_to_move)
            # Update the indices of all layers
            self.update_layer_indices()

    def get_layer_raw_data(self, layer_name):
        index = self.get_layer_index(layer_name)  # Get the index of the layer
        return self.layers[index].objects  # Return the raw data of the layer

    def update_layer_indices(self):
        for i, layer in enumerate(self.layers):
            layer.index = i  # Update the index of the layer

    def set_frame_qty(self, qty):
        self.frame_qty = qty  # Set the quantity of frames

class ClickablePlotDataItem(PlotDataItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call the parent constructor

    def mouseClickEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            ev.accept()  # Accept the event
            print("PlotDataItem clicked")  # Print a message

class EventModel:
    def __init__(self, name):
        self.name = name  # The name of the event
        self.objects = {}  # Dictionary to store event objects
        self.plot_data_item = None  # The plot data item

    def add(self, index):
        self.objects[index] = EventItem()  # Add an event item to the dictionary


class LayerItem:
    def __init__(self, layer_name):
        self.name = layer_name  # The name of the layer
        self.event = EventModel()  # The event model


class EventItem:
    def __init__(self, event_name="Default", color=(255,255,255)):
        self.name = event_name  # The name of the event
        self.color = color  # The color of the event
