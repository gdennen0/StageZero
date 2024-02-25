import tools
from functools import partial
from controller.SongDataPreviewController import SongDataPreviewController


class LocalController:
    def __init__(self, local_view, main_controller):
        self.main_controller = main_controller
        self.local_view = local_view
        self.stack = main_controller.model.stack
        self.model = main_controller.model
        self.view = main_controller.view
        self.selected_filter_name = None
        self.selected_pool_name = None
        self.song_data_preview_controller = SongDataPreviewController()
        self.init_connections()
        self.display_song_filters()

    def init_connections(self):
        self.local_view.song_filtered_data_list_widget.currentItemChanged.connect(
            self.on_filter_data_selected
        )
        self.local_view.refresh_filtered_data_button.clicked.connect(
            self.display_song_filters
        )
        self.local_view.detect_onsets.clicked.connect(self.create_onsets)

        self.local_view.onset_pool_list_widget.currentItemChanged.connect(
            self.on_onset_pool_selected
        )

        self.local_view.preview_onset_pool_item.clicked.connect(
            self.preview_onset_pool_item
        )

    def on_filter_data_selected(self, current, previous):
        self.selected_filter_name = current.text() if current else ""
        print(f"Selected data: {self.selected_filter_name}")

    def on_onset_pool_selected(self, current):
        self.selected_pool_name = current.text()
        print(f"selected pool {self.selected_pool_name}")

    def preview_onset_pool_item(self):
        self.song_object = self.model.loaded_song
        if self.selected_pool_name is not None:
            key = str(self.selected_pool_name[0])
            print(f"key {key}")
            self.onsets = self.song_object.pool.onset.items[key].onset_data
        if self.selected_filter_name is not None:
            filtered_data_name = self.selected_filter_name
        if self.selected_pool_name and self.selected_filter_name is not None:
            self.song_data_preview_controller.open(self.song_object, filtered_data_name)
            self.song_data_preview_controller.add_events(self.onsets)

    def create_onsets(self):
        filtered_data_name = self.selected_filter_name
        self.song_object = self.model.loaded_song
        song_data = self.song_object.filter[filtered_data_name].filtered_data
        sample_rate = (
            self.model.loaded_song.original_sample_rate
        )  # TODO: make this functionality suck less

        onset_data = tools.detect_onsets(song_data=song_data, sample_rate=sample_rate)
        print(f"Onsets: {onset_data}")
        self.song_object.pool.onset.add(
            onset_data, self.model.loaded_song, parent_filter_name=filtered_data_name
        )

        self.local_view.update_onset_pool_list(self.song_object.pool.onset.items)

    def display_song_filters(self):
        if self.model.loaded_song:
            self.local_view.update_song_filtered_data(self.model.loaded_song.filter)

    def display_onset_pools(self):
        if self.model.loaded_song:
            self.local_view.update_onset_pool_list(
                self.model.loaded_song.pool.onset.items
            )

    def open(self):
        self.local_view.open()
        self.display_song_filters()
        self.display_onset_pools()
