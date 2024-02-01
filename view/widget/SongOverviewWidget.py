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
from pyqtgraph import InfiniteLine, mkPen  # For customizing plots
from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QLabel,  # For displaying text or images
    QVBoxLayout,  # Box layout with a vertical direction
)
from ..UI_COLORS import UIColors

Y_AXIS_OFFSET = 100


class SongOverviewWidget(QWidget):  # Widget for displaying song overview
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initWidget()  # Initialize the widget
        self.initialize_ui_colors()

    def initialize_ui_colors(self):
        # Define UI elements and their properties
        ui_elements = {
            self: {"background": True},
        }

        # Apply colors to all UI elements
        UIColors.initialize_ui_colors(ui_elements)

        style_sheet = (
            f"background-color: {UIColors.BACKGROUND_COLOR};"
            f"QLabel {{ color: {UIColors.TEXT_COLOR}; }}"
            f"QPushButton {{ background-color: {UIColors.BUTTON_COLOR}; }}"
            f"QWidget {{ background-color: {UIColors.WIDGET_COLOR}; }}"
        )

        # Apply the concatenated style sheet
        self.setStyleSheet(style_sheet)

    def initWidget(self):  # Initialize the widget
        self.layout = QVBoxLayout(self)  # Set the layout to vertical box layout
        self.layout.setContentsMargins(0, 0, 12, 0)  # Set the margins for the layout
        self.label = QLabel(f"Song Overview")  # Label for the song overview

    def initWidget(self):
        self.layout = QVBoxLayout(self)  # Set the layout to vertical box layout
        self.layout.setContentsMargins(0, 0, 12, 0)  # Set the margins for the layout
        self.label = QLabel(f"Song Overview")  # Label for the song overview

        self.song_plot = pg.PlotWidget()  # Create a plot widget for the song

        self.song_plot.setFixedHeight(100)  # Set the fixed height of the song plot
        self.song_plot.setContentsMargins(
            0, 0, 0, 0
        )  # Set the margins for the song plot

        self.song_plot.showGrid(
            x=True, y=False, alpha=1
        )  # Show the grid for the song plot

        y_axis = self.song_plot.getAxis("left")  # Get the y-axis
        y_axis.setWidth(100)
        y_axis.setTicks([])  # Set the ticks for the y-axis

        x_axis = self.song_plot.getAxis("bottom")  # Get the y-axis
        x_axis.setTicks([])  # Set the ticks for the y-axis

        # self.layout.addWidget(self.label)  # Add the label to the layout
        self.layout.addWidget(self.song_plot)  # Add the song plot to the layout

    def init_playhead(self):
        line_specs = mkPen(color="w", width=2)  # Define the specifications for the line
        self.playhead = InfiniteLine(
            angle=90, movable=True, pen=line_specs
        )  # Create an infinite line
        self.song_plot.addItem(self.playhead)  # Add the line to the song plot

    def paint_beat_line(self, frame_number):
        line_specs = mkPen(color="b", width=1)  # Define the specifications for the line
        beat_line = InfiniteLine(
            angle=90, movable=False, pen=line_specs
        )  # Create an infinite line for beat
        beat_line.setPos(
            frame_number
        )  # Set the position of the line at specific tick number
        beat_line.beat = True  # Mark this line as a beat line
        self.song_plot.addItem(beat_line)  # Add the beat line to the song plot

    def remove_beat_lines(self):
        for item in self.song_plot.items():
            if isinstance(item, InfiniteLine) and getattr(item, "beat", False):
                self.song_plot.removeItem(
                    item
                )  # Remove the beat line from the song plot

    def paint_onset_line(self, frame_number, onset_type, color):
        line_specs = mkPen(
            color=color, width=1
        )  # Define the specifications for the line

    def remove_onset_lines(self, onset_type):
        for item in self.song_plot.items():
            if isinstance(item, InfiniteLine):
                if item.type == onset_type:
                    self.song_plot.removeItem(
                        item
                    )  # Remove the beat line from the song plot

    def plot_events(self, ticks, song_data):
        self.song_plot.setLimits(  # Set the limits for the song plot
            xMin=0,
            xMax=ticks[-1],
            yMin=0,
            yMax=1,
            minYRange=1,
            maxYRange=1,
        )
        self.song_plot.plot(ticks, song_data)  # Plot the song data

        y_axis = self.song_plot.getAxis("left")  # Get the y-axis
        y_axis.setTicks([])  # Set the ticks for the y-axis
        self.offset_y_axis_ticks()  # Call the method to format the Y-axis ticks

    def offset_y_axis_ticks(self):
        # Define a function to format the tick labels
        def tick_spacing(tick_values, scale, spacing=10):
            formatted_ticks = []
            for value in tick_values:
                formatted_value = "".center(10, " ")  # Ensure 10 empty space characters
                formatted_ticks.append((value, formatted_value))
            return formatted_ticks

        y_axis = self.song_plot.getAxis("left")  # Get the y-axis
        y_axis.setWidth(Y_AXIS_OFFSET)
        y_axis.setTicks(
            [tick_spacing(range(-10, 11), 1)]
        )  # Apply the custom tick formatting

    def update_plot(self, ticks, song_data):
        # logic to update plot
        self.song_plot.clear()  # Clear the song plot
        self.plot_events(ticks, song_data)  # Plot the events
