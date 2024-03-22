"""
Module: EventEditorWidget

This module defines a widget for editing event objects in a PyQt5 application. The widget is a QDialog that contains two QLineEdits for editing the name and displaying all attributes of the event, a QColorDialog for choosing the color of the event, and a QPushButton for saving the changes.

Arguments:
    model_object: The event object to be edited. This object should have a 'name' attribute, a 'color' attribute, and potentially other attributes.
    parent: The parent widget of this widget. Defaults to None.

Returns:
    An instance of the EventEditorWidget class. This instance can be shown by calling its 'exec_' method.

The widget uses a QVBoxLayout for its layout. The first QLineEdit is added for editing the name of the event, followed by a second QLineEdit (read-only) that displays all attributes of the event, then the color button and the save button. When the color button is clicked, a QColorDialog is opened and the selected color is saved to the 'color' attribute of the event object. When the save button is clicked, the 'name' attribute of the event object is updated with the text from the first QLineEdit, and the dialog is closed.
"""

from PyQt5.QtWidgets import (
    QDialog,  # Dialog window
    QLineEdit,  # One-line text editor
    QColorDialog,  # Dialog widget for specifying colors
    QPushButton,  # Command button
    QVBoxLayout,  # Box layout with a vertical direction
    QLabel,  # Label widget
)
from PyQt5.QtCore import pyqtSignal
import pyqtgraph as pg
from PyQt5.QtWidgets import QHBoxLayout


class EventEditorWidget(QDialog):  # Widget for editing events
    changes_saved = pyqtSignal()

    def __init__(self, model_object, parent=None):
        super().__init__(parent)  # Call the constructor of the parent class
        self.model_object = model_object  # The event to be edited
        self.layout = QVBoxLayout(self)  # Set the layout to vertical box layout

        self.name_edit = QLineEdit(self)  # Line edit for editing the name
        self.name_edit.setText(str(self.model_object.event_name))  # Set the text of the line edit to the name of the event
        self.layout.addWidget(self.name_edit)  # Add the name edit to the layout
        self.attributes_layout = QHBoxLayout()
        self.name_display = QLineEdit(self)
        self.name_display.setReadOnly(True)
        self.name_display.setText(f"Name: {self.model_object.event_name}")
        self.attributes_layout.addWidget(self.name_display)
        self.color_display = QLineEdit(self)
        self.color_display.setReadOnly(True)
        self.color_display.setText(f"Color: {self.model_object.color}")
        self.attributes_layout.addWidget(self.color_display)

        if hasattr(self.model_object, "frame_number"):
            self.frame_number_display = QLineEdit(self)
            self.frame_number_display.setReadOnly(True)
            self.frame_number_display.setText(
                f"Frame Number: {self.model_object.frame_number}"
            )
            self.attributes_layout.addWidget(self.frame_number_display)

        # Add the attributes layout to the main layout, making it to the right of other items
        self.layout.addLayout(self.attributes_layout)

        # Create a button for opening the color dialog
        self.color_button = QPushButton("Choose color", self)  # Button for choosing the color
        self.color_button.clicked.connect(self.open_color_dialog)  # Connect the button click to the open_color_dialog method
        self.layout.addWidget(self.color_button)  # Add the color button to the layout

        # Create a save button
        self.save_button = QPushButton("Save", self)  # Button for saving the changes
        self.save_button.clicked.connect(self.save_changes)  # Connect the button click to the save_changes method
        self.layout.addWidget(self.save_button)  # Add the save button to the layout

    def open_color_dialog(self):  # Open the color dialog
        # Open the color dialog and get the selected color
        color = QColorDialog.getColor()
        # If a color was selected (the user didn't cancel the dialog), temporarily store the color
        if color.isValid():
            print(f"PDI color: {color}, {color.name()}")
            self.temp_color = color.name()  # Temporarily store the selected color

    def save_changes(self):  # Save the changes
        self.model_object.event_name = self.name_edit.text()
        if hasattr(self, "temp_color"):  # Check if a new color was selected
            try:
                self.model_object.set_color(self.temp_color)
            except ValueError as e:
                print(f"Error setting color: {e}")
        self.accept()
