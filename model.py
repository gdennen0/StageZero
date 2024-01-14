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
        self.project_name = None
        self.song = SongModel()
        self.stack = StackModel()

    def get_loaded_stack(self):
        return self.stack.loaded_stack

    @property
    def loaded_song(self):
        if self.song.loaded_song:
            return self.song.objects[self.song.loaded_song]
        else:
            print(f"ERROR: No file loaded yet")


class SongModel:
    # Manage Song Item Instances
    def __init__(self):
        self.CLASS_TYPE = "MODEL"
        self.objects = {}
        self.loaded_song = None

    # Method to take a file path and name and ingest the rest of the song item data
    @staticmethod
    def build_song_object(file_path, song_name):
        song_object = SongItem(song_name, file_path)
        return song_object

    # Method to add song object to song dict
    def add_song_object_to_model(self, song_object):
        self.objects[song_object.name] = song_object


class SongItem:
    # Song Item Attributes
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.song_data, self.sample_rate = self.load_song_data(path)
        self.length_ms = self.calculate_length_ms()
        self.frame_qty = self.calculate_frame_qty()

    @staticmethod
    def load_song_data(path):
        # ingest song data & sample rate
        return librosa.load(path, sr=2000)

    def calculate_length_ms(self):
        duration_sec = librosa.get_duration(y=self.song_data, sr=self.sample_rate)
        return duration_sec * 1000

    def calculate_frame_qty(self):
        frame_qty = round(self.length_ms / 1000 * constants.PROJECT_FPS)
        return frame_qty


class StackModel:
    def __init__(self):
        # Init the stack dict
        self.objects = {}
        self.loaded_stack = None

    # add a new stack
    def create_stack(self, stack_name):
        self.objects[stack_name] = LayerModel()

    def get_loaded_stack(self):
        return self.loaded_stack

    def set_frame_qty(self, stack_name, frame_qty):
        self.objects[stack_name].frame_qty = frame_qty


class LayerModel:
    # Manage Layer Item Instances and events item instances
    def __init__(self):
        # Init the layers dict
        self.layers = []
        self.frame_qty = None
        # objet global frame_qty

    def get_layer_index(self, layer_name):
        for index, layer in enumerate(self.layers):
            print(f"There are {len(self.layers)} layers in the list.")
            print(f"Checking layer at index: {index} whose name is {layer.name}")
            if layer.name == layer_name:
                print(
                    f"[MODEL][LAYERMODEL][get_layer_index] | Matched layer named: {layer_name} to index {index}"
                )
                return index
        print(
            f"[MODEL][LAYERMODEL][get_layer_index] | No matched layer named: {layer_name}"
        )
        return None

    def get_layer_qty(self):
        return len(self.layers)

    def create_layer(self, layer_name):
        self.add_layer_to_model(layer_name)

    def add_layer_to_model(self, layer_name, index=None):
        layer = EventModel(layer_name)
        # Add a layer item to the layers dict
        if index is None:
            self.layers.append(layer)
            print(f"[MODEL] appended Layer Object {layer_name}")
        else:
            self.layers.insert(index, layer)
            print(f"[MODEL] inserted Layer Object at index: {index}")
            self.update_layer_indices()

    def set_event_data(self, layer_name, object_data):
        index = self.get_layer_index(layer_name)
        self.layers[index].objects = object_data

    def create_layer_plot_data_item(self, layer_name):
        index = self.get_layer_index(layer_name)
        self.layers[index].plot_data_item = ClickablePlotDataItem()

    def set_event_plot_data_item(self, layer_name, plot_data):
        index = self.get_layer_index(layer_name)
        self.layers[index].plot_data_item = ClickablePlotDataItem(
            plot_data, symbol="o", pen=None
        )

    def remove_layer_from_model(self, layer_name):
        # Filter out the layer with the given layer_name
        layer_index = self.get_layer_index(layer_name)
        del self.layers[layer_index]
        # self.update_layer_indices()

    def move_layer_to_index(self, layer_name, new_index):
        # Find the layer with the given layer_name
        layer_to_move = next(
            (layer for layer in self.layers if layer["layer_name"] == layer_name), None
        )
        # If the layer exists, proceed
        if layer_to_move is not None:
            # Remove the layer from its current position
            self.layers.remove(layer_to_move)
            # Insert the layer at the new index
            self.layers.insert(new_index, layer_to_move)
            # Update the indices of all layers
            self.update_layer_indices()

    def get_layer_raw_data(self, layer_name):
        index = self.get_layer_index(layer_name)
        return self.layers[index].objects

    def update_layer_indices(self):
        for i, layer in enumerate(self.layers):
            layer.index = i

    def set_frame_qty(self, qty):
        self.frame_qty = qty

class ClickablePlotDataItem(PlotDataItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mouseClickEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            ev.accept()
            print("PlotDataItem clicked")

class EventModel:
    def __init__(self, name):
        self.name = name
        self.objects = {}
        self.plot_data_item = None

    def add(self, index):
        self.objects[index] = EventItem()


class LayerItem:
    def __init__(self, layer_name):
        self.name = layer_name
        self.event = EventModel()


class EventItem:
    def __init__(self, event_name="Default", color=(255,255,255)):
        self.name = event_name
        self.color = color