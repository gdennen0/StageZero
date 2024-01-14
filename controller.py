import math
import numpy as np
import time
import vlc
from threading import Condition

from PyQt5.QtCore import (
    pyqtSignal,
    Qt,
    QThread,
)

import constants
from view import DialogWindow, EventEditorWidget

# =========================================================================================================================================
# Controller Classes
# =========================================================================================================================================


class MainController:
    def __init__(self, model, view):
        self.model = model  # Assigning the model
        self.view = view  # Assigning the view

        # Centralize All of the controllers
        self.project_controller = ProjectController(self)  # Creating an instance of ProjectController
        self.song_controller = SongController(self)  # Creating an instance of SongController
        self.stack_controller = StackController(self)  # Creating an instance of StackController
        self.layer_controller = LayerController(self)  # Creating an instance of LayerController
        self.song_overview_controller = SongOverviewController(self)  # Creating an instance of SongOverviewController
        self.song_select_controller = SongSelectController(self)  # Creating an instance of SongSelectController
        self.event_controller = EventController(self)  # Creating an instance of EventController
        self.audio_playback_controller = AudioPlaybackController(self)  # Creating an instance of AudioPlaybackController
        self.playback_mode_controller = PlaybackModeController(self)  # Creating an instance of PlaybackModeController

    def initialize_app(self):
        # Open the main window
        self.view.launch_window.open()  # Opening the launch window
        # Connect the launch windows new project button click signal to connect to project controller new project method


class ProjectController:
    # Implement functionality to save, load and create projects
    def __init__(self, main_controller):
        self.model = main_controller.model  # Assign model reference
        self.view = main_controller.view  # Assign view reference
        self.connect_signals()

    def connect_signals(self):
        self.view.launch_window.new_project_button.clicked.connect(self.new_project)  # Connecting the new_project_button click signal to the new_project method
        self.view.launch_window.load_project_button.clicked.connect(self.load_project)  # Connecting the load_project_button click signal to the load_project method

    def new_project(self):
        print(f"Begin Initializing New Project")
        project_name = DialogWindow.input_text("Input Text", "Project Name")  # Getting the project name from the user
        self.model.project_name = project_name  # Setting the project name in the model

        self.view.main_window.open(project_name)  # Opening the main window with the project name
        self.view.launch_window.close()  # Closing the launch window

    def load_project(self):
        # functions to load the project file
        print(f"Begin Loading Project")

class SongSelectController:
    def __init__(self, main_controller):
        self.main_controller = main_controller  # Assigning main controller reference
        self.view = main_controller.view  # Assigning view reference
        self.model = main_controller.model  # Assigning model reference
        self.generate_dropdown_items()  # Generating the dropdown items
        self.connect_signals()  # Connecting the UI signals to slots in this controller

    def connect_signals(self):
        self.view.main_window.song_select_menu.song_selector.currentIndexChanged.connect(
            self.on_song_selected
        )  # Connecting the song_selector currentIndexChanged signal to the on_song_selected method
        self.view.main_window.song_select_menu.add_new_song.clicked.connect(
            self.main_controller.song_controller.add_song
        )  # Connecting the add_new_song clicked signal to the add_song method in the song controller

    def generate_dropdown_items(self):
        # Add the selected song to the dropdown menu
        if self.model.loaded_song != None:  # Checking if a song is loaded, if its not loaded dont proceed
            self.view.main_window.song_select_menu.song_selector.addItem(
                self.model.song.loaded_song
            )  # Adding the loaded song to the song_selector dropdown menu so it is at the top of the menu
        # add the remaining songs to the dropdown menu
        for song_name in self.model.song.objects:  # Iterating over the model song objects
            if song_name != self.model.loaded_song.name:  # Checking if the song is not the loaded song because we already loaded that
                self.view.main_window.song_select_menu.song_selector.addItem(song_name)  # Adding the song to the song_selector dropdown menu

    def on_song_selected(self, index):
        # Handle what happens when a song is selected
        if index == -1:  # Checking if the index is -1 (if the song_selector does not have any items in it)
            return  # If the index is -1, return
        selected_song = self.view.main_window.song_select_menu.song_selector.itemText(
            index
        )  # Getting the selected songs name from the song_selector dropdown menu given the song_selector index
        print(f"Selected song: {selected_song} index: {index}")  # Printing the selected song and index
        self.main_controller.song_controller.load_song(selected_song)  # Loading the selected song with the song_controller

    def update_dropdown(self):
        # Clear the dropdown
        self.view.main_window.song_select_menu.song_selector.clear()
        # Generate and place the dropdown Items
        self.generate_dropdown_items()

class PlaybackModeController:
    def __init__(self, main_controller):
        self.main_controller = main_controller  # Main controller reference
        self.view = main_controller.view  # View reference
        self.model = main_controller.model  # Model reference
        self.playback_modes = ["Play", "Edit", "Record"]  # Available playback modes
        self.connect_signals()  # Connect signals

    def connect_signals(self):
        # Connect the signal for when the user selects an item in playback_mode_selector 
        self.view.main_window.playback_mode.playback_mode_selector.currentIndexChanged.connect(
            self.on_playback_mode_changed
        )

    def get_current_mode(self):
        # Get the current playback mode
        playback_selector = self.view.main_window.playback_mode.playback_mode_selector      # Reference to the playback selector

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

class SongOverviewController:
    def __init__(self, main_controller):
        self.model = main_controller.model  # Model reference
        self.song_overview_widget = main_controller.view.main_window.song_overview  # Song overview widget reference
        self.main_controller = main_controller  # Main controller reference
        self.view = main_controller.view  # View reference

    def generate_ticks(self):
        # Generate ticks for the song
        song = self.model.loaded_song.name
        length_ms = self.model.song.objects[song].length_ms
        frame_qty = self.calculate_frame_quantity(length_ms, constants.PROJECT_FPS)
        song_data = self.model.song.objects[song].song_data
        sample_rate = self.model.song.objects[song].sample_rate
        samples_per_frame = sample_rate / constants.PROJECT_FPS

        frame_numbers = np.arange(len(song_data)) / samples_per_frame

        return frame_numbers

    def init_v_line(self):
        # Initialize the vertical line
        song_overview_widget = self.view.main_window.song_overview
        song_overview_widget.init_v_line()
        self.main_controller.audio_playback_controller.time_update_thread.time_updated.connect(
            self.update_v_line_position
        )

    def update_v_line_position(self, frame_number):
        # Update the position of the vertical line
        # print(f"update_v_line_pos")
        self.view.main_window.song_overview.v_line.setPos(float(frame_number))

    def calculate_frame_quantity(self, length_ms, fps):
        # Calculate the frame quantity and round up to the nearest whole frame
        frame_qty = math.ceil((length_ms / 1000) * fps)
        print(f"# of frames for {(length_ms / 1000)}seconds @ {fps}fps is {frame_qty}")
        return frame_qty

    def create_frames_array(self, frame_qty):  # create tick array
        print(f"Creating {frame_qty} frame array")
        return np.arange(frame_qty)

    def update_plot(self):
        # Update the plot
        ticks = self.generate_ticks()
        song_data = self.model.song.objects[self.model.song.loaded_song].song_data
        self.song_overview_widget.update_plot(ticks, song_data)
        self.init_v_line()

class SongController:
    def __init__(self, main_controller):
        self.main_controller = main_controller  # Main controller reference
        self.model = main_controller.model  # Model reference
        self.view = main_controller.view  # View reference

    def print(self, function_type, string):
        print(f"[CONTROLLER][{function_type}] | {string}")

    def add_song(self):
        # Add a song
        file_path = DialogWindow.open_file(
            "Select Song", "", "Audio Files (*.mp3 *.wav);;All Files (*)"
        )
        song_name = DialogWindow.input_text("Enter Song Name", "Song Name")
        song_object = self.model.song.build_song_object(file_path, song_name)
        self.model.song.add_song_object_to_model(
            song_object
        )
        self.main_controller.stack_controller.create_stack(song_name)
        if self.model.song.loaded_song == None:
            self.load_song(song_name)
        else:
            self.main_controller.song_select_controller.update_dropdown()

    def load_song(self, song_name):
        # Load a song
        self.print("load_song", f"current selected song: {song_name}")
        # Change loaded_song to song_name
        self.model.song.loaded_song = song_name
        # Change loaded_stack to song_name
        self.model.stack.loaded_stack = song_name
        # load the frame qty for the stack
        self.main_controller.stack_controller.set_stack_frame_qty(song_name)
        self.print("load_song", f"Updating song Plot")
        # Update the Song Overview Plot
        self.main_controller.song_overview_controller.update_plot()
        # Reload all of the layer plots
        # self.main_controller.layer_controller.init_plot(song_name)
        self.main_controller.layer_controller.reload_layer_plot()
        # Load the audio into the playback controller
        self.main_controller.audio_playback_controller.load_song()
        # reset the audio playback
        self.main_controller.audio_playback_controller.stop()
        self.main_controller.audio_playback_controller.reset()


class StackController:
    def __init__(self, main_controller):
        # Initialize with references to main controller, model, and view
        self.main_controller = main_controller
        self.model = main_controller.model
        self.view = main_controller.view

    def create_stack(self, stack_name):
        # Create a new stack with the given name
        print(f"Creating stack {stack_name}")
        self.model.stack.create_stack(stack_name)
        # Set the number of frames for the stack
        self.set_stack_frame_qty(stack_name)
        # Initialize the plot for the new stack
        # self.main_controller.layer_controller.init_plot(stack_name)

    def change_stack(self, stack_name):
        # Change the selected stack to the one with the given name
        self.model.stack.selected_stack = stack_name
        self.main_controller.layer_controller.init_plot(stack_name)

    def get_loaded_stack(self):
        # Return the currently loaded stack
        return self.model.stack.loaded_stack

    def set_stack_frame_qty(self, stack_name):
        # Set the number of frames for the stack with the given name
        frame_qty = self.model.song.objects[stack_name].frame_qty
        self.model.stack.objects[stack_name].set_frame_qty(frame_qty)


class LayerController:
    # This class manages the layers in the application.
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.stack = main_controller.model.stack
        self.model = main_controller.model
        self.view = main_controller.view
        self.plot_click_handler = PlotClickHandler(main_controller)
        self.connect_signals()

    def connect_signals(self):
        # Connect the remove and add layer buttons to their respective functions
        self.view.main_window.layer_control.btnRemove.clicked.connect(self.remove_layer)
        self.view.main_window.layer_control.btnAdd.clicked.connect(self.add_layer)

    def init_plot(self, stack_name):
        # Initialize the plot for the given stack
        layer_plot = self.view.main_window.stack.layer_widget.layer_plot
        song_overview_plot = self.view.main_window.song_overview.song_plot
        frame_qty = self.model.stack.objects[stack_name].frame_qty

        x_ticks = np.arange(0, frame_qty, 1)
        y_values = np.zeros(frame_qty)

        num_layers = len(self.model.stack.objects[stack_name].layers)

        # Plot the layer plot and link it to the song_overview_plot
        layer_plot.plot(x_ticks, y_values, pen=None)
        layer_plot.setXLink(song_overview_plot)

        self.init_v_line()
        self.set_layer_plot_limits(0, frame_qty, 0, num_layers)
        self.connect_layer_plot_signals(layer_plot)

    def reload_layer_plot(self):
        # Clear the layer plot and reinitialize it
        self.view.main_window.stack.layer_widget.layer_plot.clear()
        layers = self.model.stack.objects[self.model.stack.loaded_stack].layers
        self.init_plot(self.model.stack.loaded_stack)
        self.update_layer_plot_height()

        for index, layer in enumerate(layers):
            self.add_plot_layer(layer.name)

    def replot_layer_plot(self):
        # Replot the layer plot
        layer_plot = self.view.main_window.stack.layer_widget.layer_plot
        layer_plot.replot()

    def add_layer(self):
        # Add a new layer to the stack
        if self.model.stack.objects != None:
            layer_name = DialogWindow.input_text("Enter Layer Name", "Layer Name")
            self.add_model_layer(layer_name)
            self.add_plot_layer(layer_name)

    def remove_layer(self):
        # Remove a layer from the stack
        layer_name = DialogWindow.input_text("Enter Layer Name", "Layer Name")
        stack = self.model.stack.objects[self.model.stack.loaded_stack]
        stack.remove_layer_from_model(layer_name)
        self.main_controller.layer_controller.reload_layer_plot()

    def add_model_layer(self, layer_name):
        # Add a new layer to the model
        self.model.stack.objects[self.model.loaded_song.name].create_layer(layer_name)

    def add_plot_layer(self, layer_name):
        # Add a new layer to the plot
        stack = self.model.stack.objects[self.model.loaded_song.name]
        layer_plot = self.view.main_window.stack.layer_widget.layer_plot
        self.refresh_plot_data_item(layer_name)
        layer_plot_item = stack.layers[stack.get_layer_index(layer_name)].plot_data_item
        layer_plot.addItem(layer_plot_item)

        self.update_layer_names()
        self.update_layer_plot_height()
        self.refresh_plot_widget_layer(layer_name)

    def refresh_plot_widget_layer(self, layer_name):
        # Refresh the layer plot widget
        stack = self.model.stack.objects[self.model.song.loaded_song]
        plot = self.view.main_window.stack.layer_widget.layer_plot

        layer_index = stack.get_layer_index(layer_name)
        layer_plot_item = stack.layers[layer_index].plot_data_item

        plot.removeItem(layer_plot_item)
        plot.addItem(stack.layers[layer_index].plot_data_item)

        layer_qty = stack.get_layer_qty()
        self.set_layer_plot_limits(yMax=layer_qty)

    def update_layer_names(self):
        # Update the names of the layers
        loaded_stack = self.model.stack.objects[self.model.stack.loaded_stack]
        layer_names = [
            layer.name
            for layer in loaded_stack.layers
        ]
        self.view.main_window.stack.layer_widget.update_layer_names(layer_names)

    def update_layer_plot_height(self):
        # Update the height of the layer plot
        layer_height = 50  # You can adjust this value as needed
        offset = 18 # This encompasses the x axis height 
        num_layers = len(self.model.stack.objects[self.model.stack.loaded_stack].layers)

        total_height = num_layers * layer_height + offset

        self.view.main_window.stack.layer_widget.layer_plot.setFixedHeight(total_height)

    def set_layer_plot_limits(self, xMin=0, xMax=None, yMin=0, yMax=None):
        # Set the limits of the layer plot
        layer_plot = self.view.main_window.stack.layer_widget.layer_plot
        limits = {}

        if xMin is not None:
            limits["xMin"] = xMin
        if xMax is not None:
            limits["xMax"] = xMax
        if yMin is not None:
            limits["yMin"] = yMin
        if yMax is not None:
            limits["yMax"] = yMax

        layer_plot.setLimits(**limits)
        # Auto re-zoom the plot to fit the new changed limits
        # But only zoom out the y axis 100%
        layer_plot.getViewBox().setRange(yRange=(yMin, yMax), padding=0)

    def refresh_plot_data_item(self, layer_name):
        # Refresh the plot data item for the given layer
        stack = self.model.stack.objects[self.model.song.loaded_song]
        # translate raw data to plot data
        plottable_data = self.translate_raw_data_to_plot_data(layer_name)
        # get the layer plot item
        stack.set_event_plot_data_item(layer_name, plottable_data)

    def translate_raw_data_to_plot_data(self, layer_name):
        # Translate the raw data of a layer to plottable data
        stack = self.model.stack.objects[self.model.loaded_song.name]
        raw_data = stack.get_layer_raw_data(layer_name)
        layer_index = stack.get_layer_index(layer_name)

        present_events_array = [(key, (layer_index + 0.5)) for key, value in raw_data.items() if value is not None]

        plottable_data = np.array(present_events_array)
        return plottable_data

    def calculate_frame_quantity(self, length_ms, fps):
        # Calculate the number of frames for a given length and fps
        frame_qty = math.ceil((length_ms / 1000) * fps)
        print(f"# of frames for {(length_ms / 1000)}seconds @ {fps}fps is {frame_qty}")
        return frame_qty

    def init_v_line(self):
        # Initialize the vertical line in the layer widget
        layer_widget = self.view.main_window.stack.layer_widget
        layer_widget.init_v_line()
        self.main_controller.audio_playback_controller.time_update_thread.time_updated.connect(
            self.update_v_line_position
        )

    def update_v_line_position(self, frame_number):
        # Update the position of the vertical line
        v_line = self.view.main_window.stack.layer_widget.v_line
        v_line.setPos(float(frame_number))

    def tally_events(event_data):
        # Count the number of events in the event data
        return sum(1 for value in event_data.values() if value is not None)

    def on_plot_click(self, event, event_plot):
        # Handle a click on the plot
        if event.button() == Qt.LeftButton:
            scene_pos = event.scenePos()
            plot_pos = event_plot.plotItem.vb.mapSceneToView(scene_pos)
            print(f"[PLOT CLICK] scene: {scene_pos} | plot: {plot_pos} ")
            self.plot_click_handler.handle_click(scene_pos, plot_pos)

    def connect_layer_plot_signals(self, layer_plot):
        # Connect the plot click signal to the on_plot_click function
        layer_plot.scene().sigMouseClicked.connect(
            lambda event, layer_plot=layer_plot: self.on_plot_click(event, layer_plot)
        )

    def disconnect_layer_plot_signals(self, layer_plot):
        # Disconnect the plot click signal from the on_plot_click function
        try:
            layer_plot.scene().sigMouseClicked.disconnect(
                lambda event, layer_plot=layer_plot: self.on_plot_click(event, layer_plot)
            )
        except TypeError:
            print("No signals connected to the plot.")

class PlotClickHandler:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.model = main_controller.model

    def handle_click(self, scene_pos, plot_pos):
        playback_mode = self.main_controller.playback_mode_controller.get_current_mode()

        if playback_mode == "Record":
            self.handle_record_click(scene_pos, plot_pos)
        # Add more elif conditions here for other playback modes

        if playback_mode == "Edit":
            self.handle_edit_click(scene_pos, plot_pos)

        if playback_mode == "Play":
            print(f"Playback mode: Play selected, doing nothing")

    def handle_record_click(self, scene_pos, plot_pos):
        loaded_stack = self.model.stack.loaded_stack
        matched_layer_index = math.floor(plot_pos.y())
        matched_layer_name = (
            self.model.stack.objects[loaded_stack].layers[matched_layer_index].name
        )

        matched_frame = self.match_click_to_frame(scene_pos, plot_pos)

        print(f"Matched layer {matched_layer_index} matched frame: {matched_frame}")
        # Add the EventItem to the appropriate layer in the LayerModel
        if matched_layer_index < len(self.model.stack.objects[loaded_stack].layers):
            self.model.stack.objects[loaded_stack].layers[matched_layer_index].add(
                matched_frame
            )
        else:
            print("Layer doesn't exist at index")

        self.main_controller.layer_controller.refresh_plot_data_item(matched_layer_name)
        self.main_controller.layer_controller.refresh_plot_widget_layer(
            matched_layer_name
        )
        print(f"end handle_plot_click")

    def handle_edit_click(self, scene_pos, plot_pos):
        loaded_stack = self.model.stack.loaded_stack
        matched_layer_index = math.floor(plot_pos.y())
        matched_frame = self.match_click_to_frame(scene_pos, plot_pos)

        print(f"Matched layer {matched_layer_index} matched frame: {matched_frame}")
        try:
            event_object = (
                self.model.stack.objects[loaded_stack]
                .layers[matched_layer_index]
                .objects[matched_frame]
            )
        except KeyError:
            DialogWindow.error(
                f"Error: Event at frame {matched_frame} does not exist within {matched_layer_index}."
            )
            return

        self.main_controller.event_controller.edit_event(event_object)

    def match_click_to_frame(self, scene_pos, plot_pos):
        print(f"Matching click raw x: {scene_pos} / plot pos x {plot_pos}")
        frame_number = int(round(plot_pos.x()))
        print(f"--> Matched to frame: {frame_number}")
        return frame_number


class EventController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.stack = main_controller.model.stack
        self.model = main_controller.model
        self.view = main_controller.view

    def clear_event_plot(self, layer_name):
        widget = self.main_controller.layer_controller.get_widget_by_name(layer_name)
        widget.event_plot.clear()

    def add_event_to_plot(self, layer_name, frame_number):
        print(f"layer: {layer_name}, adding event at frame {frame_number}")
        self.main_controller.layer_controller.replot_layer(layer_name)

    def edit_event(self, event_object):
        self.editor = EventEditorWidget(event_object)
        self.editor.exec_()


# =========================================================================================================================================
# Thread Classes
# =========================================================================================================================================


class TimeUpdateThread(QThread):
    # Define a signal that will be emitted every time the label needs to be updated
    time_updated = pyqtSignal(int)

    STOPPED, RUNNING, PAUSED = range(3)

    def __init__(self):
        super().__init__()
        # self.model = main_controller.model
        self.state = self.STOPPED
        self.elapsed_time = 0
        self.start_time = None
        self.pause_time = None
        self.condition = Condition()
        self.time_per_frame_seconds = constants.PROJECT_FPS / 1000  # time per frame in seconds

    def run(self):
        while True:
            with self.condition:
                while self.state != self.RUNNING:
                    self.condition.wait()  # Pauses the thread
                adjusted_time = self.elapsed_time + (
                    time.perf_counter() - self.start_time
                )
                frame_number = int(adjusted_time * constants.PROJECT_FPS)
                self.time_updated.emit(frame_number)
            time.sleep(self.time_per_frame_seconds)

    def start_clock(self):
        with self.condition:
            if self.state == self.STOPPED:
                print(f"starting clock")
                self.start_time = time.perf_counter()
                self.state = self.RUNNING
                self.condition.notify_all()  # Wakes up all threads waiting on this condition
                self.start()  # Begins execution of the thread

    def pause_clock(self):
        with self.condition:
            if self.state == self.RUNNING:
                print(f"paused clock")
                self.paused_time = time.perf_counter()
                self.elapsed_time = self.paused_time - self.start_time
                self.state = self.PAUSED

    def resume_clock(self):
        with self.condition:
            if self.state == self.PAUSED:
                print(f"resuming clock")
                # get the elapsed time
                self.start_time = time.perf_counter()
                self.state = self.RUNNING
                self.condition.notify_all()

    def reset_clock(self):
        with self.condition:
            if self.state == self.PAUSED:
                print(f"resetting clock")
                self.elapsed_time = 0
                self.start_time = None

            elif self.state == self.RUNNING:
                print(f"resetting clock")
                self.state = self.PAUSED
                self.elapsed_time = 0
                self.start_time = time.perf_counter()
                self.state = self.RUNNING
                self.condition.notify_all()

            elif self.state == self.STOPPED:
                print(f"resetting clock")
                self.state = self.STOPPED
                self.elapsed_time = 0
                self.start_time = None

    def stop_clock(self):
        if self.state == self.RUNNING:
            self.state = self.STOPPED

        if self.state == self.PAUSED:
            self.state = self.STOPPED

