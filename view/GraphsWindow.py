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
        self.graph_selector.addItems(["Mel Spectrogram", "Graph 2", "Graph 3"])  # Add tool names here
        self.graph_selector.currentIndexChanged.connect(self.toolSelected)
        self.layout.addWidget(self.graph_selector)

        # Stacked widget to hold different tool widgets
        self.graph_stack = QStackedWidget(self)
        self.layout.addWidget(self.graph_stack)

        # Initialize tool widgets and add them to the stack
        self.initialize_graphs()

    def initialize_graphs(self):
        # Tool widgets are initialized and added to the stack here
        # Example tool widgets
        self.mel_spectrogram = MelSpectrogramWidget()
        self.graph2_widget = QWidget()
        self.graph3_widget = QWidget()

        # Add tool widgets to the stack
        self.graph_stack.addWidget(self.mel_spectrogram)
        self.graph_stack.addWidget(self.graph2_widget)
        self.graph_stack.addWidget(self.graph3_widget)

    def toolSelected(self, index):
        # Change the current widget in the stack based on the selected tool
        self.graph_stack.setCurrentIndex(index)

    def open(self):
        # Show the Tools window
        self.show()
