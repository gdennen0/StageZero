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
    QWidget,  # Base class for all user interface objects
    QHBoxLayout,  # Box layout with a horizontal direction
)
from ..CustomAxis import CustomAxis
from pyqtgraph import ViewBox
from PyQt5.QtCore import pyqtSignal


class LayerWidget(QWidget):  # Widget for a layer

    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.plot_items = None
        self.layout = QHBoxLayout(self)  # Set the layout to horizontal box layout
        self.layout.setContentsMargins(0, 0, 12, 0)  # Set the margins for the layout
        self.custom_axis = CustomAxis(orientation="left")  # Custom axis for the layer
        self.layer_plot = pg.PlotWidget(viewBox=CustomViewBox(), axisItems={"left": self.custom_axis})
        self.layout.addWidget(self.layer_plot)  # Add the plot widget to the layout
        
        self.layer_plot.setAcceptHoverEvents(True)
        self.layer_plot.setMouseTracking(True)
        self.layer_plot.setFixedHeight(0)  # Set the fixed height for the plot widget
        self.layer_plot.showGrid(x=True, y=True, alpha=1)  # Show the grid for the plot widget
        self.layer_plot.getViewBox().setMouseEnabled(x=True, y=False)  # Disable mouse interaction for the y-axis
        self.layer_plot.setMenuEnabled(False)  # Disable the right-click plot options
        self.init_playhead()

    def get_all_plot_items(self):
        return self.layer_plot.getViewBox().allChildren()

    def add_plot_item(self, plot_layer_item):  # Add a plot layer to the layer widget
        plot_layer_item.setZValue(10)
        self.layer_plot.addItem(plot_layer_item)

    def remove_items(self, items):
        """Remove a list of LayerPlotItem objects from the layer plot."""
        for item in items:
            self.layer_plot.removeItem(item)
            print(f"Removed plot item: {item}")

    def remove_item(self, item):
        """Remove a list of LayerPlotItem objects from the layer plot."""
        self.layer_plot.removeItem(item)
        print(f"Removed plot item: {item}")

    def update_layer_names(self, layer_names):  # Update the layer names
        # print(f"update layer names")
        for name in layer_names:
            print(name)
        self.custom_axis.setLayers(layer_names)  # Set the layers for the custom axis
        self.layer_plot.update()  # Update the plot widget

    def init_playhead(self):  # Initialize the vertical line
        line_specs = mkPen(color="w", width=2)  # Specifications for the line
        self.playhead = InfiniteLine(angle=90, movable=True, pen=line_specs)
        self.layer_plot.addItem(self.playhead)  # Add the line to the plot widget
        self.playhead.setPos(0)

    def reload_playhead(self):
        self.layer_plot.removeItem(self.playhead)
        self.init_playhead()

    def remove_group(self, plot_data_group):
        for plot_data_item in plot_data_group:
            self.layer_plot.removeItem(plot_data_item)
            print(f"removing plot data item: {plot_data_item}")

    def connectCustomViewBoxSignal(self, signal, slot):
        if signal == "sigItemsSelected":
            self.layer_plot.getViewBox().sigItemsSelected.connect(slot)


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