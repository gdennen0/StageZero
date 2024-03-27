import librosa
import constants
import numpy as np
from ..pool.PoolModel import PoolModel
from view.WaveformPlotItem import WaveformPlotItem
from view.LineItem import LineItem

class SongItem:
    # Song Item Attributes
    def __init__(self):
        self.name = None
        self.path = None
        self.song_data = None
        self.sample_rate = None
        self.length_ms = None
        self.frame_qty = None
        self.x_axis = None
        self.waveform_plot_item = None
        self.pool = PoolModel()
        self.filter = {}
        self.lines = []

    def set_name(self, name):
        self.name = name

    def set_path(self, path):
        self.path = path

    def load_song_data(self, path):
        self.song_data, self.sample_rate = librosa.load(path) 

    def set_length_ms(self, song_data, sample_rate):
        duration_sec = librosa.get_duration(y=song_data, sr=sample_rate)  # Get the duration of the song in seconds
        adjusted_duration_sec = duration_sec * 1000
        self.length_ms = adjusted_duration_sec

    def set_frame_qty(self, length_ms):
        self.frame_qty = round(length_ms / 1000 * constants.PROJECT_FPS)  # Calculate the quantity of frames

    def generate_x_axis(self, song_data, sample_rate):
        # Generate x axis items for the song
        samples_per_frame = sample_rate / constants.PROJECT_FPS
        self.x_axis = np.arange(len(song_data)) / samples_per_frame
    
    def build_data(self, song_name, path):
        self.set_name(song_name)
        self.set_path(path)
        self.load_song_data(path)  # Load the song data and sample rate
        self.set_length_ms(self.song_data, self.sample_rate)  # Calculate the length of the song in milliseconds
        self.set_frame_qty(self.length_ms)  # Calculate the quantity of frames
        self.generate_x_axis(self.song_data, self.sample_rate)
        self.generate_waveform_plot_item(self.x_axis, self.song_data)

    def to_dict(self):
        return {
            "name": self.name,
            "path": self.path,
            "length_ms": self.length_ms,
            "frame_qty": self.frame_qty,
            # Exclude waveform_plot_item from serialization
        }

    def deserialize(self, data):
        self.name = data.get("name")
        self.path = data.get("path")
        self.length_ms = data.get("length_ms", 0)
        self.frame_qty = data.get("frame_qty", 0)
        print(f"name: {self.name}, path: {self.path}, ")
        # Reload song data based on path
        self.load_song_data(self.path)
        self.generate_x_axis(self.song_data, self.sample_rate)
        self.generate_waveform_plot_item(self.x_axis, self.song_data)
    
    def generate_waveform_plot_item(self, x_axis, song_data):
        print(f"[SongItem][generate_waveform_plot_item] | Generating waveform plot item")
        self.waveform_plot_item = WaveformPlotItem()
        self.waveform_plot_item.set_waveform_data(x_axis, song_data)

    def get_original_song_data(self, path):
        song_data, sample_rate = librosa.load(path)
        return song_data, sample_rate

    def add_line(self, frame_number, color=None, type=None):
        line = LineItem()
        line.set_frame_number(frame_number)
        if color:
            line.set_color(color)
        if type:
            line.set_type(type)

        self.lines.append(line)
        pass

    def add_filtered_data(self, filter_name, filtered_data):
        self.filter[filter_name] = FilterItem(filtered_data)
        print(f"Adding FilterItem {filter_name} ")

    @property
    def filtered_song_data(self, filter_type):
        if filter_type in self.filters:
            return self.filters[filter_type].data


class FilterItem:
    def __init__(self, filtered_data):
        self.filtered_data = filtered_data
