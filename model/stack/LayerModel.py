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
        self.layers = {}  # List to store layer objects
        self.frame_qty = None  # The quantity of frames

    def generate_plot_data_items(self):
        for layer_key, layer_item in self.layers.items():
            layer_item.generate_plot_layer_data_items()

    def get_layer_qty(self):
        return len(self.layers)  # Returns the quantity of layers

    def create_layer(self, layer_name):
        self.add_layer_to_model(layer_name)  # Add a layer to the model

    def add_layer_to_model(self, layer_name):
        layer = EventModel()  # Create a new event model
        layer.set_layer_name(layer_name)
        layer.set_layer_number(self.get_next_free_layer_number())

        # Add a layer item to the layers dict
        if layer_name not in self.layers:
            self.layers[layer_name] = layer # Append the layer to the list
            print(f"[MODEL] Added Layer Object {layer_name}")  # Print a message
        else:
            print(f"error layer with that name already exists")
    
    def get_next_free_layer_number(self):
        used_numbers = [self.layers[layer].layer_number for layer in self.layers]
        next_free_number = 0
        while next_free_number in used_numbers:
            next_free_number += 1
        
        print(f"Next open index: {next_free_number}")
        return next_free_number
    
    # Sets the layers objects to object_data arg
    def set_event_data(self, layer_name, object_data):
        self.layers[layer_name].objects = object_data  # Set the event data for the layer

    def remove_layer_from_model(self, layer_name):
        del self.layers[layer_name]  # Delete the layer

    def get_layer_raw_data(self, layer_name):
        return self.layers[layer_name].objects  # Return the raw data of the layer

    def set_frame_qty(self, qty):
        self.frame_qty = qty  # Set the quantity of frames

    def delete_event(self, layer_name, event_key):
        del self.layers[layer_name].objects[event_key]
        print(f"Deleted event {event_key}")

    def get_event_data(self, layer_name, frame):
        return self.layers[layer_name].objects[frame]

    def move_event(self, layer_name, original_frame, new_frame):
        print(
            f"updating event layer: {layer_name}\n...{   original_frame} ----> {new_frame}"
        )
        data = self.get_event_data(layer_name, original_frame)
        self.layers[layer_name].add(new_frame)
        self.layers[layer_name].update_data(new_frame, data)

        self.delete_event(layer_name, original_frame)

    def change_event_layer(self, original_layer, new_layer, frame_number):
        if original_layer == new_layer:
            print(f"passing for frame {frame_number}")
            pass
        else:
            event = self.layers[original_layer].objects[frame_number] #get the event object
            self.layers[new_layer].add(frame_number)    # adding new frame on new layer
            event.parent_layer_name = self.layers[new_layer].layer_name
            event.parent_layer_number = self.layers[new_layer].layer_number
            event.plot_data_item.parent_layer_name = self.layers[new_layer].layer_name
            event.plot_data_item.parent_layer_number = self.layers[new_layer].layer_number
            event.plot_data_item.set_y_position(self.layers[new_layer].layer_number)
            self.layers[new_layer].objects[frame_number] = event # add data to new frame 
            self.layers[original_layer].delete(frame_number) # delete frame data from original layer
        # print(f"changing event {frame_number} from layer {original_layer} to layer {new_layer} \n event parent layer {event.parent_layer} parent layer index: {event.parent_layer_index},\n plotdataitem name {event.plot_data_item.layer_name}, layer_index {event.plot_data_item.layer_index}")