"""
By default this is going to load up original_song_data 
"""

from .TimeUpdateThread import TimeUpdateThread
from view.window.SongDataPreviewWindow import SongDataPreviewWindow
import vlc
from librosa import resample
import numpy as np
import soundfile as sf
import tempfile
import os


class AudioPlaybackEngine:
    STOPPED, RUNNING, PAUSED = range(3)  # Define states for the audio playback

    def __init__(self):
        self.playback_clock_thread = TimeUpdateThread()
        self.audio_player = vlc.MediaPlayer()
        self.loaded_audio_data = None
        self.state = self.STOPPED  # Initial state is STOPPED

    def load_song(self, song_object):
        self.original_song_data = song_object.original_song_data
        self.original_sample_rate = song_object.original_sample_rate
        self.filter_objects = song_object.filter
        self.loaded_audio_data = song_object.original_song_data

        print(
            f"[AudioPlaybackEngine] loading song {song_object.name} with sample rate of {self.original_sample_rate} and {len(self.filter_objects)} filter objects"
        )
        self.reload_audio()

    def reload_audio(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            sf.write(tmpfile, self.loaded_audio_data, self.original_sample_rate)
        tmpfile_path = tmpfile.name
        self.audio_player.set_mrl(tmpfile_path)
        self.playback_clock_thread = TimeUpdateThread()
        self.stop()
        self.reset()

    def load_filtered_data(self, filter_name):
        self.loaded_audio_data = self.filter_objects[filter_name].filtered_data
        self.reload_audio()

    def load_original_song_data(self):
        self.loaded_audio_data = self.original_song_data
        self.reload_audio()

    def play(self):
        # Handle the play action
        if self.state == self.STOPPED:
            print(f"play button pressed")
            self.audio_player.play()
            self.playback_clock_thread.start_clock()
            self.state = self.RUNNING

        if self.state == self.PAUSED:
            print(f"resume function pressed")
            self.state = self.RUNNING
            self.audio_player.play()
            self.playback_clock_thread.resume_clock()

    def pause(self):
        # Handle the pause action
        if self.state == self.RUNNING:
            print(f"pause button pressed")
            self.state = self.PAUSED
            self.audio_player.pause()
            self.playback_clock_thread.pause_clock()

    def reset(self):
        # Handle the reset action
        if self.state == self.PAUSED:
            self.playback_clock_thread.reset_clock()
            self.audio_player.stop()
            print(f"reset button pressed")

        elif self.state == self.RUNNING:
            self.playback_clock_thread.reset_clock()
            self.audio_player.stop()
            self.audio_player.play()
            print(f"reset button pressed")

        elif self.state == self.STOPPED:
            self.playback_clock_thread.stop_clock()
            self.playback_clock_thread.reset_clock()
            self.audio_player.stop()

    def stop(self):
        # Handle the stop action
        self.state = self.STOPPED
        self.audio_player.stop()
        self.playback_clock_thread.stop_clock()
        self.playback_clock_thread.terminate()

    def init_connections(self):
        # Initialize connections for the play, pause, and reset buttons
        apc = self.view.main_window.audio_playback_command  # set apc reference
        # connect the buttons
        apc.play_button.clicked.connect(self.play)
        apc.pause_button.clicked.connect(self.pause)
        apc.reset_button.clicked.connect(self.reset)

    def update_time_label(self, frame_number):
        # Update the time label
        apc = self.view.main_window.audio_playback_command

        frame_label_string = f"Frame: {frame_number}/{self.model.loaded_song.frame_qty}"

        apc.time_label.setText(frame_label_string)
