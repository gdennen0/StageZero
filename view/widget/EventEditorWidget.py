"""
Module: EventEditorWidget

This module defines a widget for editing event objects in a PyQt5 application. The widget is a QDialog that contains a QLineEdit for editing the name of the event, a QColorDialog for choosing the color of the event, and a QPushButton for saving the changes.

Arguments:
    event_object: The event object to be edited. This object should have a 'name' attribute and a 'color' attribute.
    parent: The parent widget of this widget. Defaults to None.

Returns:
    An instance of the EventEditorWidget class. This instance can be shown by calling its 'exec_' method.

The widget uses a QVBoxLayout for its layout. The QLineEdit is added first, followed by the color button and the save button. When the color button is clicked, a QColorDialog is opened and the selected color is saved to the 'color' attribute of the event object. When the save button is clicked, the 'name' attribute of the event object is updated with the text from the QLineEdit, and the dialog is closed.
"""

from PyQt5.QtWidgets import (
    QDialog,  # Dialog window
    QLineEdit,  # One-line text editor
    QColorDialog,  # Dialog widget for specifying colors
    QPushButton,  # Command button
    QVBoxLayout,  # Box layout with a vertical direction
)


class EventEditorWidget(QDialog):  # Widget for editing events
    def __init__(self, event_object, parent=None):
        super().__init__(parent)  # Call the constructor of the parent class
        self.event_object = event_object  # The event to be edited
        self.layout = QVBoxLayout(self)  # Set the layout to vertical box layout

        self.attr1_edit = QLineEdit(self)  # Line edit for editing the first attribute
        self.attr1_edit.setText(
            str(self.event_object.name)
        )  # Set the text of the line edit to the name of the event
        self.layout.addWidget(self.attr1_edit)  # Add the line edit to the layout

        # Create a button for opening the color dialog
        self.color_button = QPushButton(
            "Choose color", self
        )  # Button for choosing the color
        self.color_button.clicked.connect(
            self.open_color_dialog
        )  # Connect the button click to the open_color_dialog method
        self.layout.addWidget(self.color_button)  # Add the color button to the layout

        # Create a save button
        self.save_button = QPushButton("Save", self)  # Button for saving the changes
        self.save_button.clicked.connect(
            self.save_changes
        )  # Connect the button click to the save_changes method
        self.layout.addWidget(self.save_button)  # Add the save button to the layout

    def open_color_dialog(self):  # Open the color dialog
        # Open the color dialog and get the selected color
        color = QColorDialog.getColor()

        # If a color was selected (the user didn't cancel the dialog), update the event_object's color
        if color.isValid():
            self.event_object.color = color.name()

    def save_changes(self):  # Save the changes
        # Update the event_object attributes with the new values from the QLineEdit widgets
        self.event_object.name = self.attr1_edit.text()

        # Close the dialog
        self.accept()
