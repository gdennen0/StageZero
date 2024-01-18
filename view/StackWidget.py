"""
Module: StackWidget

This module defines the StackWidget class, a QWidget subclass that provides a scrollable stack of LayerWidgets. 
Each LayerWidget represents a layer in a graphical interface, and the StackWidget allows for easy navigation 
and manipulation of these layers.

Arguments: None

Returns: An instance of the StackWidget class, which is a QWidget with additional functionality for handling 
a stack of LayerWidgets.

The StackWidget is initialized with a QVBoxLayout, and a QLabel is added at the top to display the text "Layers". 
A QScrollArea is then created and added to the layout, which allows the stack of layers to be scrollable. 
A QWidget is created to hold the content of the stack, and a QVBoxLayout is set for this widget. 
The layout's margins and spacing are set to zero, and its alignment is set to the top. 
The widget for the stack content is then set as the widget for the scroll area. 
Finally, a LayerWidget is created and added to the stack content layout, and the layouts are updated.
"""

from PyQt5.QtCore import (
    Qt,  # For Qt related operations
)
from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QLabel,  # For displaying text or images
    QVBoxLayout,  # Box layout with a vertical direction
    QScrollArea,  # Scrollable display area
    QSizePolicy,  # Layout attribute describing horizontal and vertical resizing policy
)

from .LayerWidget import LayerWidget

class StackWidget(QWidget):  # Widget for displaying the stack of layers
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()  # Initialize the widget

    def initialize(self):  # Initialize the widget
        self.layout = QVBoxLayout(self)  # Set the layout to vertical box layout
        self.layout.setContentsMargins(0, 0, 0, 0)  # Set the margins to zero
        self.layout.setSpacing(0)  # Set spacing to zero

        # Add label at the top
        self.label = QLabel("Layers")  # Label for the layers
        self.layout.addWidget(self.label)  # Add the label to the layout

        # Creating a scroll area
        self.scroll_area = QScrollArea(self)  # Scroll area for the layers
        # self.scroll_area.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.scroll_area.setWidgetResizable(True)  # Make the widget resizable
        self.layout.addWidget(self.scroll_area)  # Add the scroll area to the layout

        self.stack_content = QWidget()  # Widget for the stack content
        self.stack_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set the size policy for the stack content
        self.stack_content_layout = QVBoxLayout(self.stack_content)  # Set the layout for the stack content to vertical box layout
        self.stack_content_layout.setContentsMargins(0, 0, 0, 0)  # Set the margins for the stack content layout to zero
        self.stack_content_layout.setSpacing(0)  # Set the spacing for the stack content layout to zero
        self.stack_content_layout.setAlignment(Qt.AlignTop)  # Align the stack content layout to the top

        self.scroll_area.setWidget(self.stack_content)  # Set the widget for the scroll area to the stack content

        self.layer_widget = LayerWidget()  # Widget for the layer
        self.stack_content_layout.addWidget(self.layer_widget, alignment=Qt.AlignTop)  # Add the layer widget to the stack content layout

        self.stack_content_layout.update()  # Update the stack content layout
        self.scroll_area.update()  # Update the scroll area
