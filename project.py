import sys
import json
import librosa
import math
import numpy as np
import pyqtgraph as pg
import time
import vlc
from threading import Condition

from pyqtgraph import AxisItem, InfiniteLine, mkPen
from PyQt5.QtCore import (
    pyqtSignal,
    Qt,
    QThread,
)
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QFileDialog,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QInputDialog,
    QScrollArea,
    QComboBox,
    QSizePolicy,
    QDialog,
    QLineEdit,
    QColorDialog,
    QMessageBox,
)


# Constants until init file is implemented
PROJECT_FPS = 30

# =========================================================================================================================================
# Model Classes
# =========================================================================================================================================


class MainModel:
    def __init__(self):
        self.project_name = None
        self.song = SongModel()
        self.stack = StackModel()

    def get_loaded_stack(self):
        return self.stack.loaded_stack

    def get_loaded_song(self):
        loaded_song = self.song.loaded_song
        if loaded_song == None:
            print(f"[MODEL][MAIN][get_loaded_song] | No song loaded")
        return loaded_song


class SongModel:
    # Manage Song Item Instances
    def __init__(self):
        self.CLASS_TYPE = "MODEL"
        self.objects = {}
        self.loaded_song = None

    # Method to take a file path and name and ingest the rest of the song item data
    @staticmethod
    def build_song_object(file_path, song_name):
        song_object = SongItem(song_name, file_path)
        return song_object

    # Method to add song object to song dict
    def add_song_object_to_model(self, song_object):
        self.objects[song_object.name] = song_object


class SongItem:
    # Song Item Attributes
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.song_data, self.sample_rate = self.load_song_data(path)
        self.length_ms = self.calculate_length_ms()
        self.frame_qty = self.calculate_frame_qty()

    @staticmethod
    def load_song_data(path):
        # ingest song data & sample rate
        return librosa.load(path, sr=2000)

    def calculate_length_ms(self):
        duration_sec = librosa.get_duration(y=self.song_data, sr=self.sample_rate)
        return duration_sec * 1000

    def calculate_frame_qty(self):
        frame_qty = round(self.length_ms / 1000 * PROJECT_FPS)
        return frame_qty


class StackModel:
    def __init__(self):
        # Init the stack dict
        self.objects = {}
        self.loaded_stack = None

    # add a new stack
    def create_stack(self, stack_name):
        self.objects[stack_name] = LayerModel()

    def get_loaded_stack(self):
        return self.loaded_stack

    def set_frame_qty(self, stack_name, frame_qty):
        self.objects[stack_name].frame_qty = frame_qty


class LayerModel:
    # Manage Layer Item Instances and events item instances
    def __init__(self):
        # Init the layers dict
        self.layers = []
        self.frame_qty = None
        # objet global frame_qty

    def get_layer_index(self, layer_name):
        for index, layer in enumerate(self.layers):
            print(f"There are {len(self.layers)} layers in the list.")
            print(f"Checking layer at index: {index} whose name is {layer.name}")
            if layer.name == layer_name:
                print(
                    f"[MODEL][LAYERMODEL][get_layer_index] | Matched layer named: {layer_name} to index {index}"
                )
                return index
        print(
            f"[MODEL][LAYERMODEL][get_layer_index] | No matched layer named: {layer_name}"
        )
        return None

    def get_layer_qty(self):
        return len(self.layers)

    def create_layer(self, layer_name):
        self.add_layer_to_model(layer_name)

    def add_layer_to_model(self, layer_name, index=None):
        layer = EventModel(layer_name)
        # Add a layer item to the layers dict
        if index is None:
            self.layers.append(layer)
            print(f"[MODEL] appended Layer Object {layer_name}")
        else:
            self.layers.insert(index, layer)
            print(f"[MODEL] inserted Layer Object at index: {index}")
            self.update_layer_indices()

    def set_event_data(self, layer_name, object_data):
        index = self.get_layer_index(layer_name)
        self.layers[index].objects = object_data

    def create_layer_plot_data_item(self, layer_name):
        index = self.get_layer_index(layer_name)
        self.layers[index].plot_data_item = pg.PlotDataItem()

    def set_event_plot_data_item(self, layer_name, plot_data):
        index = self.get_layer_index(layer_name)
        self.layers[index].plot_data_item = pg.PlotDataItem(
            plot_data, symbol="o", pen=None
        )

    def remove_layer_from_model(self, layer_name):
        # Filter out the layer with the given layer_name
        layer_index = self.get_layer_index(layer_name)
        del self.layers[layer_index]
        # self.update_layer_indices()

    def move_layer_to_index(self, layer_name, new_index):
        # Find the layer with the given layer_name
        layer_to_move = next(
            (layer for layer in self.layers if layer["layer_name"] == layer_name), None
        )
        # If the layer exists, proceed
        if layer_to_move is not None:
            # Remove the layer from its current position
            self.layers.remove(layer_to_move)
            # Insert the layer at the new index
            self.layers.insert(new_index, layer_to_move)
            # Update the indices of all layers
            self.update_layer_indices()

    def get_layer_raw_data(self, layer_name):
        index = self.get_layer_index(layer_name)
        return self.layers[index].objects

    def update_layer_indices(self):
        for i, layer in enumerate(self.layers):
            layer.index = i

    def set_frame_qty(self, qty):
        self.frame_qty = qty


class EventModel:
    def __init__(self, name):
        self.name = name
        self.objects = {}
        self.plot_data_item = None

    def add(self, index):
        self.objects[index] = EventItem()


class LayerItem:
    def __init__(self, layer_name):
        self.name = layer_name
        self.event = EventModel()


class EventItem:
    def __init__(self, event_name="Default", color=(255,255,255)):
        self.name = event_name
        self.color = color


# =========================================================================================================================================
# View Classes
# =========================================================================================================================================


class MainView:
    def __init__(self):
        self.launch_window = LaunchWindow()
        self.main_window = MainWindow()


class LaunchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self):
        self.layout = QVBoxLayout(self)

        self.new_project_button = QPushButton("New Project", self)
        self.load_project_button = QPushButton("Load Project", self)

        self.layout.addWidget(self.new_project_button)
        self.layout.addWidget(self.load_project_button)

    # Launch Window Structure
    def open(self):
        # calling the show method of the super class
        super().show()

    def close(self):
        # calling the close method of the super class
        super().close()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize()

    def open(self, title):
        self.label = title
        self.setWindowTitle(self.label)
        self.show()

    def close(self):
        self.close()

    def initialize(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)  # Set spacing to zero

        self.song_select_menu = SongSelectWidget()
        self.song_overview = SongOverviewWidget()
        self.audio_playback_command = AudioPlaybackCommandWidget()
        self.layer_control = LayerControlWidget()
        self.stack = StackWidget()
        self.playback_mode = PlaybackModeWidget()

        # Set the size policy for song_select_menu and song_overview
        self.song_select_menu.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.song_overview.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self.layout.addWidget(self.song_select_menu)
        self.layout.addWidget(self.song_overview)
        self.layout.addWidget(self.playback_mode)
        self.layout.addWidget(self.audio_playback_command)
        self.layout.addWidget(self.layer_control)
        self.layout.addWidget(self.stack)


class AudioPlaybackCommandWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(1, 1, 1, 1)  # Set half as much padding

        self.play_button = QPushButton("Play", self)
        self.pause_button = QPushButton("Pause", self)
        self.reset_button = QPushButton("Reset", self)
        self.time_label = QLabel("Frame: ", self)

        self.layout.addWidget(self.time_label)  # And this line
        self.layout.addWidget(self.play_button)
        self.layout.addWidget(self.pause_button)
        self.layout.addWidget(self.reset_button)


class PlaybackModeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(1, 1, 1, 1)  # Set half as much padding

        self.label = QLabel("Playback Mode", self)
        self.playback_mode_selector = QComboBox(self)
        self.playback_mode_selector.addItems(["Play", "Edit", "Record"])

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.playback_mode_selector)


class EventEditorWidget(QDialog):
    def __init__(self, event_object, parent=None):
        super().__init__(parent)
        self.event_object = event_object
        self.layout = QVBoxLayout(self)

        self.attr1_edit = QLineEdit(self)
        self.attr1_edit.setText(str(self.event_object.name))
        self.layout.addWidget(self.attr1_edit)

        # Create a button for opening the color dialog
        self.color_button = QPushButton("Choose color", self)
        self.color_button.clicked.connect(self.open_color_dialog)
        self.layout.addWidget(self.color_button)

        # Create a save button
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_changes)
        self.layout.addWidget(self.save_button)

    def open_color_dialog(self):
        # Open the color dialog and get the selected color
        color = QColorDialog.getColor()

        # If a color was selected (the user didn't cancel the dialog), update the event_object's color
        if color.isValid():
            self.event_object.color = color.name()

    def save_changes(self):
        # Update the event_object attributes with the new values from the QLineEdit widgets
        self.event_object.name = self.attr1_edit.text()

        # Close the dialog
        self.accept()



class LayerControlWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(1, 0.5, 0.5, 1)  # Set half as much padding

        self.label = QLabel(f"Layer Controls")
        self.layout.addWidget(self.label)

        self.btnRemove = QPushButton("Remove", self)
        self.btnAdd = QPushButton("Add", self)

        self.layout.addWidget(self.btnAdd)
        self.layout.addWidget(self.btnRemove)


class StackWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)  # Set spacing to zero

        # Add label at the top
        self.label = QLabel("Layers")
        self.layout.addWidget(self.label)

        # Creating a scroll area
        self.scroll_area = QScrollArea(self)
        # self.scroll_area.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        self.stack_content = QWidget()
        self.stack_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stack_content_layout = QVBoxLayout(self.stack_content)
        self.stack_content_layout.setContentsMargins(0, 0, 0, 0)
        self.stack_content_layout.setSpacing(0)
        self.stack_content_layout.setAlignment(Qt.AlignTop)

        self.scroll_area.setWidget(self.stack_content)

        self.layer_widget = LayerWidget()
        self.stack_content_layout.addWidget(self.layer_widget, alignment=Qt.AlignTop)

        self.stack_content_layout.update()
        self.scroll_area.update()


class LayerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize()
        # self.setObjectName(layer_name)

    def initialize(self):
        self.layout = QHBoxLayout(self)  # Set the layer widget layout to horizontal
        self.layout.setContentsMargins(0, 0, 12, 0)

        self.custom_axis = CustomAxis(orientation="left")
        self.layer_plot = pg.PlotWidget(axisItems={"left": self.custom_axis})
        self.layout.addWidget(self.layer_plot)
        self.layer_plot.setFixedHeight(0)
        self.layer_plot.showGrid(x=True, y=True, alpha=1)
        # self.event_plot.setFixedHeight(35)
        self.layer_plot.getViewBox().setMouseEnabled(y=False)

    def add_plot_layer(self, plot_layer_item):
        # Add the PlotDataItem to the plot
        self.layer_plot.addItem(plot_layer_item)

    def update_layer_names(self, layer_names):
        self.custom_axis.setLayers(layer_names)
        self.layer_plot.update()

    def init_v_line(self):
        line_specs = mkPen(color="w", width=2)
        self.v_line = InfiniteLine(angle=90, movable=True, pen=line_specs)
        self.layer_plot.addItem(self.v_line)


class CustomAxis(AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layers = []

    def setLayers(self, layers):
        self.layers = layers

    def tickValues(self, minVal, maxVal, size):
        minVal, maxVal = sorted((minVal, maxVal))
        ticks = []
        # Generate ticks at intervals of 1
        major_ticks = np.arange(math.floor(minVal), math.ceil(maxVal) + 1)
        ticks.append((1.0, major_ticks))
        # Generate ticks at intervals of 0.5
        minor_ticks = np.arange(math.floor(minVal * 2), math.ceil(maxVal * 2) + 1) / 2
        ticks.append((0.5, minor_ticks))
        return ticks

    def tickStrings(self, values, scale, spacing):
        strings = []
        for tick_value in values:
            index = int(tick_value)
            if 0 <= index < len(self.layers) and tick_value % 1 == 0.5:
                strings.append(self.layers[index])
            else:
                strings.append("")
        return strings


class SongSelectWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self):
        self.layout = QHBoxLayout(self)
        self.label = QLabel(f"Select Song")
        self.add_new_song = QPushButton("Add New Song", self)
        self.song_selector = QComboBox(self)

        # Place the child widgets within the SongSelectWidget layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.add_new_song)
        self.layout.addWidget(self.song_selector)


class SongOverviewWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initWidget()

    def initWidget(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 12, 0)
        self.label = QLabel(f"Song Overview")

        self.song_plot = pg.PlotWidget()

        self.song_plot.setFixedHeight(100)
        self.song_plot.setContentsMargins(0, 0, 0, 0)

        self.song_plot.showGrid(x=True, y=False, alpha=1)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.song_plot)

    def init_v_line(self):
        line_specs = mkPen(color="w", width=2)
        self.v_line = InfiniteLine(angle=90, movable=True, pen=line_specs)
        self.song_plot.addItem(self.v_line)

    def plot_events(self, ticks, song_data):
        self.song_plot.setLimits(
            xMin=0,
            xMax=ticks[-1],
            yMin=0,
            yMax=1,
            minYRange=1,
            maxYRange=1,
        )
        self.song_plot.plot(ticks, song_data)

        y_axis = self.song_plot.getAxis("left")
        y_axis.setTicks([])

    def update_plot(self, ticks, song_data):
        # logic to update plot
        self.song_plot.clear()
        self.plot_events(ticks, song_data)

# Class to encapsulate any dialog/popup window for prompting user interaction
class DialogWindow:
    # Prompt user to select a file to open
    def open_file(title, dir, filter):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            title,
            dir,
            filter,
            options=options,
        )
        return file_path

    # Prompt user to select file save name/path
    def save_file(title, dir, filter):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            None,
            title,
            dir,
            filter,
            options=options,
        )
        return file_path

    # Prompt user to input text
    def input_text(title, label):
        name, ok = QInputDialog.getText(None, title, label)
        if ok:
            return name

    def error(message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(message)
        msg.setWindowTitle("Error")
        msg.exec_()


# =========================================================================================================================================
# Controller Classes
# =========================================================================================================================================


class MainController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Centralize All of the controllers
        self.project_controller = ProjectController(self)
        self.song_controller = SongController(self)
        self.stack_controller = StackController(self)
        self.layer_controller = LayerController(self)
        self.song_overview_controller = SongOverviewController(self)
        self.song_select_controller = SongSelectController(self)
        self.event_controller = EventController(self)
        self.audio_playback_controller = AudioPlaybackController(self)
        self.playback_mode_controller = PlaybackModeController(self)

    def initialize_app(self):
        # Open the main window
        self.view.launch_window.open()
        # Connect the launch windows new project button click signal to connect to project controller new project method


class ProjectController:
    # This class should contain methods that update the ProjectModel based on user input,
    # and update the MainWindow to reflect changes in the ProjectModel.
    def __init__(self, main_controller):
        self.model = main_controller.model
        self.view = main_controller.view
        # Connect the launch windows new project button click signal to connect to project controller new project method
        self.view.launch_window.new_project_button.clicked.connect(self.new_project)
        # Connect the launch windows load project button click signal to connect to project controller load project method
        self.view.launch_window.load_project_button.clicked.connect(self.load_project)

    def new_project(self):
        print(f"Begin Initializing New Project")
        project_name = DialogWindow.input_text("Input Text", "Project Name")
        self.model.project_name = project_name

        self.view.main_window.open(project_name)
        self.view.launch_window.close()

    def load_project(self):
        print(f"Begin Loading Project")

class SongSelectController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.view = main_controller.view
        self.model = main_controller.model
        self.generate_dropdown_items()
        self.connect_signals()

    def connect_signals(self):
        self.view.main_window.song_select_menu.song_selector.currentIndexChanged.connect(
            self.on_song_selected
        )
        self.view.main_window.song_select_menu.add_new_song.clicked.connect(
            self.main_controller.song_controller.add_song
        )

    def generate_dropdown_items(self):
        # Add the selected song to the dropdown menu
        if self.model.song.loaded_song != None:
            self.view.main_window.song_select_menu.song_selector.addItem(
                self.model.song.loaded_song
            )
        # add the remaining songs to the dropdown menu
        for song_name in self.model.song.objects:
            if song_name != self.model.song.loaded_song:
                self.view.main_window.song_select_menu.song_selector.addItem(song_name)

    def on_song_selected(self, index):
        if index == -1:
            return
        selected_song = self.view.main_window.song_select_menu.song_selector.itemText(
            index
        )
        print(f"Selected song: {selected_song} index: {index}")
        self.main_controller.song_controller.load_song(selected_song)

    def update_dropdown(self):
        # Clear the dropdown
        self.view.main_window.song_select_menu.song_selector.clear()
        # Generate and place the dropdown Items
        self.generate_dropdown_items()

class PlaybackModeController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.view = main_controller.view
        self.model = main_controller.model
        self.playback_modes = ["Play", "Edit", "Record"]
        self.connect_signals()

    def connect_signals(self):
        self.view.main_window.playback_mode.playback_mode_selector.currentIndexChanged.connect(
            self.on_playback_mode_changed
        )

    def get_current_mode(self):
        current_index = (
            self.view.main_window.playback_mode.playback_mode_selector.currentIndex()
        )
        if current_index != -1:
            return self.playback_modes[current_index]
        else:
            return None

    def on_playback_mode_changed(self, index):
        if index == -1:
            return
        selected_mode = (
            self.view.main_window.playback_mode.playback_mode_selector.itemText(index)
        )
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
    STOPPED, RUNNING, PAUSED = range(3)

    def __init__(self, main_controller):
        self.model = main_controller.model
        self.view = main_controller.view
        self.song_model = main_controller.model.song
        self.player = vlc.MediaPlayer()
        self.state = self.STOPPED
        self.init_connections()

        self.time_update_thread = TimeUpdateThread()
        self.time_update_thread.time_updated.connect(self.update_time_label)

    def load_song(self):
        song_path = self.song_model.objects[self.model.song.loaded_song].path
        self.player.set_media(vlc.Media(song_path))

    def play(self):
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
        if self.state == self.RUNNING:
            print(f"pause button pressed")
            self.state = self.PAUSED
            self.player.pause()
            self.time_update_thread.pause_clock()

    def reset(self):
        if self.state == self.PAUSED:
            self.time_update_thread.reset_clock()
            print(f"reset button pressed")

        elif self.state == self.RUNNING:
            self.time_update_thread.reset_clock()
            print(f"reset button pressed")

        elif self.state == self.STOPPED:
            self.time_update_thread.stop_clock()
            self.time_update_thread.reset_clock()

    def stop(self):
        self.state = self.STOPPED
        self.time_update_thread.stop_clock()

    def get_playback_time(self):
        return self.player.get_time()  # Returns playback time in milliseconds

    def init_connections(self):
        self.view.main_window.audio_playback_command.play_button.clicked.connect(
            self.play
        )
        self.view.main_window.audio_playback_command.pause_button.clicked.connect(
            self.pause
        )
        self.view.main_window.audio_playback_command.reset_button.clicked.connect(
            self.reset
        )

    def update_time_label(self, frame_number):
        # print(f"[update_time_label] frame: {frame_number}")
        frame_label_string = f"Frame: {frame_number}/{self.model.song.objects[self.model.song.loaded_song].frame_qty}"
        self.view.main_window.audio_playback_command.time_label.setText(
            frame_label_string
        )

class SongOverviewController:
    def __init__(self, main_controller):
        self.model = main_controller.model
        self.song_overview_widget = main_controller.view.main_window.song_overview
        self.main_controller = main_controller
        self.view = main_controller.view

    def generate_ticks(self):
        # Match a tick to a song_data index
        song = self.model.get_loaded_song()
        length_ms = self.model.song.objects[song].length_ms
        frame_qty = self.calculate_frame_quantity(length_ms, PROJECT_FPS)
        song_data = self.model.song.objects[song].song_data
        sample_rate = self.model.song.objects[song].sample_rate
        samples_per_frame = sample_rate / PROJECT_FPS

        frame_numbers = np.arange(len(song_data)) / samples_per_frame

        return frame_numbers

    def init_v_line(self):
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
        ticks = self.generate_ticks()
        song_data = self.model.song.objects[self.model.song.loaded_song].song_data
        self.song_overview_widget.update_plot(ticks, song_data)
        self.init_v_line()

class SongController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.model = main_controller.model
        self.view = main_controller.view

    def print(self, function_type, string):
        print(f"[CONTROLLER][{function_type}] | {string}")

    def add_song(self):
        # Prompt user to input song file path
        file_path = DialogWindow.open_file(
            "Select Song", "", "Audio Files (*.mp3 *.wav);;All Files (*)"
        )
        # Prompt user to input song name
        song_name = DialogWindow.input_text("Enter Song Name", "Song Name")
        # ingest song into song item object
        song_object = self.model.song.build_song_object(file_path, song_name)
        # Try to add song to song model
        self.model.song.add_song_object_to_model(
            song_object
        )  # Create a stack for the new song
        self.main_controller.stack_controller.create_stack(song_name)
        # load the frame qty for the stack
        # self.main_controller.stack_controller.set_stack_frame_qty(song_name)
        # refresh the song_select_menu
        self.main_controller.song_select_controller.update_dropdown()

    def load_song(self, song_name):
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
        self.main_controller = main_controller
        self.model = main_controller.model
        self.view = main_controller.view

    def create_stack(self, stack_name):
        print(f"creating stack {stack_name}")
        self.model.stack.create_stack(stack_name)
        # set the frame qty for the stack
        self.set_stack_frame_qty(stack_name)
        self.main_controller.layer_controller.init_plot(stack_name)

    def change_stack(self, stack_name):
        self.model.stack.selected_stack = stack_name

    def get_loaded_stack(self):
        return self.model.stack.loaded_stack

    def set_stack_frame_qty(self, stack_name):
        frame_qty = self.model.song.objects[stack_name].frame_qty
        self.model.stack.objects[stack_name].set_frame_qty(frame_qty)


class LayerController:
    # This class should contain methods that update the LayerModel based on user input,
    # and update the LayerWidget and LayersContainer to reflect changes in the LayerModel
    def __init__(self, main_controller):
        # self.layer_model = main_controller.model.layer
        self.main_controller = main_controller
        self.stack = main_controller.model.stack
        self.model = main_controller.model
        self.view = main_controller.view
        self.plot_click_handler = PlotClickHandler(main_controller)
        self.connect_signals()

    def connect_signals(self):
        self.view.main_window.layer_control.btnRemove.clicked.connect(self.remove_layer)
        self.view.main_window.layer_control.btnAdd.clicked.connect(self.add_layer)

    def init_plot(self, stack_name):
        # Create variables for the functions/plots we will use
        layer_plot = self.view.main_window.stack.layer_widget.layer_plot
        song_overview_plot = self.view.main_window.song_overview.song_plot
        frame_qty = self.model.stack.objects[stack_name].frame_qty
        # print(f"Stack: {loaded_stack} frame qty: {frame_qty}")
        # initialize the plot x/y axis tick items
        x_ticks = np.arange(0, frame_qty, 1)
        y_values = np.zeros(frame_qty)

        num_layers = len(self.model.stack.objects[stack_name].layers)

        # plot the layer plot with the x/y ticks
        layer_plot.plot(x_ticks, y_values, pen=None)
        # link the plot to the song_overview_plot
        layer_plot.setXLink(song_overview_plot)

        #  self.update_layer_names()
        self.init_v_line()
        # set the limits to match the current songs total frame qty
        self.set_layer_plot_limits(0, frame_qty, 0, num_layers)
        # connect the click signals to this controller class, pass it the plot item
        self.connect_layer_plot_signals(layer_plot)

    def reload_layer_plot(self):
        self.view.main_window.stack.layer_widget.layer_plot.clear()
        layers = self.model.stack.objects[self.model.stack.loaded_stack].layers
        self.init_plot(self.model.stack.loaded_stack)
        self.update_layer_plot_height()

        for index, layer in enumerate(layers):
            self.add_plot_layer(layer.name)

    def replot_layer_plot(self):
        layer_plot = self.view.main_window.stack.layer_widget.layer_plot
        layer_plot.replot()

    def add_layer(self):
        # Check if a stack is loaded
        if self.model.stack.objects != None:
            # Prompt user for layer name
            layer_name = DialogWindow.input_text("Enter Layer Name", "Layer Name")
            # add a layer to the model
            self.add_model_layer(layer_name)
            self.add_plot_layer(layer_name)
            # self.init_plot()

    def remove_layer(self):
        layer_name = DialogWindow.input_text("Enter Layer Name", "Layer Name")
        stack = self.model.stack.objects[self.model.stack.loaded_stack]
        # 1. Remove the layer from the model.
        stack.remove_layer_from_model(layer_name)
        # 2. Reload the layer plot
        self.main_controller.layer_controller.reload_layer_plot()

    def add_model_layer(self, layer_name):
        self.model.stack.objects[self.model.song.loaded_song].create_layer(layer_name)

    def add_plot_layer(self, layer_name):
        stack = self.model.stack.objects[self.model.song.loaded_song]
        # get a reference to the layer plot
        layer_plot = self.view.main_window.stack.layer_widget.layer_plot
        self.refresh_plot_data_item(layer_name)
        layer_plot_item = stack.layers[stack.get_layer_index(layer_name)].plot_data_item
        layer_plot.addItem(layer_plot_item)
        self.update_layer_names()
        self.update_layer_plot_height()
        self.refresh_plot_widget_layer(layer_name)

    def refresh_plot_widget_layer(self, layer_name):
        stack = self.model.stack.objects[self.model.song.loaded_song]
        # get a reference to the layer plot
        plot = self.view.main_window.stack.layer_widget.layer_plot
        # get the layer index
        layer_index = stack.get_layer_index(layer_name)
        # get the layer plot item
        layer_plot_item = stack.layers[layer_index].plot_data_item
        # remove the old plot item
        plot.removeItem(layer_plot_item)
        # add the refreshed plot item back to the plot
        plot.addItem(stack.layers[layer_index].plot_data_item)

        layer_qty = stack.get_layer_qty()

        self.set_layer_plot_limits(yMax=layer_qty)

    def update_layer_names(self):
        layer_names = [
            layer.name
            for layer in self.model.stack.objects[self.model.stack.loaded_stack].layers
        ]
        self.view.main_window.stack.layer_widget.update_layer_names(layer_names)

    def update_layer_plot_height(self):
        # Define the fixed height for each layer
        layer_height = 50  # You can adjust this value as needed
        offset = 20
        # Define the height for margins, labels, etc.
        # Get the number of layers
        num_layers = len(self.model.stack.objects[self.model.stack.loaded_stack].layers)

        # Calculate the total height
        total_height = num_layers * layer_height + offset

        # Set the total height as the height of the layer_plot
        self.view.main_window.stack.layer_widget.layer_plot.setFixedHeight(total_height)

    def set_layer_plot_limits(self, xMin=0, xMax=None, yMin=0, yMax=None):
        # Get the layer plot from the main window
        layer_plot = self.view.main_window.stack.layer_widget.layer_plot
        # Initialize an empty dictionary to hold the limits
        limits = {}
        # If xMin is provided, add it to the limits dictionary
        if xMin is not None:
            limits["xMin"] = xMin
        # If xMax is provided, add it to the limits dictionary
        if xMax is not None:
            limits["xMax"] = xMax
        # If yMin is provided, add it to the limits dictionary
        if yMin is not None:
            limits["yMin"] = yMin
        # If yMax is provided, add it to the limits dictionary
        if yMax is not None:
            limits["yMax"] = yMax
        # Set the limits of the layer plot using the limits dictionary
        layer_plot.setLimits(**limits)
        # Auto re-zoom the plot to fit the new changed limits
        # But only zoom out the y axis 100%
        layer_plot.getViewBox().setRange(yRange=(yMin, yMax), padding=0)

    def refresh_plot_data_item(self, layer_name):
        stack = self.model.stack.objects[self.model.song.loaded_song]
        # translate raw data to plot data
        plottable_data = self.translate_raw_data_to_plot_data(layer_name)
        # get the layer plot item
        stack.set_event_plot_data_item(layer_name, plottable_data)

    def translate_raw_data_to_plot_data(self, layer_name):
        stack = self.model.stack.objects[self.model.song.loaded_song]
        raw_data = stack.get_layer_raw_data(layer_name)
        layer_index = stack.get_layer_index(layer_name)
        present_events_array = []
        for key, value in raw_data.items():
            if value is not None:
                print(f"Found Frame: {key}")
                # Append a tuple with X as the key and Y as the layer index
                present_events_array.append((key, (layer_index + 0.5)))

        # Ensure plottable_data is in the proper format for pg.PlotDataItem
        plottable_data = np.array(present_events_array)
        return plottable_data

    def calculate_frame_quantity(self, length_ms, fps):
        # Calculate the frame quantity and round up to the nearest whole frame
        frame_qty = math.ceil((length_ms / 1000) * fps)
        print(f"# of frames for {(length_ms / 1000)}seconds @ {fps}fps is {frame_qty}")
        return frame_qty

    def init_v_line(self):
        layer_widget = self.view.main_window.stack.layer_widget
        layer_widget.init_v_line()
        self.main_controller.audio_playback_controller.time_update_thread.time_updated.connect(
            self.update_v_line_position
        )

    def update_v_line_position(self, frame_number):
        # Get the vertical line from the layer widget
        v_line = self.view.main_window.stack.layer_widget.v_line
        # Update the position of the vertical line
        v_line.setPos(float(frame_number))

    def tally_events(event_data):
        return sum(1 for value in event_data.values() if value is not None)

    def on_plot_click(self, event, event_plot):
        if event.button() == Qt.LeftButton:
            # Get the position of the click in scene coordinates
            scene_pos = event.scenePos()
            # Get the x-coordinate of the click and round it to the nearest integer
            plot_pos = event_plot.plotItem.vb.mapSceneToView(scene_pos)
            # Retrieve the widget name from the event sender
            print(f"[PLOT CLICK] scene: {scene_pos} | plot: {plot_pos} ")
            self.plot_click_handler.handle_click(scene_pos, plot_pos)

    def connect_layer_plot_signals(self, layer_plot):
        layer_plot.scene().sigMouseClicked.connect(
            lambda event, layer_plot=layer_plot: self.on_plot_click(event, layer_plot)
        )


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
        self.time_per_frame_seconds = PROJECT_FPS / 1000  # time per frame in seconds

    def run(self):
        while True:
            with self.condition:
                while self.state != self.RUNNING:
                    self.condition.wait()  # Pauses the thread
                adjusted_time = self.elapsed_time + (
                    time.perf_counter() - self.start_time
                )
                frame_number = int(adjusted_time * PROJECT_FPS)
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
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainController(MainModel(), MainView())

    main.initialize_app()
    sys.exit(app.exec_())
