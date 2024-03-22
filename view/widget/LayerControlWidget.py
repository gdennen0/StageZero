"""
Module: LayerControlWidget
This module defines a widget for controlling layers in a PyQt5 application. It is a subclass of QWidget, the base class for all user interface objects in PyQt5.

Arguments: None
This module does not take any arguments. It initializes itself with a horizontal box layout, a label, and two buttons for adding and removing layers.

Returns: None
This module does not return any values. It is used for its side effects, namely creating a user interface for controlling layers.

The LayerControlWidget class defined in this module has an initialize method that sets up the user interface. This method creates a QHBoxLayout (a layout with a horizontal direction), sets its margins, and adds a QLabel (a widget for displaying text or images) and two QPushButtons (command buttons) to it. The QLabel displays the text "Layer Controls", and the QPushButtons are labeled "Add" and "Remove" and are used for adding and removing layers, respectively.
"""

from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QLabel,  # For displaying text or images
    QHBoxLayout,  # Box layout with a horizontal direction
    QPushButton,  # Command button
)


class LayerControlWidget(QWidget):  # Widget for controlling layers
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()  # Initialize the widget

    def initialize(self):  # Initialize the widget
        self.layout = QHBoxLayout(self)  # Set the layout to horizontal box layout
        self.label = QLabel(f"Layer Controls")  # Label for the layer controls
        self.layout.addWidget(self.label)  # Add the label to the layout
        self.btnRemove = QPushButton("Remove", self)  # Button for removing a layer
        self.btnAdd = QPushButton("Add", self)  # Button for adding a layer
        self.layout.addWidget(self.btnAdd)  # Add the add button to the layout
        self.layout.addWidget(self.btnRemove)  # Add the remove button to the layout
