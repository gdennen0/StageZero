
"""
Module: CustomAxis

This module defines the CustomAxis class, which is a subclass of the AxisItem class from pyqtgraph. 
The CustomAxis class is used to customize the axis of a plot, specifically for displaying layers of a song.

The class has the following methods:
    - __init__: Initializes the CustomAxis instance and calls the constructor of the parent class, AxisItem.
    - setLayers: Sets the layers of the CustomAxis instance.
    - tickValues: Returns the major and minor ticks for the axis based on the minimum and maximum values and the size.
    - tickStrings: Returns the strings for the ticks based on the values, scale, and spacing.

Arguments:
    - *args: Variable length argument list.
    - **kwargs: Arbitrary keyword arguments.

Returns:
    - An instance of the CustomAxis class.
"""


import math  # For mathematical operations
import numpy as np  # For array operations
from pyqtgraph import AxisItem  # For customizing plots

class CustomAxis(AxisItem):  # Custom axis class
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call the constructor of the parent class
        self.layers = []  # Initialize the layers

    def setLayers(self, layers):  # Set the layers
        self.layers = layers  # Set the layers

    def tickValues(self, minVal, maxVal, size):  # Get the tick values
        minVal, maxVal = sorted((minVal, maxVal))  # Sort the minimum and maximum values
        ticks = []  # Initialize the ticks
        # Generate ticks at intervals of 1
        major_ticks = np.arange(math.floor(minVal), math.ceil(maxVal) + 1)  # Generate the major ticks
        ticks.append((1.0, major_ticks))  # Add the major ticks to the ticks
        # Generate ticks at intervals of 0.5
        minor_ticks = np.arange(math.floor(minVal * 2), math.ceil(maxVal * 2) + 1) / 2  # Generate the minor ticks
        ticks.append((0.5, minor_ticks))  # Add the minor ticks to the ticks
        return ticks  # Return the ticks

    def tickStrings(self, values, scale, spacing):  # Get the tick strings
        strings = []  # Initialize the strings
        for tick_value in values:  # For each tick value
            index = int(tick_value)  # Get the index
            if 0 <= index < len(self.layers) and tick_value % 1 == 0.5:  # If the index is valid and the tick value is a half integer
                strings.append(self.layers[index])  # Add the layer name to the strings
            else:  # Otherwise
                strings.append("")  # Add an empty string to the strings
        return strings  # Return the strings

