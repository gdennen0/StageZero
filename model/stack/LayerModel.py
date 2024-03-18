"""
Module: LayerModel

This module defines the LayerModel class which is used to manage a collection of EventModel objects. Each EventModel object represents a layer in the application.

Arguments:
    layer_name (str): The name of the layer to be created or managed.
    index (int, optional): The index at which a new layer should be inserted. If not provided, the new layer is appended to the end of the list.
    object_data (list, optional): A list of objects to be added to a layer. This is used when setting event data for a layer.

Returns:
    get_layer_index: Returns the index of a layer given its name. If no layer with the given name exists, it returns None.
    get_layer_qty: Returns the quantity of layers currently managed by the LayerModel.
    create_layer: Returns nothing. It creates a new layer with the given name and adds it to the list of layers.
    set_event_data: Returns nothing. It sets the event data for a layer given its name and a list of objects.

The LayerModel class provides methods for creating new layers, getting the index of a layer given its name, getting the quantity of layers, and setting event data for a layer. It maintains a list of layers, where each layer is an instance of the EventModel class.
"""

from .EventModel import EventModel


class LayerModel:
    # Manage Layer Item Instances and events item instances
    def __init__(self):
        self.layers = []  # List to store layer objects
        self.frame_qty = None  # The quantity of frames

    def generate_plot_data_items(self):
        for layer in self.layers:
            layer.generate_plot_layer_data_items()

    def get_layer_index(self, layer_name):
        layer_names = {layer.name: index for index, layer in enumerate(self.layers)}
        return layer_names.get(layer_name, None)

    def get_layer_name(self, layer_index):
        for layer in self.layers:
            if self.layers.index(layer) == layer_index:
                return layer.name
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
            layer_index = self.get_layer_index(layer_name)
            print(f"getting layer index {layer_index}")
            self.layers[layer_index].set_index(layer_index)
        else:
            self.layers.insert(index, layer)  # Insert the layer at the specified index
            print(f"[MODEL] inserted Layer Object at index: {index}")  # Print a message
            self.update_layer_indices()  # Update the indices of the layers

    def set_event_data(self, layer_name, object_data):
        index = self.get_layer_index(layer_name)  # Get the index of the layer
        self.layers[index].objects = object_data  # Set the event data for the layer

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

    def delete_event(self, layer, frame):
        del self.layers[layer].objects[frame]
        print(f"Deleted event at frame {frame}")

    def get_event_data(self, layer, frame):
        return self.layers[layer].objects[frame]

    def move_event(self, layer_index, original_frame, new_frame):
        print(
            f"updating event layer index: {layer_index}\n...{   original_frame} ----> {new_frame}"
        )
        data = self.get_event_data(layer_index, original_frame)
        self.layers[layer_index].add(new_frame)
        self.layers[layer_index].update_data(new_frame, data)

        self.delete_event(layer_index, original_frame)

    def change_event_layer(self, original_layer, new_layer, frame_number):
        event = self.layers[original_layer].objects[frame_number]
        self.layers[new_layer].add(frame_number)
        event.parent_layer = self.layers[new_layer].name
        event.parent_layer_index = new_layer
        event.plot_data_item.layer_name = self.layers[new_layer].name
        event.plot_data_item.layer_index = new_layer
        event.plot_data_item.set_y_position(new_layer + .5)
        self.layers[new_layer].objects[frame_number] = event
        self.layers[original_layer].delete(frame_number)

        print(f"changing event {frame_number} from layer {original_layer} to layer {new_layer} \n event parent layer {event.parent_layer} parent layer index: {event.parent_layer_index},\n plotdataitem name {event.plot_data_item.layer_name}, layer_index {event.plot_data_item.layer_index}")