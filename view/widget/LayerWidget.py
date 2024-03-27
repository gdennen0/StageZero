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
from pyqtgraph import InfiniteLine, mkPen  # For customizing plots
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
)
from pyqtgraph import ViewBox, PlotWidget
from PyQt5.QtCore import pyqtSignal
import math  # For mathematical operations
import numpy as np  # For array operations
from pyqtgraph import AxisItem  # For customizing plots

class LayerWidget(QWidget):  # Widget for a layer

    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.plot_items = None
        self.layout = QHBoxLayout(self)  # Set the layout to horizontal box layout
        self.layout.setContentsMargins(0, 0, 12, 0)  # Set the margins for the layout
        self.y_axis = CustomAxis(orientation="left")  # Custom axis for the layer
        self.layer_plot = LayerPlot(viewBox=CustomViewBox(), axisItems={"left": self.y_axis})
        self.layout.addWidget(self.layer_plot)  # Add the plot widget to the layout
        
        self.layer_plot.setAcceptHoverEvents(True)
        self.layer_plot.setMouseTracking(True)
        self.layer_plot.setFixedHeight(0)  # Set the fixed height for the plot widget
        self.layer_plot.showGrid(x=True, y=True, alpha=1)  # Show the grid for the plot widget
        self.layer_plot.getViewBox().setMouseEnabled(x=True, y=False)  # Disable mouse interaction for the y-axis
        self.layer_plot.setMenuEnabled(False)  # Disable the right-click plot options

    def get_all_plot_items(self):
        return self.layer_plot.getViewBox().allChildren()

    def add_plot_item(self, plot_layer_item):  # Add a plot layer to the layer widget
        plot_layer_item.setZValue(10)
        self.layer_plot.addItem(plot_layer_item)

    def remove_items(self, items):
        for item in items:
            self.layer_plot.removeItem(item)
            print(f"[LayerWidget][remove_items] | Removed plot item: {item}")

    def remove_item(self, item):
        self.layer_plot.removeItem(item)
        print(f"[LayerWidget][remove_item] | Removed plot item: {item}")

    def update_layer_names(self, layer_names):  # Update the layer names
        self.y_axis.setLayers(layer_names)  # Set the layers for the custom axis

    def init_playhead(self):  # Initialize the vertical line
        line_specs = mkPen(color="w", width=2)  # Specifications for the line
        self.playhead = InfiniteLine(angle=90, movable=True, pen=line_specs)
        self.layer_plot.addItem(self.playhead)  # Add the line to the plot widget
        self.playhead.setPos(0)

    def add_playhead(self, playhead):  # Initialize the vertical line
        print(f"adding playhead to layer plot")
        self.layer_plot.addItem(playhead)  # Add the line to the plot widget

    def remove_group(self, plot_data_group):
        for plot_data_item in plot_data_group:
            self.layer_plot.removeItem(plot_data_item)
            print(f"removing plot data item: {plot_data_item}")

    def connectCustomViewBoxSignal(self, signal, slot):
        if signal == "sigItemsSelected":
            self.layer_plot.getViewBox().sigItemsSelected.connect(slot)

    def set_plot_x_max(self, x_max):
        self.layer_plot.setLimits(xMax=x_max)
        # self.layer_plot.autoRange(padding=0)

class LayerPlot(PlotWidget):
    def __init__(self, *args, **kwargs):
        super(LayerPlot, self).__init__(*args, **kwargs)


class CustomViewBox(ViewBox):
    sigLayerDrag = pyqtSignal(object, object)  # Signal to emit when items are selected
    sigLayerClick = pyqtSignal(object, object) # 

    def __init__(self, *args, **kwargs):
        super(CustomViewBox, self).__init__(*args, **kwargs)
        self.roi = None
        self.dragStartPos = None

    def mouseDragEvent(self, ev):
        self.sigLayerDrag.emit(ev, self)

    def mouseClickEvent(self, ev):
        self.sigLayerClick.emit(ev, self)


class CustomAxis(AxisItem):  # Custom axis class
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call the constructor of the parent class
        # self.layers = []  # Initialize the layers
        self.fixedWidth = 100  # Set a fixed width for the Y-axis

    def width(self):
        # Override the width method to return a fixed width
        return self.fixedWidth
    
    def resetLayers(self):
        self.layers = []
        self.update()

    def setLayers(self, layers):  # Set the layers
        self.layers = layers  # Set the layers
        self.update()