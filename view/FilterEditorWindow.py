import os
import json
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QListWidget
from PyQt5.QtCore import pyqtSlot



class FilterEditorWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Audio Filter Presets')
        self.setGeometry(300, 300, 500, 300)  # Adjusted size to accommodate new layout
        self.initialize_window_elements()

    def initialize_window_elements(self):
        main_layout = QHBoxLayout(self)

        # List of filter files
        self.filter_list_widget = QListWidget()
        main_layout.addWidget(self.filter_list_widget)

        # Right side layout for displaying properties
        properties_layout = QVBoxLayout()
        main_layout.addLayout(properties_layout)

        # Filter name label and input
        filter_name_label = QLabel("Filter Name")
        self.filter_name_input = QLineEdit()
        self.filter_name_input.setPlaceholderText('Enter filter name')
        properties_layout.addWidget(filter_name_label)
        properties_layout.addWidget(self.filter_name_input)

        # Filter Type label and dropdown
        filter_type_label = QLabel("Filter Type")
        self.filter_type_combo_box = QComboBox()
        self.filter_type_combo_box.addItems(["Low-pass", "High-pass", "Band-pass", "Band-stop", "Butterworth", "Chebyshev I", "Chebyshev II", "Elliptic", "Bessel"])
        properties_layout.addWidget(filter_type_label)
        properties_layout.addWidget(self.filter_type_combo_box)

        # Frequency cutoff label and input
        filter_cutoff_frequency_label = QLabel("Cutoff Frequency (Hz)")
        self.cutoff_frequency_input = QLineEdit()
        properties_layout.addWidget(filter_cutoff_frequency_label)
        properties_layout.addWidget(self.cutoff_frequency_input)
        # Add more inputs as needed

        # Save and Delete Buttons
        self.save_button = QPushButton('Save Preset')
        self.delete_button = QPushButton('Delete Preset')
        properties_layout.addWidget(self.save_button)
        properties_layout.addWidget(self.delete_button)

        self.setLayout(main_layout)
        self.update_filter_list()  # Initial population of the list

    def update_filter_list(self):
        filter_files = os.listdir('filters')  # Assuming 'filters' directory is in the current working directory
        self.filter_list_widget.clear()
        self.filter_list_widget.addItems(filter_files)
