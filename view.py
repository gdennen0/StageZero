import math
import numpy as np
import pyqtgraph as pg
from threading import Condition

from pyqtgraph import AxisItem, InfiniteLine, mkPen
from PyQt5.QtCore import (
    Qt,
)
from PyQt5.QtWidgets import (
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