
"""
Module: PlaybackModeController

This module defines the PlaybackModeController class, which is responsible for managing the playback modes of the application. 
It interacts with the main controller, view, and model of the application to perform various operations related to the playback modes.

The PlaybackModeController class has methods to handle the changes in the playback mode, get the current playback mode, and perform actions based on the selected playback mode.

Arguments:
    main_controller: A reference to the main controller of the application.

Returns:
    None. This module is used for controlling the playback modes and does not return any value.
"""



class PlaybackModeController:
    def __init__(self, main_controller):
        self.main_controller = main_controller  # Main controller reference
        self.view = main_controller.view  # View reference
        self.model = main_controller.model  # Model reference
        self.playback_modes = ["Play", "Edit", "Record"]  # Available playback modes
        self.connect_signals()  # Connect signals

    def connect_signals(self):
        # Connect the signal for when the user selects an item in playback_mode_selector 
        self.view.main_window.stage_widget.playback_mode.playback_mode_selector.currentIndexChanged.connect(
            self.on_playback_mode_changed
        )

    def get_current_mode(self):
        # Get the current playback mode
        playback_selector = self.view.main_window.stage_widget.playback_mode.playback_mode_selector      # Reference to the playback selector

        # call currentIndex method on the selector
        current_index = playback_selector.currentIndex()
        if current_index != -1: # if the selection index is not in an uninitialized state (-1)
            return self.playback_modes[current_index]
        else:
            return None

    def on_playback_mode_changed(self, index):
        # Handle the event when the playback mode changes
        if index == -1: # if the selection index is in an uninitialized state (-1)
            return
        selected_mode = self.playback_modes[index]  # get the string associated with the index

        if selected_mode == "Play":
            self.play_mode()
        elif selected_mode == "Edit":
            self.edit_mode()
        elif selected_mode == "Record":
            self.record_mode()

    def play_mode(self):
        print(f"Play Mode Selected")
        pass

    def edit_mode(self):
        print(f"Edit Mode Selected")
        pass

    def record_mode(self):
        print(f"Record Mode Selected")
        pass
