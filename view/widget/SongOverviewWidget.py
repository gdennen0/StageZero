"""
Module: SongOverviewWidget
This module defines a widget for displaying an overview of a song. It inherits from QWidget, a PyQt5 widget that provides a base class for all user interface objects. 

The SongOverviewWidget includes a label and a plot of the song. The plot is created using pyqtgraph, a Python library for scientific graphics and GUIs. The plot includes a grid and an infinite line that serves as a playhead. The playhead can be moved by the user to navigate through the song. 

The module also includes methods for painting beat lines on the plot and for removing these lines. Beat lines are represented as infinite lines and are painted at specific frame numbers. They are marked as beat lines using a custom attribute.

Arguments: 
None

Returns: 
An instance of SongOverviewWidget, which can be added to a layout in a PyQt5 application.
"""

import pyqtgraph as pg  # For plotting
from pyqtgraph import InfiniteLine, mkPen, PlotWidget  # For customizing plots
from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QLabel,  # For displaying text or images
    QVBoxLayout,  # Box layout with a vertical direction
)
from PyQt5.QtCore import pyqtSignal

Y_AXIS_OFFSET = 100


class SongOverviewWidget(QWidget):  # Widget for displaying song overview
    sigPlayheadPositionChange = pyqtSignal(float)  # Define a new signal for playhead position changes
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initWidget()  # Initialize the widget

    def initWidget(self):  # Initialize the widget
        self.layout = QVBoxLayout(self)  # Set the layout to vertical box layout
        self.layout.setContentsMargins(0, 0, 12, 0)  # Set the margins for the layout
        self.label = QLabel(f"Song Overview")  # Label for the song overview

    def initWidget(self):
        self.layout = QVBoxLayout(self)  # Set the layout to vertical box layout
        self.layout.setContentsMargins(0, 0, 12, 0)  # Set the margins for the layout
        self.label = QLabel(f"Song Overview")  # Label for the song overview
        self.song_plot = SongPlotItem()
        self.layout.addWidget(self.song_plot)  # Add the song plot to the layout

    def set_plot_x_max(self, x_max):
        self.song_plot.setLimits(xMax=x_max)
        self.song_plot.autoRange(padding=0)

    def add_waveform_data(self, waveform_item):
        print(f"[SongOverviewWidget][add_waveform_data] | {waveform_item}")
        self.song_plot.addItem(waveform_item)

    def remove_waveform_data(self, waveform_item):
        print(f"[SongOverviewWidget][remove_waveform_data] | {waveform_item}")
        self.song_plot.removeItem(waveform_item)

    def add_playhead(self, playhead):
        print(f"[SongOverviewWidget][add_playhead] | {playhead}")
        self.song_plot.addItem(playhead)  # Add the line to the song plot

    def emit_playhead_position(self):
        # print(f"emit playhead pos")
        x_position = self.playhead.getXPos()
        self.sigPlayheadPositionChange.emit(x_position)

    def add_line(self, frame_number, name):
        line_specs = mkPen(color="b", width=1)  # Define the specifications for the line
        line = InfiniteLine(angle=90, movable=False, pen=line_specs)  # Create an infinite line for beat
        line.name = name
        line.setPos(frame_number)  # Set the position of the line at specific tick number
        self.song_plot.addItem(line)

    def reload_plot(self, x_ticks, waveform_plot_item):
        self.song_plot.addItem(waveform_plot_item)
        self.set_plot_x_max(x_ticks[-1])
        
class SongPlotItem(PlotWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)  # Properly initialize the superclass
        self.setFixedHeight(100)  # Set the fixed height of the song plot
        self.setContentsMargins(0, 0, 0, 0)  # Set the margins for the song plot
        self.showGrid(x=True, y=False, alpha=1)  

        y_axis = self.getAxis("left")
        y_axis.setWidth(100)
        y_axis.setTicks([])  # Set the ticks for the y-axis

        x_axis = self.getAxis("bottom")
        x_axis.setTicks([])  # Set the ticks for the x-axis
        
        self.setLimits(  # Set the limits for the song plot
            xMin=0,
            xMax=1,
            yMin=0,
            yMax=1,
            minYRange=1,
            maxYRange=1,
        )

        