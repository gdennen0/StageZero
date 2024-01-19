"""
Module: MelSpectrogramWidget

This module defines a widget for displaying a Mel spectrogram. It uses PyQt5 for the user interface and pyqtgraph for plotting.

The MelSpectrogramWidget is a QWidget that contains a QVBoxLayout. Inside this layout, a PlotWidget is added which is used to display the spectrogram image.

The spectrogram image is a 2D numpy array that is transposed for correct orientation and displayed using an ImageItem from pyqtgraph.

Arguments:
    None

Returns:
    None

This module follows the Zen of Python by being simple and readable, with each method doing one clear task. It also avoids premature optimization, with a straightforward way of displaying the spectrogram.
"""

import numpy as np  # For array operations
import pyqtgraph as pg  # For plotting
from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QVBoxLayout,  # Box layout with a vertical direction
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class STFTLinearSpectrogramWidget(QWidget):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()

    def initialize(self):
        self.layout = QVBoxLayout(self)    

    def plot(self, figure):
        canvas = FigureCanvas(figure)
        canvas_widget = QWidget()

        canvas_layout = QVBoxLayout(canvas_widget)  # Define canvas_layout before using it
        canvas_layout.addWidget(canvas)

        # Create the navigation toolbar and add it to the canvas layout
        toolbar = NavigationToolbar(canvas, self)
        canvas_layout.addWidget(toolbar)
        
        canvas_widget.setLayout(canvas_layout)  # Now canvas_layout is defined
        self.layout.addWidget(canvas_widget)


