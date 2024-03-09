"""
Module: AudioPlaybackController

This module defines the AudioPlaybackController class, which is responsible for controlling the audio playback of the application. 
It uses the VLC media player for playing the audio and a separate thread for updating the time. 
The controller can handle different states of the audio playback, such as STOPPED, RUNNING, and PAUSED.

Arguments:
    main_controller (MainController): The main controller of the application. It provides references to the model and view of the application.

Returns:
    None

The AudioPlaybackController class has methods for loading a song into the player, handling the play, pause, and reset actions, and updating the time label. 
The play, pause, and reset methods change the state of the audio playback and the player accordingly. 
The load_song method loads a song into the player using the path of the song from the song model. 
The update_time_label method updates the time label in the view with the current time of the player.
"""

from .AudioPlaybackEngine import AudioPlaybackEngine


class AudioPlaybackController:
    def __init__(self, main_controller):
        self.model = main_controller.model
        self.main = main_controller
        self.apc = main_controller.view.main_window.stage_widget.audio_playback_command
        self.view = main_controller.view
        self.audio_playback_engine = AudioPlaybackEngine()
        self.init_connections()  # Initialize connections
        self.connect_playhead()

    def refresh(self):
        self.audio_playback_engine.load_song(self.model.loaded_song)
        self.audio_playback_engine.reload_audio()
        self.connect_playhead()

    def load_song(self, song_object):
        self.audio_playback_engine.load_song(song_object)
        self.connect_playhead()

    def play(self):
        if self.model.loaded_song:
            self.audio_playback_engine.play()

    def pause(self):
        if self.model.loaded_song:
            self.audio_playback_engine.pause()

    def reset(self):
        if self.model.loaded_song:
            self.audio_playback_engine.reset()

    def stop(self):
        if self.model.loaded_song:
            self.audio_playback_engine.stop()

    def init_connections(self):
        # connect the buttons
        self.apc.play_button.clicked.connect(self.play)
        self.apc.pause_button.clicked.connect(self.pause)
        self.apc.reset_button.clicked.connect(self.reset)

    def update_time_label(self, frame_number):
        # Update the time label
        frame_label_string = f"Frame: {frame_number}"
        self.apc.time_label.setText(frame_label_string)

    def connect_playhead(self):
        self.audio_playback_engine.playback_clock_thread.time_updated.connect(
            self.main.song_overview_controller.update_playhead_position
        )
        self.audio_playback_engine.playback_clock_thread.time_updated.connect(
            self.update_time_label
        )
        self.audio_playback_engine.playback_clock_thread.time_updated.connect(
            self.main.layer_controller.update_playhead_position
        )
        print(f"Connecting playhead in APC")
