import json

from analyze import filter
from view.window.FilterAudioWindow import FilterAudioWindow
from .SongDataPreviewController import SongDataPreviewController
class FilterAudioController:
    def __init__(self, main_controller):
        self.model = main_controller.model
        self.main = main_controller
        self.view = main_controller.view
        self.filter_audio_window = FilterAudioWindow()
        self.song_data_preview_controller = SongDataPreviewController()
        self.filter_objects = None

    def connect_signals(self):
        self.filter_audio_window.filter_list_widget.itemSelectionChanged.connect(self.display_filter_properties)
        self.filter_audio_window.apply_filter_to_song.clicked.connect(self.apply_filter_to_audio)
        self.filter_audio_window.preview_filtered_data.clicked.connect(self.preview_filtered_data)

    def display_filter_properties(self):
        selected_item = self.filter_audio_window.filter_list_widget.currentItem()
        if selected_item:
            file_name = selected_item.text()
            with open(f"filters/{file_name}", "r") as file:
                properties = json.load(file)
            self.filter_audio_window.filter_name_label.setText(f"Filter Name: {properties.get('filter_name', '')}")
            self.filter_audio_window.filter_type_label.setText(f"Filter Type: {properties.get('filter_type', '')}")
            self.filter_audio_window.filter_cutoff_frequency_label.setText(f"Cutoff Frequency: {properties.get('cutoff_frequency', '')}") # Update more labels as needed
            self.filter_audio_window.process_audio_with_filter(properties)

    def apply_filter_to_audio(self):
        selected_item = self.filter_audio_window.filter_list_widget.currentItem()
        if selected_item:
            file_name = selected_item.text()
            filter_name = file_name.rsplit(".", 1)[0]
            with open(f"filters/{file_name}", "r") as file:
                properties = json.load(file)
            filter_type = properties.get("filter_type", "")
            cutoff_frequency = properties.get("cutoff_frequency", "")
            filtered_data = filter.apply_filter(filter_type,cutoff_frequency, self.model.loaded_song.song_data, self.model.loaded_song.sample_rate) # function to add filtered data to song
            self.model.add_filtered_data(filter_name, filtered_data)
            self.filter_audio_window.update_song_filtered_data(self.model.loaded_song.filter) # function to refresh the list of filters on song

    def display_song_filters(self):
        self.filter_audio_window.update_song_filtered_data(
            self.model.loaded_song.filter
        )

    def preview_filtered_data(self):
        print(f"previewing filtered data")
        selected_item = (
            self.filter_audio_window.song_filtered_data_list_widget.currentItem()
        )
        if selected_item:
            filtered_data_name = selected_item.text()
            song_object = self.model.loaded_song
            self.song_data_preview_controller.open(song_object, filtered_data_name)

    def open(self):
        self.filter_audio_window.show()
        self.connect_signals()
