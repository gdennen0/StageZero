import numpy as np  # For array operations
import pyqtgraph as pg  # For plotting
from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QVBoxLayout,  # Box layout with a vertical direction
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class MelSpectrogramWidget(QWidget):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.layout = QVBoxLayout(self)  
          
    def plot(self, figure):
        canvas = FigureCanvas(figure)
        canvas_widget = QWidget()
        canvas_layout = QVBoxLayout(canvas_widget)  # Define canvas_layout before using it
        canvas_layout.addWidget(canvas)
        toolbar = NavigationToolbar(canvas, self)
        canvas_layout.addWidget(toolbar)
        canvas_widget.setLayout(canvas_layout)  # Now canvas_layout is defined
        self.layout.addWidget(canvas_widget)
