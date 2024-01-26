import os
import json
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QLineEdit,
    QListWidget,
)
from PyQt5.QtCore import pyqtSlot

from ..UI_COLORS import UIColors


class FilterEditorWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Audio Filter Presets")
        self.setGeometry(300, 300, 500, 300)  # Adjusted size to accommodate new layout
        self.initialize_window_elements()
        self.initialize_ui_colors()

    def initialize_ui_colors(self):
        # Define UI elements and their properties
        ui_elements = {
            self.filter_type_combo_box: {"list": True},
            self.filter_name_label: {"text": True},
            self.filter_name_input: {"inputbox": True},
            self.filter_type_label: {"text": True},
            self.filter_list_widget: {"list": True},
            self.save_button: {"button": True},
            self.delete_button: {"button": True},
            self.cutoff_frequency_input: {"inputbox": True},
            self.filter_cutoff_frequency_label: {"text": True},
        }

        # Apply colors to all UI elements
        UIColors.initialize_ui_colors(ui_elements)

        style_sheet = (
            f"background-color: {UIColors.BACKGROUND_COLOR};"
            f"QLabel {{ color: {UIColors.TEXT_COLOR}; }}"
            f"QPushButton {{ "
            f"background-color: {UIColors.BUTTON_COLOR}; "
            f"color: {UIColors.BUTTON_TEXT_COLOR}; "  # Set the text color for buttons
            f"}}"
            f"QListWidget {{"
            f"background-color: {UIColors.LIST_COLOR}; "
            f"color: {UIColors.LIST_TEXT_COLOR}; "  # Set the text color for buttons
            f"border-top-color: {UIColors.LIST_BORDER_COLOR}; "  # Set the top border color for QListWidget
            f"border-bottom-color: {UIColors.LIST_BORDER_COLOR}; "  # Set the bottom border color for QListWidget
            f"}}"
            f"QComboBox {{"
            f"background-color: {UIColors.LIST_COLOR}; "
            f"color: {UIColors.LIST_TEXT_COLOR}; "  # Set the text color for buttons
            f"border: 1px solid {UIColors.LIST_BORDER_COLOR}; "  # Set the border color for QComboBox
            f"}}"
            f"QLineEdit {{"
            f"background-color: {UIColors.INPUT_BOX_COLOR}; "
            f"color: {UIColors.INPUT_BOX_TEXT_COLOR}; "  # Set the text color for input box
            f"border: 1px solid {UIColors.INPUT_BOX_BORDER_COLOR}; "  # Set the border color for input box
            f"}}"
        )

        # Apply the concatenated style sheet
        self.setStyleSheet(style_sheet)

    def initialize_window_elements(self):
        main_layout = QHBoxLayout(self)

        # List of filter files
        self.filter_list_widget = QListWidget()
        main_layout.addWidget(self.filter_list_widget)

        # Right side layout for displaying properties
        properties_layout = QVBoxLayout()
        main_layout.addLayout(properties_layout)

        # Filter name label and input
        self.filter_name_label = QLabel("Filter Name")
        self.filter_name_input = QLineEdit()
        self.filter_name_input.setPlaceholderText("Enter filter name")
        properties_layout.addWidget(self.filter_name_label)
        properties_layout.addWidget(self.filter_name_input)

        # Filter Type label and dropdown
        self.filter_type_label = QLabel("Filter Type")
        self.filter_type_combo_box = QComboBox()
        self.filter_type_combo_box.addItems(
            [
                "Low-pass",
                "High-pass",
                "Band-pass",
                "Band-stop",
                "Butterworth",
                "Chebyshev I",
                "Chebyshev II",
                "Elliptic",
                "Bessel",
            ]
        )
        properties_layout.addWidget(self.filter_type_label)
        properties_layout.addWidget(self.filter_type_combo_box)

        # Frequency cutoff label and input
        self.filter_cutoff_frequency_label = QLabel("Cutoff Frequency (Hz)")
        self.cutoff_frequency_input = QLineEdit()
        properties_layout.addWidget(self.filter_cutoff_frequency_label)
        properties_layout.addWidget(self.cutoff_frequency_input)
        # Add more inputs as needed

        # Save and Delete Buttons
        self.save_button = QPushButton("Save Preset")
        self.delete_button = QPushButton("Delete Preset")
        properties_layout.addWidget(self.save_button)
        properties_layout.addWidget(self.delete_button)

        self.setLayout(main_layout)
        self.update_filter_list()  # Initial population of the list

    def update_filter_list(self):
        filter_files = os.listdir(
            "filters"
        )  # Assuming 'filters' directory is in the current working directory
        self.filter_list_widget.clear()
        self.filter_list_widget.addItems(filter_files)
