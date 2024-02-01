"""
Module: ToolsWindow

This module defines the ToolsWindow class, which is a QWidget. The ToolsWindow is a part of the user interface that provides various tools for the user to interact with. 
It includes a dropdown menu for tool selection and a stacked widget to hold different tool widgets. 
The tool widgets are initialized and added to the stack in the initializeTools method. 
When a tool is selected from the dropdown menu, the toolSelected method changes the current widget in the stack based on the selected tool.

Arguments: None

Returns: None

This module follows the Zen of Python by being simple and readable, with each method having a single responsibility. 
The use of QWidget as a base class allows for easy integration with other PyQt5 components and the use of QVBoxLayout for layout management 
ensures that the layout is flexible and can adapt to changes in the window size.
"""

from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QVBoxLayout,  # Box layout with a vertical direction
    QComboBox,  # Drop down selection box
    QStackedWidget,
)

from ..widget.BPMToolWidget import BpmToolWidget
from ..widget.OnsetDetectionWidget import OnsetDetectionWidget
from ..widget.KicksToolWidget import KicksToolWidget


class ToolsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tools")
        self.initializeUI()

    def initializeUI(self):
        # Main layout for the Tools window
        self.layout = QVBoxLayout(self)

        # Dropdown menu to select a tool
        self.tool_selector = QComboBox(self)
        self.tool_selector.addItems(
            ["BPM Counter", "Onset Detection", "Kick Detection"]
        )  # Add tool names here
        self.tool_selector.currentIndexChanged.connect(self.toolSelected)
        self.layout.addWidget(self.tool_selector)

        # Stacked widget to hold different tool widgets
        self.tools_stack = QStackedWidget(self)
        self.layout.addWidget(self.tools_stack)

        # Initialize tool widgets and add them to the stack
        self.initializeTools()

    def initializeTools(self):
        # Tool widgets are initialized and added to the stack here
        # Example tool widgets
        self.bpm = BpmToolWidget()
        self.onset = OnsetDetectionWidget()
        self.kick = KicksToolWidget()

        # Add tool widgets to the stack
        self.tools_stack.addWidget(self.bpm)
        self.tools_stack.addWidget(self.onset)
        self.tools_stack.addWidget(self.kick)

    def toolSelected(self, index):
        # Change the current widget in the stack based on the selected tool
        self.tools_stack.setCurrentIndex(index)

    def open(self):
        # Show the Tools window
        self.show()
