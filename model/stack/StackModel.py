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
