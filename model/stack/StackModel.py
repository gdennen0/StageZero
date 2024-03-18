"""
Module: StackModel

This module defines the StackModel class, which is responsible for managing a collection of LayerModel objects.
Each LayerModel object represents a layer in a stack, and the StackModel class provides methods for creating new stacks,
getting the currently loaded stack, and setting the quantity of frames for a specific stack.

Arguments: 
stack_name - The name of the stack. It is used as a key in the objects dictionary to store and retrieve LayerModel objects.
frame_qty - The quantity of frames for a specific stack. It is used to set the frame_qty attribute of a LayerModel object.

Returns: 
get_loaded_stack - This method returns the currently loaded stack.
"""

from .LayerModel import LayerModel
from view import LayerPlotItem
from pyqtgraph import GraphicsObject, PlotDataItem


class StackModel:
    def __init__(self):
        # Init the stack dict
        self.objects = {}  # Dictionary to store stack objects
        self.loaded_stack = None  # The loaded stack
        self.loaded_plot_data_group = {}

    # add a new stack
    def create_stack(self, stack_name):
        self.objects[stack_name] = (
            LayerModel()
        )  # Create a new layer model and add it to the dictionary

    def get_layer_items(self, layer_name):
        return self.objects[layer_name].event.items

    def set_loaded_stack(self, name):
        print(f"set loaded stack to: {name}")
        self.loaded_stack = name

    def load_data_from_dict(self, stack_data):
        for stack in stack_data:
            name = stack
            print(f"load_data_from_dict | layer: {name}")
            self.create_stack(name)

    def generate_plot_data_items(self):
        for stack_key, stack_item in self.objects.items():
            stack_item.generate_plot_data_items()

    def deserialize_stack(self, serialized_stacks):
        print(f"deserializeing stacks!")
        self.objects.clear()  # Clear existing data
        for stack_name, stack_info in serialized_stacks.items():
            print(f"    deserializing stack: {stack_name}")
            stack = LayerModel()  # Assuming LayerModel is used to represent each stack
            stack.frame_qty = stack_info.get("frame_qty", 0)
            for layer_name, layer_info in stack_info["layers"].items():
                print(f"deserializing layer {layer_name}")
                stack.create_layer(layer_name)
                for event_key, event_info in layer_info["events"].items():
                    print(f"deserializing event {event_key}, {event_info}")
                    stack.layers[layer_name].add(event_info["frame_number"])
                    event = stack.layers[layer_name].objects[
                        event_info["frame_number"]
                    ]
                    event.deserialize(
                        event_info
                    )  # Assuming EventItem has a deserialize method
            self.objects[stack_name] = stack
        # Set the loaded stack if needed
