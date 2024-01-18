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

class MelSpectrogramWidget(QWidget):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()

    def initialize(self):
        self.layout = QVBoxLayout(self)    

        # Assuming self.spectrogram_plot is a pyqtgraph.PlotWidget or similar
        self.spectrogram_plot = pg.PlotWidget(self)
        self.spectrogram_image = pg.ImageItem(axisOrder='row-major')  # Create an ImageItem
        self.spectrogram_plot.addItem(self.spectrogram_image)  # Add ImageItem to the PlotWidget
        self.layout.addWidget(self.spectrogram_plot)

    def plot_spectrogram(self, spectrogram_data):
        """
        Plot or update the spectrogram data on the spectrogram plot.

        :param spectrogram_data: A 2D numpy array representing the spectrogram data.
        """
        self.spectrogram_image.setImage(spectrogram_data.T, autoLevels=True)  # Transpose the data for correct orientation

