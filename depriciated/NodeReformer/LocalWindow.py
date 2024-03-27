from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QLabel,  # For displaying text or images
    QVBoxLayout,  # Box layout with a vertical direction
    QHBoxLayout,
    QPushButton,  # Command button
    QListWidget,
)
from PyQt5.QtWidgets import QComboBox
from view.widget.OnsetFilterWidget import OnsetFilterWidget


class LocalWindow(QWidget):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()

    def initialize(self):
        self.main_layout = QVBoxLayout()

        # self.plot =
        # Input Data Widget
        self.input_data_widget = QWidget()
        self.input_data_layout = QVBoxLayout(self)
        self.input_data_widget.setLayout(self.input_data_layout)

        self.song_filtered_label = QLabel("Loaded Song's filtered data")
        self.song_filtered_data_list_widget = QListWidget()

        self.refresh_filtered_data_button = QPushButton("Refresh Song Data", self)
        self.detect_onsets = QPushButton("Detect Onsets", self)

        self.input_data_layout.addWidget(self.song_filtered_label)
        self.input_data_layout.addWidget(self.refresh_filtered_data_button)
        self.input_data_layout.addWidget(self.song_filtered_data_list_widget)
        self.input_data_layout.addWidget(self.detect_onsets)
        # add to main layout

        # Onset Pool Widget
        self.onset_pool_widget = QWidget()
        self.onset_pool_layout = QVBoxLayout(self)
        self.onset_pool_widget.setLayout(self.onset_pool_layout)

        self.onset_pool_label = QLabel("Onset Pool")
        self.onset_pool_list_widget = QListWidget()

        self.preview_onset_pool_item = QPushButton("Preview onset pool item", self)

        self.onset_pool_layout.addWidget(self.onset_pool_label)
        self.onset_pool_layout.addWidget(self.onset_pool_list_widget)
        self.onset_pool_layout.addWidget(self.preview_onset_pool_item)

        # add widgets to main layout
        self.main_layout.addWidget(self.input_data_widget)
        self.main_layout.addWidget(self.onset_pool_widget)

        # Set the main layout to the LocalWindow
        self.setLayout(self.main_layout)

    def open(self):
        self.show()

    def update_song_filtered_data(self, filtered_song_objects):
        self.song_filtered_data_list_widget.clear()
        song_keys = list(filtered_song_objects.keys())
        self.song_filtered_data_list_widget.addItems(song_keys)

    def update_onset_pool_list(self, onset_pool_list):
        self.onset_pool_list_widget.clear()
        onset_items = [
            f"{key}: {item.name}"
            for key, item in onset_pool_list.items()
            if item is not None
        ]
        self.onset_pool_list_widget.addItems(onset_items)
