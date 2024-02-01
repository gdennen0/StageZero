from view.window.SongDataPreviewWindow import SongDataPreviewWindow
import vlc
from librosa import resample
import numpy as np
import soundfile as sf
import tempfile
import os
from .AudioPlaybackEngine import AudioPlaybackEngine


class SongDataPreviewController:
    def open(self, song_object, filter_data_name):
        self.song_data_preview_window = SongDataPreviewWindow()
        self.song_data = song_object.filter[filter_data_name].filtered_data
        self.original_sample_rate = song_object.original_sample_rate
        self.resampled_song_data = resample(
            self.song_data, orig_sr=self.original_sample_rate, target_sr=2000
        )
        self.song_axis = song_object.x_axis
        self.song_data_preview_window.open(self.resampled_song_data, self.song_axis)

        self.audio_playback_engine = AudioPlaybackEngine()
        self.audio_playback_engine.load_song(song_object)
        self.audio_playback_engine.load_filtered_data(filter_data_name)

        self.init_playhead()
        self.initialize_connections()

    def initialize_connections(self):
        self.song_data_preview_window.play_button.clicked.connect(self.play_audio)
        self.song_data_preview_window.pause_button.clicked.connect(self.pause_audio)
        self.song_data_preview_window.reset_button.clicked.connect(self.reset_audio)
        self.song_data_preview_window.window_closed.connect(
            self.stop_audio
        )  # Connect window close event to stop_audio

    def play_audio(self):
        self.audio_playback_engine.play()

    def pause_audio(self):
        self.audio_playback_engine.pause()

    def reset_audio(self):
        self.audio_playback_engine.reset()

    def stop_audio(self):
        self.audio_playback_engine.stop()  # Stop audio when window is closed

    def init_playhead(self):
        # Initialize the vertical line
        self.song_data_preview_window.init_playhead()
        self.audio_playback_engine.playback_clock_thread.time_updated.connect(
            self.update_playhead_position
        )

    def update_playhead_position(self, frame_number):
        # Update the position of the vertical line
        self.song_data_preview_window.playhead.setPos(float(frame_number))
