"""
Module: DialogWindow

This module provides a set of utility functions for creating and managing dialog windows in a PyQt5 application. 
It includes functions for opening files, saving files, inputting text, and displaying error messages. 
Each function creates a specific type of dialog window, sets the necessary options, and returns the user's input or selection.

Arguments: 
    - title: A string representing the title of the dialog window.
    - dir: A string representing the initial directory displayed in the file dialog.
    - filter: A string representing the file filter for the file dialog.
    - message: A string representing the message to be displayed in the error dialog.

Returns: 
    - open_file: Returns a string representing the path of the file selected by the user.
    - save_file: Returns a string representing the path of the file to be saved as selected by the user.
    - input_text: Returns a string representing the text input by the user.
    - error: No return value. Displays an error message to the user.
"""

from PyQt5.QtWidgets import (
    QFileDialog,  # Dialog for users to select files or directories
    QInputDialog,  # Dialog for user input
    QMessageBox,  # Modal dialog for informing the user or for asking the user a question and receiving an answer
)


class DialogWindow:
    # Prompt user to select a file to open
    def open_file(title, dir=None, filter=None):
        options = QFileDialog.Options()  # Define the options for the file dialog
        file_path, _ = QFileDialog.getOpenFileName(  # Get the open file name
            None,
            title,
            dir,
            filter,
            options=options,
        )
        return file_path  # Return the file path

    # Prompt user to select file save name/path
    def save_file(title, dir=None, filter=None):
        options = QFileDialog.Options()  # Define the options for the file dialog
        file_path, _ = QFileDialog.getSaveFileName(  # Get the save file name
            None,
            title,
            dir,
            filter,
            options=options,
        )
        return file_path  # Return the file path

    # Prompt user to input text
    def input_text(title, label):
        name, ok = QInputDialog.getText(
            None, title, label
        )  # Get the text input from the user
        if ok:  # If the input is valid
            return name  # Return the name

    def error(message):
        msg = QMessageBox()  # Create a message box
        msg.setIcon(QMessageBox.Critical)  # Set the icon to critical
        msg.setText("Error")  # Set the text to "Error"
        msg.setInformativeText(message)  # Set the informative text to the message
        msg.setWindowTitle("Error")  # Set the window title to "Error"
        msg.exec_()  # Execute the message box
