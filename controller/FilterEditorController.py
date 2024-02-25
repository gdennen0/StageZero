import json
import os
from view.window.FilterEditorWindow import FilterEditorWindow
from PyQt5.QtGui import QIntValidator
import re


class FilterEditorController:
    def __init__(self):
        self.filter_editor_window = FilterEditorWindow()

    def open(self):
        self.filter_editor_window.show()
        self.connect_signals()

    def connect_signals(self):
        self.filter_editor_window.filter_list_widget.itemSelectionChanged.connect(
            self.load_filter_properties
        )
        self.filter_editor_window.save_button.clicked.connect(self.save_filter)
        self.filter_editor_window.delete_button.clicked.connect(self.delete_filter)

    def save_filter(self):
        if self.validate_inputs():
            params = {
                "filter_name": self.filter_editor_window.filter_name_input.text(),
                "filter_type": self.filter_editor_window.filter_type_combo_box.currentText(),
                "cutoff_frequency": self.filter_editor_window.cutoff_frequency_input.text(),
                # Add more parameters as needed
            }
            self.saveParametersToFile(params)
            self.filter_editor_window.update_filter_list()

    def validate_inputs(self):
        try:
            filter_name_input = self.filter_editor_window.filter_name_input.text()
            if not re.match("^[a-zA-Z0-9_-]+$", filter_name_input):
                raise ValueError("Invalid Character")

            cutoff_frequency_input = (
                self.filter_editor_window.cutoff_frequency_input.text()
            )
            if (
                not cutoff_frequency_input.isdigit()
                and not cutoff_frequency_input.replace(".", "", 1).isdigit()
            ):
                raise ValueError("Cutoff frequency must be a number.")

            cutoff_frequency = float(cutoff_frequency_input)
            if not 20 <= cutoff_frequency <= 20000:
                raise ValueError("The input frequency must be between 20Hz and 20kHz.")

            return True
        except ValueError as e:
            from PyQt5.QtWidgets import QMessageBox

            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Warning)
            error_dialog.setText("Invalid Input")
            error_dialog.setInformativeText(str(e))
            error_dialog.setWindowTitle("Error")
            error_dialog.exec_()
            return False

    def load_filter_properties(self):
        file_name = self.filter_editor_window.filter_list_widget.currentItem().text()
        with open(f"filters/{file_name}", "r") as file:
            properties = json.load(file)
        self.filter_editor_window.filter_name_input.setText(
            properties.get("filter_name", "")
        )
        self.filter_editor_window.filter_type_combo_box.setCurrentText(
            properties.get("filter_type", "Low-pass")
        )
        self.filter_editor_window.cutoff_frequency_input.setText(
            properties.get("cutoff_frequency", "")
        )
        # Load more properties as needed

    def delete_filter(self):
        selected_item = self.filter_editor_window.filter_list_widget.currentItem()
        if selected_item:
            os.remove(f"filters/{selected_item.text()}")
            self.filter_editor_window.update_filter_list()

    def saveParametersToFile(self, params):
        # Logic to save parameters to a file in the filter folder with the filter_name as the file name
        file_name = (
            params.get("filter_name", "default_filter") + ".json"
        )  # Default to 'default_filter.json' if no name is provided
        with open(f"filters/{file_name}", "w") as file:
            json.dump(params, file)
