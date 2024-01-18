"""
Module: LayerWidget

This module defines the LayerWidget class, which is a QWidget subclass. The LayerWidget is a graphical user interface 
component that represents a layer in a plot. It includes a custom axis (CustomAxis) and a plot widget (pg.PlotWidget) 
for displaying the layer data. The LayerWidget also provides methods for adding plot layers, updating layer names, 
and initializing a playhead (a vertical line indicating the current position in the plot).

Arguments:
    None

Returns:
    An instance of the LayerWidget class.

The LayerWidget class follows the Zen of Python by being simple and readable, with each method doing one specific task. 
It also leverages the power of the PyQt5 and pyqtgraph libraries to provide a rich and interactive user interface.
"""

import pyqtgraph as pg  # For plotting
from pyqtgraph import AxisItem, InfiniteLine, mkPen  # For customizing plots
from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QHBoxLayout,  # Box layout with a horizontal direction
)

from .CustomAxis import CustomAxis

class LayerWidget(QWidget):  # Widget for a layer
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()  # Initialize the widget
        # self.setObjectName(layer_name)

    def initialize(self):  # Initialize the widget
        self.layout = QHBoxLayout(self)  # Set the layout to horizontal box layout
        self.layout.setContentsMargins(0, 0, 12, 0)  # Set the margins for the layout

        self.custom_axis = CustomAxis(orientation="left")  # Custom axis for the layer
        self.layer_plot = pg.PlotWidget(axisItems={"left": self.custom_axis})  # Plot widget for the layer
        self.layout.addWidget(self.layer_plot)  # Add the plot widget to the layout
        self.layer_plot.setFixedHeight(0)  # Set the fixed height for the plot widget
        self.layer_plot.showGrid(x=True, y=True, alpha=1)  # Show the grid for the plot widget
        # self.event_plot.setFixedHeight(35)
        self.layer_plot.getViewBox().setMouseEnabled(y=False)  # Disable mouse interaction for the y-axis

    def add_plot_layer(self, plot_layer_item):  # Add a plot layer to the layer widget
        # Add the PlotDataItem to the plot
        self.layer_plot.addItem(plot_layer_item)

    def update_layer_names(self, layer_names):  # Update the layer names
        self.custom_axis.setLayers(layer_names)  # Set the layers for the custom axis
        self.layer_plot.update()  # Update the plot widget

    def init_playhead(self):  # Initialize the vertical line
        line_specs = mkPen(color="w", width=2)  # Specifications for the line
        self.playhead = InfiniteLine(angle=90, movable=True, pen=line_specs)  # Create the line
        self.layer_plot.addItem(self.playhead)  # Add the line to the plot widget

