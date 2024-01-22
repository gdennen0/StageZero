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


from controller.TimeUpdateThread import TimeUpdateThread
import vlc

class AudioPlaybackController:
    STOPPED, RUNNING, PAUSED = range(3)  # Define states for the audio playback

    def __init__(self, main_controller):
        self.model = main_controller.model  # Model reference
        self.view = main_controller.view  # View reference
        self.song_model = main_controller.model.song  # Song model reference
        self.player = vlc.MediaPlayer()  # VLC media player instance
        self.state = self.STOPPED  # Initial state is STOPPED
        self.init_connections()  # Initialize connections

        self.time_update_thread = TimeUpdateThread()  # Thread for updating time
        self.time_update_thread.time_updated.connect(self.update_time_label)  # Connect the time update signal

    def load_song(self):
        # Load a song into the player
        song_path = self.song_model.objects[self.model.loaded_song.name].path
        self.player.set_media(vlc.Media(song_path))

    def play(self):
        # Handle the play action
        if self.state == self.STOPPED:
            print(f"play button pressed")
            self.player.play()
            self.time_update_thread.start_clock()
            self.state = self.RUNNING

        if self.state == self.PAUSED:
            print(f"resume function pressed")
            self.state = self.RUNNING
            self.player.play()
            self.time_update_thread.resume_clock()

    def pause(self):
        # Handle the pause action
        if self.state == self.RUNNING:
            print(f"pause button pressed")
            self.state = self.PAUSED
            self.player.pause()
            self.time_update_thread.pause_clock()

    def reset(self):
        # Handle the reset action
        if self.state == self.PAUSED:
            self.time_update_thread.reset_clock()
            self.player.stop()
            print(f"reset button pressed")

        elif self.state == self.RUNNING:
            self.time_update_thread.reset_clock()
            self.player.stop()
            self.player.play()
            print(f"reset button pressed")

        elif self.state == self.STOPPED:
            self.time_update_thread.stop_clock()
            self.time_update_thread.reset_clock()
            self.player.stop()

    def stop(self):
        # Handle the stop action
        self.state = self.STOPPED
        self.time_update_thread.stop_clock()

    def get_playback_time(self):
        return self.player.get_time()  # Returns playback time in milliseconds

    def init_connections(self):
        # Initialize connections for the play, pause, and reset buttons
        apc = self.view.main_window.audio_playback_command      #set apc reference
        # connect the buttons
        apc.play_button.clicked.connect(self.play)
        apc.pause_button.clicked.connect(self.pause)
        apc.reset_button.clicked.connect(self.reset)

    def update_time_label(self, frame_number):
        # Update the time label
        apc = self.view.main_window.audio_playback_command
        
        frame_label_string = f"Frame: {frame_number}/{self.model.loaded_song.frame_qty}"

        apc.time_label.setText(frame_label_string)

