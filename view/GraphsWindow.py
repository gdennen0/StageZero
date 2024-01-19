"""
Module: GraphsWindow

This module defines the GraphsWindow class, which is a QWidget. The GraphsWindow class is used to create a window that displays different types of graphs to the user. The user can select the type of graph they want to view from a dropdown menu. The selected graph is then displayed in the window.

Arguments: None

The GraphsWindow class does not take any arguments. It initializes its own attributes during instantiation. These attributes include a QVBoxLayout for the main layout, a QComboBox for the graph selection dropdown menu, and a QStackedWidget to hold the different graph widgets.

The class also defines several methods for initializing the UI, initializing the graph widgets, and handling the event when a different graph is selected from the dropdown menu.

Returns: None

The GraphsWindow class does not return any values. It is used for its side effects of creating a window and displaying graphs.
"""

from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QVBoxLayout,  # Box layout with a vertical direction
    QComboBox,  # Drop down selection box
    QStackedWidget
)

from .STFTLinearSpectrogramWidget import STFTLinearSpectrogramWidget
from .LogFrequencyAxisWidget import LogFrequencyAxisWidget
from .MelSpectrogramWidget import MelSpectrogramWidget

class GraphsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Graphs')
        self.initializeUI()

    def initializeUI(self):
        # Main layout for the Tools window
        self.layout = QVBoxLayout(self)

        # Dropdown menu to select a tool
        self.graph_selector = QComboBox(self)
        self.graph_selector.addItems([
            "stft_linear_spectrogram", 
            "log_frequency_axis",
            "mel_spectrogram",
            ]
        )  
        self.layout.addWidget(self.graph_selector)

        # Stacked widget to hold different tool widgets
        self.graph_stack = QStackedWidget(self)
        self.layout.addWidget(self.graph_stack)

        self.initialize_graphs()

    def initialize_graphs(self):
        # Tool widgets are initialized and added to the stack here
        # Example tool widgets
        self.stft_linear_spectrogram = STFTLinearSpectrogramWidget()
        self.log_frequency_axis = LogFrequencyAxisWidget()
        self.mel_spectrogram = MelSpectrogramWidget()

        # Add tool widgets to the stack
        self.graph_stack.addWidget(self.stft_linear_spectrogram)
        self.graph_stack.addWidget(self.log_frequency_axis)
        self.graph_stack.addWidget(self.mel_spectrogram)

    def open_graph(self, index):
        # Change the current widget in the stack based on the selected tool

        self.graph_stack.setCurrentIndex(index)

    def open(self):
        # Show the Tools window
        self.show()
