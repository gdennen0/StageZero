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

from ..UI_COLORS import UIColors
import pyqtgraph as pg  # For plotting
from pyqtgraph import AxisItem, InfiniteLine, mkPen  # For customizing plots
from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QHBoxLayout,  # Box layout with a horizontal direction
)
from pyqtgraph.Qt import QtCore
from ..CustomAxis import CustomAxis
from pyqtgraph import RectROI
from view.LayerPlotItem import LayerPlotItem


class LayerWidget(QWidget):  # Widget for a layer
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.plot_items = None
        self.setStyleSheet(
            f"QToolTip {{ background-color: {UIColors.TOOL_TIP_BACKGROUND_COLOR}; color: {UIColors.TOOL_TIP_TEXT_COLOR}; border: 1px solid {UIColors.TOOL_TIP_BORDER_COLOR}; }}"
        )
        self.layout = QHBoxLayout(self)  # Set the layout to horizontal box layout
        self.layout.setContentsMargins(0, 0, 12, 0)  # Set the margins for the layout
        self.custom_axis = CustomAxis(orientation="left")  # Custom axis for the layer
        self.layer_plot = pg.PlotWidget(
            viewBox=CustomViewBox(), axisItems={"left": self.custom_axis}
        )
        self.layout.addWidget(self.layer_plot)  # Add the plot widget to the layout
        self.layer_plot.setAcceptHoverEvents(True)
        self.layer_plot.setMouseTracking(True)

        self.layer_plot.setFixedHeight(0)  # Set the fixed height for the plot widget
        self.layer_plot.showGrid(
            x=True, y=True, alpha=1
        )  # Show the grid for the plot widget
        self.layer_plot.getViewBox().setMouseEnabled(
            x=True, y=False
        )  # Disable mouse interaction for the y-axis
        self.layer_plot.setMenuEnabled(False)  # Disable the right-click plot options
        self.init_playhead()

    def get_all_plot_items(self):
        return self.layer_plot.getViewBox().allChildren()

    def add_plot_item(self, plot_layer_item):  # Add a plot layer to the layer widget
        plot_layer_item.setZValue(10)
        self.layer_plot.addItem(plot_layer_item)

    def clicked(x, y, z):
        print(f"Clicked! {x} {y} {z}")

    def remove_items(self, items):
        """Remove a list of LayerPlotItem objects from the layer plot."""
        for item in items:
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


from pyqtgraph import ViewBox, RectROI
from PyQt5.QtCore import Qt


class CustomViewBox(ViewBox):
    def __init__(self, *args, **kwargs):
        super(CustomViewBox, self).__init__(*args, **kwargs)
        self.roi = None
        self.dragStartPos = None

    def mouseDragEvent(self, ev, axis=None):
        if ev.button() == Qt.LeftButton and ev.modifiers() == Qt.ShiftModifier:
            ev.accept()
            pos = ev.scenePos()
            if ev.isStart():
                # Drag start
                print(f"unmapped:{pos}")
                self.dragStartPos = self.mapSceneToView(pos)
                print(f"mapped: {self.dragStartPos}")
                self.roi = RectROI(
                    [self.dragStartPos.x(), self.dragStartPos.y()], [1, 1], pen="w"
                )
                self.addItem(self.roi)
            elif ev.isFinish():
                # Drag finish, select items within ROI
                self.get_items_in_roi()
                self.removeItem(self.roi)
                self.roi = None
                self.dragStartPos = None
            else:
                # Drag update
                if self.roi and self.dragStartPos:
                    currentPos = self.mapSceneToView(pos)
                    self.roi.setSize(
                        [
                            currentPos.x() - self.dragStartPos.x(),
                            currentPos.y() - self.dragStartPos.y(),
                        ]
                    )
        else:
            super(CustomViewBox, self).mouseDragEvent(ev, axis)

    def get_items_in_roi(self):
        # Get the bounds of the ROI
        roi_bounds = self.roi.mapRectToParent(self.roi.boundingRect())
        print(f"ROI BOUNDS: {roi_bounds}")

        # List to hold items within the ROI
        selected_items = []

        # Iterate over all items in the ViewBox
        for item in self.allChildren():
            if hasattr(item, "pos"):
                # Ensure the item has a position attribute and is an instance of LayerPlotItem
                item_pos = item.pos()
                # print(f"item pos: {item_pos}")
                if roi_bounds.contains(item_pos):
                    # The item's position is within the ROI bounds
                    selected_items.append(item)
                    print(f"item within ROI bounds at pos {item_pos}")

        # Now you have a list of selected items
        # You can process these items further as needed
        print(f"Selected items: {selected_items}")
