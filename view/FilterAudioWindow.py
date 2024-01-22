import os
import json
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton



class FilterAudioWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Audio Filter Viewer')
        self.setGeometry(300, 300, 500, 300)  # Adjusted size to accommodate new layout
        self.initialize_window_elements()

    def initialize_window_elements(self):
        main_layout = QHBoxLayout(self)

        # List of filter files
        self.filter_list_widget = QListWidget()
        self.filter_list_widget.itemSelectionChanged.connect(self.display_filter_properties)
        main_layout.addWidget(self.filter_list_widget)

        # Right side layout for displaying properties
        properties_layout = QVBoxLayout()
        main_layout.addLayout(properties_layout) 

        # Filter name label
        self.filter_name_label = QLabel("Filter Name")
        properties_layout.addWidget(self.filter_name_label)

        # Filter Type label
        self.filter_type_label = QLabel("Filter Type")
        properties_layout.addWidget(self.filter_type_label)

        # Frequency cutoff label
        self.filter_cutoff_frequency_label = QLabel("Cutoff Frequency")
        properties_layout.addWidget(self.filter_cutoff_frequency_label)

        # New column for displaying song filtered data
        self.song_filtered_data_list_widget = QListWidget()
        main_layout.addWidget(self.song_filtered_data_list_widget)

        self.apply_filter_to_song = QPushButton('Apply filter to song')
        main_layout.addWidget(self.apply_filter_to_song)

        self.setLayout(main_layout)
        self.update_filter_list()  # Initial population of the list

    def update_filter_list(self):
        filter_files = os.listdir('filters')  # Assuming 'filters' directory is in the current working directory
        self.filter_list_widget.clear()
        self.filter_list_widget.addItems(filter_files)

    def update_song_filtered_data(self, filtered_song_objects):
        self.song_filtered_data_list_widget.clear()
        song_keys = list(filtered_song_objects.keys())
        self.song_filtered_data_list_widget.addItems(song_keys)


    def display_filter_properties(self):
        selected_item = self.filter_list_widget.currentItem()
        if selected_item:
            file_name = selected_item.text()
            with open(f'filters/{file_name}', 'r') as file:
                properties = json.load(file)
            self.filter_name_label.setText(f"Filter Name: {properties.get('filter_name', '')}")
            self.filter_type_label.setText(f"Filter Type: {properties.get('filter_type', '')}")
            self.filter_cutoff_frequency_label.setText(f"Cutoff Frequency: {properties.get('cutoff_frequency', '')}")
            # Update more labels as needed
            self.process_audio_with_filter(properties)

    def process_audio_with_filter(self, filter_properties):
        # Process audio data using the filter properties
        # This is a placeholder for the actual audio processing logic
        # After processing, insert the audio data into a SongItem within the MainModel
        pass  # Replace with actual processing and insertion logic
