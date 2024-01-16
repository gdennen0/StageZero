import math  # For mathematical operations
import numpy as np  # For array operations
import pyqtgraph as pg  # For plotting
from threading import Condition  # For thread synchronization

from pyqtgraph import AxisItem, InfiniteLine, mkPen  # For customizing plots
from PyQt5.QtCore import (
    Qt,  # For Qt related operations
)
from PyQt5.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QAction,
    QWidget,  # Base class for all user interface objects
    QLabel,  # For displaying text or images
    QFileDialog,  # Dialog for users to select files or directories
    QHBoxLayout,  # Box layout with a horizontal direction
    QVBoxLayout,  # Box layout with a vertical direction
    QPushButton,  # Command button
    QInputDialog,  # Dialog for user input
    QScrollArea,  # Scrollable display area
    QComboBox,  # Drop down selection box
    QSizePolicy,  # Layout attribute describing horizontal and vertical resizing policy
    QDialog,  # Dialog window
    QLineEdit,  # One-line text editor
    QColorDialog,  # Dialog widget for specifying colors
    QMessageBox,  # Modal dialog for informing the user or for asking the user a question and receiving an answer
    QStackedWidget
)


# =========================================================================================================================================
# View Classes
# =========================================================================================================================================


class MainView(QMainWindow):  # Main view class
    def __init__(self):
        super().__init__()
        self.launch_window = LaunchWindow()  # Initialize launch window
        self.main_window = MainWidget()  # Initialize main window
        self.tools_window = ToolsWindow()
        self.main_menu = MainMenu()
        self.init_ui()

    def init_ui(self):
        # Set the application title in the menu bar
        self.setWindowTitle('StageZeroDev')
        # Set the custom menu bar
        self.setMenuBar(self.main_menu)

    def open_main_window(self):
        # Set the main window as the central widget
        self.setCentralWidget(self.main_window)
        self.show()

    def open_launch_window(self):
        self.setCentralWidget(self.launch_window)
        self.show()

class LaunchWindow(QWidget):  # Class for the launch window
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()  # Initialize the launch window

    def initialize(self):  # Initialize the launch window
        self.layout = QVBoxLayout(self)  # Set the layout to vertical box layout

        self.new_project_button = QPushButton("New Project", self)  # Button for creating a new project
        self.load_project_button = QPushButton("Load Project", self)  # Button for loading an existing project

        self.layout.addWidget(self.new_project_button)  # Add the new project button to the layout
        self.layout.addWidget(self.load_project_button)  # Add the load project button to the layout

    # Launch Window Structure
    def open(self):  # Open the launch window
        # calling the show method of the super class
        super().show()

    def close(self):  # Close the launch window
        # calling the close method of the super class
        super().close()


class MainWidget(QWidget):  # Class for the main window
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()  # Initialize the main window

    def open(self, title):  # Open the main window with a given title
        self.label = title  # Set the window title
        self.setWindowTitle(self.label)  # Set the window title
        self.show()  # Show the window

    def close(self):  # Close the main window
        self.close()  # Close the window

    def initialize(self):  # Initialize the main window
        self.layout = QVBoxLayout(self)  # Set the layout to vertical box layout
        self.layout.setSpacing(0)  # Set spacing to zero

        self.song_select_menu = SongSelectWidget()  # Widget for song selection
        self.song_overview = SongOverviewWidget()  # Widget for displaying song overview
        self.audio_playback_command = AudioPlaybackCommandWidget()  # Widget for controlling audio playback
        self.layer_control = LayerControlWidget()  # Widget for controlling layers
        self.stack = StackWidget()  # Widget for displaying the stack of layers
        self.playback_mode = PlaybackModeWidget()  # Widget for selecting the playback mode

        # Set the size policy for song_select_menu and song_overview
        self.song_select_menu.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)  # Set the size policy for song_select_menu
        self.song_overview.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)  # Set the size policy for song_overview

        self.layout.addWidget(self.song_select_menu)  # Add the song_select_menu to the layout
        self.layout.addWidget(self.song_overview)  # Add the song_overview to the layout
        self.layout.addWidget(self.playback_mode)  # Add the playback_mode to the layout
        self.layout.addWidget(self.audio_playback_command)  # Add the audio_playback_command to the layout
        self.layout.addWidget(self.layer_control)  # Add the layer_control to the layout
        self.layout.addWidget(self.stack)  # Add the stack to the layout


class MainMenu(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_menu_bar()

    def init_menu_bar(self):
        # File Menu Dropdown
        self.file_menu = self.addMenu('&File')

        self.save_action = QAction('&Save', self)
        self.exit_action = QAction('&Exit', self)
        
        self.save_action.setShortcut('Ctrl+S')
        self.exit_action.setShortcut('Ctrl+Q')

        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.exit_action)

        # View Menu Dropdown
        self.view_menu = self.addMenu('&View')
        
        self.tools_action = QAction('&Tool Window', self)
        self.view_menu.addAction(self.tools_action)


class ToolsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tools')
        self.initializeUI()

    def initializeUI(self):
        # Main layout for the Tools window
        self.layout = QVBoxLayout(self)

        # Dropdown menu to select a tool
        self.tool_selector = QComboBox(self)
        self.tool_selector.addItems(["BPM Counter", "Tool 2", "Tool 3"])  # Add tool names here
        self.tool_selector.currentIndexChanged.connect(self.toolSelected)
        self.layout.addWidget(self.tool_selector)

        # Stacked widget to hold different tool widgets
        self.tools_stack = QStackedWidget(self)
        self.layout.addWidget(self.tools_stack)

        # Initialize tool widgets and add them to the stack
        self.initializeTools()

    def initializeTools(self):
        # Tool widgets are initialized and added to the stack here
        # Example tool widgets
        self.bpm = BpmToolWidget()
        self.tool2_widget = QWidget()
        self.tool3_widget = QWidget()

        # Add tool widgets to the stack
        self.tools_stack.addWidget(self.bpm)
        self.tools_stack.addWidget(self.tool2_widget)
        self.tools_stack.addWidget(self.tool3_widget)

    def toolSelected(self, index):
        # Change the current widget in the stack based on the selected tool
        self.tools_stack.setCurrentIndex(index)

    def open(self):
        # Show the Tools window
        self.show()


class BpmToolWidget(QWidget):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()

    def initialize(self):
        self.layout = QVBoxLayout(self)    

        self.count_button = QPushButton("Count", self)
        self.paint_to_song_overview_button = QPushButton("Paint to SongOverview", self)
        self.remove_from_song_overview_button = QPushButton("Remove BPM from SongOverview", self)
        self.bpm_label = QLabel("BPM", self)

        self.layout.addWidget(self.count_button)
        self.layout.addWidget(self.paint_to_song_overview_button)
        self.layout.addWidget(self.remove_from_song_overview_button)
        self.layout.addWidget(self.bpm_label)

class AudioPlaybackCommandWidget(QWidget):  # Widget for controlling audio playback
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()  # Initialize the widget

    def initialize(self):  # Initialize the widget
        self.layout = QHBoxLayout(self)  # Set the layout to horizontal box layout
        self.layout.setContentsMargins(1, 1, 1, 1)  # Set half as much padding

        self.play_button = QPushButton("Play", self)  # Button for playing the audio
        self.pause_button = QPushButton("Pause", self)  # Button for pausing the audio
        self.reset_button = QPushButton("Reset", self)  # Button for resetting the audio
        self.time_label = QLabel("Frame: ", self)  # Label for displaying the current frame

        self.layout.addWidget(self.time_label)  # Add the time label to the layout
        self.layout.addWidget(self.play_button)  # Add the play button to the layout
        self.layout.addWidget(self.pause_button)  # Add the pause button to the layout
        self.layout.addWidget(self.reset_button)  # Add the reset button to the layout


class PlaybackModeWidget(QWidget):  # Widget for selecting the playback mode
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()  # Initialize the widget

    def initialize(self):  # Initialize the widget
        self.layout = QHBoxLayout(self)  # Set the layout to horizontal box layout
        self.layout.setContentsMargins(1, 1, 1, 1)  # Set half as much padding

        self.label = QLabel("Playback Mode", self)  # Label for the playback mode
        self.playback_mode_selector = QComboBox(self)  # Combo box for selecting the playback mode
        self.playback_mode_selector.addItems(["Play", "Edit", "Record"])  # Add the playback modes to the combo box

        self.layout.addWidget(self.label)  # Add the label to the layout
        self.layout.addWidget(self.playback_mode_selector)  # Add the playback mode selector to the layout


class EventEditorWidget(QDialog):  # Widget for editing events
    def __init__(self, event_object, parent=None):
        super().__init__(parent)  # Call the constructor of the parent class
        self.event_object = event_object  # The event to be edited
        self.layout = QVBoxLayout(self)  # Set the layout to vertical box layout

        self.attr1_edit = QLineEdit(self)  # Line edit for editing the first attribute
        self.attr1_edit.setText(str(self.event_object.name))  # Set the text of the line edit to the name of the event
        self.layout.addWidget(self.attr1_edit)  # Add the line edit to the layout

        # Create a button for opening the color dialog
        self.color_button = QPushButton("Choose color", self)  # Button for choosing the color
        self.color_button.clicked.connect(self.open_color_dialog)  # Connect the button click to the open_color_dialog method
        self.layout.addWidget(self.color_button)  # Add the color button to the layout

        # Create a save button
        self.save_button = QPushButton("Save", self)  # Button for saving the changes
        self.save_button.clicked.connect(self.save_changes)  # Connect the button click to the save_changes method
        self.layout.addWidget(self.save_button)  # Add the save button to the layout

    def open_color_dialog(self):  # Open the color dialog
        # Open the color dialog and get the selected color
        color = QColorDialog.getColor()

        # If a color was selected (the user didn't cancel the dialog), update the event_object's color
        if color.isValid():
            self.event_object.color = color.name()

    def save_changes(self):  # Save the changes
        # Update the event_object attributes with the new values from the QLineEdit widgets
        self.event_object.name = self.attr1_edit.text()

        # Close the dialog
        self.accept()



class LayerControlWidget(QWidget):  # Widget for controlling layers
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()  # Initialize the widget

    def initialize(self):  # Initialize the widget
        self.layout = QHBoxLayout(self)  # Set the layout to horizontal box layout
        self.layout.setContentsMargins(1, 0.5, 0.5, 1)  # Set half as much padding

        self.label = QLabel(f"Layer Controls")  # Label for the layer controls
        self.layout.addWidget(self.label)  # Add the label to the layout

        self.btnRemove = QPushButton("Remove", self)  # Button for removing a layer
        self.btnAdd = QPushButton("Add", self)  # Button for adding a layer

        self.layout.addWidget(self.btnAdd)  # Add the add button to the layout
        self.layout.addWidget(self.btnRemove)  # Add the remove button to the layout


class StackWidget(QWidget):  # Widget for displaying the stack of layers
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()  # Initialize the widget

    def initialize(self):  # Initialize the widget
        self.layout = QVBoxLayout(self)  # Set the layout to vertical box layout
        self.layout.setContentsMargins(0, 0, 0, 0)  # Set the margins to zero
        self.layout.setSpacing(0)  # Set spacing to zero

        # Add label at the top
        self.label = QLabel("Layers")  # Label for the layers
        self.layout.addWidget(self.label)  # Add the label to the layout

        # Creating a scroll area
        self.scroll_area = QScrollArea(self)  # Scroll area for the layers
        # self.scroll_area.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.scroll_area.setWidgetResizable(True)  # Make the widget resizable
        self.layout.addWidget(self.scroll_area)  # Add the scroll area to the layout

        self.stack_content = QWidget()  # Widget for the stack content
        self.stack_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set the size policy for the stack content
        self.stack_content_layout = QVBoxLayout(self.stack_content)  # Set the layout for the stack content to vertical box layout
        self.stack_content_layout.setContentsMargins(0, 0, 0, 0)  # Set the margins for the stack content layout to zero
        self.stack_content_layout.setSpacing(0)  # Set the spacing for the stack content layout to zero
        self.stack_content_layout.setAlignment(Qt.AlignTop)  # Align the stack content layout to the top

        self.scroll_area.setWidget(self.stack_content)  # Set the widget for the scroll area to the stack content

        self.layer_widget = LayerWidget()  # Widget for the layer
        self.stack_content_layout.addWidget(self.layer_widget, alignment=Qt.AlignTop)  # Add the layer widget to the stack content layout

        self.stack_content_layout.update()  # Update the stack content layout
        self.scroll_area.update()  # Update the scroll area


class LayerWidget(QWidget):  # Widget for a layer
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()  # Initialize the widget
        # self.setObjectName(layer_name)

    def initialize(self):  # Initialize the widget
        self.layout = QHBoxLayout(self)  # Set the layout to horizontal box layout
        self.layout.setContentsMargins(0, 0, 12, 0)  # Set the margins for the layout

        self.custom_axis = CustomAxis(orientation="left")  # Custom axis for the layer
        self.layer_plot = pg.PlotWidget(axisItems={"left": self.custom_axis})  # Plot widget for the layer
        self.layout.addWidget(self.layer_plot)  # Add the plot widget to the layout
        self.layer_plot.setFixedHeight(0)  # Set the fixed height for the plot widget
        self.layer_plot.showGrid(x=True, y=True, alpha=1)  # Show the grid for the plot widget
        # self.event_plot.setFixedHeight(35)
        self.layer_plot.getViewBox().setMouseEnabled(y=False)  # Disable mouse interaction for the y-axis

    def add_plot_layer(self, plot_layer_item):  # Add a plot layer to the layer widget
        # Add the PlotDataItem to the plot
        self.layer_plot.addItem(plot_layer_item)

    def update_layer_names(self, layer_names):  # Update the layer names
        self.custom_axis.setLayers(layer_names)  # Set the layers for the custom axis
        self.layer_plot.update()  # Update the plot widget

    def init_playhead(self):  # Initialize the vertical line
        line_specs = mkPen(color="w", width=2)  # Specifications for the line
        self.playhead = InfiniteLine(angle=90, movable=True, pen=line_specs)  # Create the line
        self.layer_plot.addItem(self.playhead)  # Add the line to the plot widget


class CustomAxis(AxisItem):  # Custom axis class
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call the constructor of the parent class
        self.layers = []  # Initialize the layers

    def setLayers(self, layers):  # Set the layers
        self.layers = layers  # Set the layers

    def tickValues(self, minVal, maxVal, size):  # Get the tick values
        minVal, maxVal = sorted((minVal, maxVal))  # Sort the minimum and maximum values
        ticks = []  # Initialize the ticks
        # Generate ticks at intervals of 1
        major_ticks = np.arange(math.floor(minVal), math.ceil(maxVal) + 1)  # Generate the major ticks
        ticks.append((1.0, major_ticks))  # Add the major ticks to the ticks
        # Generate ticks at intervals of 0.5
        minor_ticks = np.arange(math.floor(minVal * 2), math.ceil(maxVal * 2) + 1) / 2  # Generate the minor ticks
        ticks.append((0.5, minor_ticks))  # Add the minor ticks to the ticks
        return ticks  # Return the ticks

    def tickStrings(self, values, scale, spacing):  # Get the tick strings
        strings = []  # Initialize the strings
        for tick_value in values:  # For each tick value
            index = int(tick_value)  # Get the index
            if 0 <= index < len(self.layers) and tick_value % 1 == 0.5:  # If the index is valid and the tick value is a half integer
                strings.append(self.layers[index])  # Add the layer name to the strings
            else:  # Otherwise
                strings.append("")  # Add an empty string to the strings
        return strings  # Return the strings


class SongSelectWidget(QWidget):  # Widget for song selection
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()  # Initialize the widget

    def initialize(self):  # Initialize the widget
        self.layout = QHBoxLayout(self)  # Set the layout to horizontal box layout
        self.label = QLabel(f"Select Song")  # Label for song selection
        self.add_new_song = QPushButton("Add New Song", self)  # Button for adding a new song
        self.song_selector = QComboBox(self)  # Combo box for selecting a song

        # Place the child widgets within the SongSelectWidget layout
        self.layout.addWidget(self.label)  # Add the label to the layout
        self.layout.addWidget(self.add_new_song)  # Add the add new song button to the layout
        self.layout.addWidget(self.song_selector)  # Add the song selector to the layout


class SongOverviewWidget(QWidget):  # Widget for displaying song overview
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initWidget()  # Initialize the widget

    def initWidget(self):  # Initialize the widget
        self.layout = QVBoxLayout(self)  # Set the layout to vertical box layout
        self.layout.setContentsMargins(0, 0, 12, 0)  # Set the margins for the layout
        self.label = QLabel(f"Song Overview")  # Label for the song overview

    def initWidget(self):
        self.layout = QVBoxLayout(self)  # Set the layout to vertical box layout
        self.layout.setContentsMargins(0, 0, 12, 0)  # Set the margins for the layout
        self.label = QLabel(f"Song Overview")  # Label for the song overview

        self.song_plot = pg.PlotWidget()  # Create a plot widget for the song

        self.song_plot.setFixedHeight(100)  # Set the fixed height of the song plot
        self.song_plot.setContentsMargins(0, 0, 0, 0)  # Set the margins for the song plot

        self.song_plot.showGrid(x=True, y=False, alpha=1)  # Show the grid for the song plot

        self.layout.addWidget(self.label)  # Add the label to the layout
        self.layout.addWidget(self.song_plot)  # Add the song plot to the layout

    def init_playhead(self):
        line_specs = mkPen(color="w", width=2)  # Define the specifications for the line
        self.playhead = InfiniteLine(angle=90, movable=True, pen=line_specs)  # Create an infinite line
        self.song_plot.addItem(self.playhead)  # Add the line to the song plot
    
    def paint_beat_line(self, frame_number):
        line_specs = mkPen(color="b", width=1)  # Define the specifications for the line
        beat_line = InfiniteLine(angle=90, movable=False, pen=line_specs)  # Create an infinite line for beat
        beat_line.setPos(frame_number)  # Set the position of the line at specific tick number
        beat_line.beat = True  # Mark this line as a beat line
        self.song_plot.addItem(beat_line)  # Add the beat line to the song plot
   
    def remove_beat_lines(self):
        for item in self.song_plot.items():
            if isinstance(item, InfiniteLine) and getattr(item, 'beat', False):
                self.song_plot.removeItem(item)  # Remove the beat line from the song plot


    def plot_events(self, ticks, song_data):
        self.song_plot.setLimits(  # Set the limits for the song plot
            xMin=0,
            xMax=ticks[-1],
            yMin=0,
            yMax=1,
            minYRange=1,
            maxYRange=1,
        )
        self.song_plot.plot(ticks, song_data)  # Plot the song data

        y_axis = self.song_plot.getAxis("left")  # Get the y-axis
        y_axis.setTicks([])  # Set the ticks for the y-axis

    def update_plot(self, ticks, song_data):
        # logic to update plot
        self.song_plot.clear()  # Clear the song plot
        self.plot_events(ticks, song_data)  # Plot the events

# Class to encapsulate any dialog/popup window for prompting user interaction
class DialogWindow:
    # Prompt user to select a file to open
    def open_file(title, dir, filter):
        options = QFileDialog.Options()  # Define the options for the file dialog
        file_path, _ = QFileDialog.getOpenFileName(  # Get the open file name
            None,
            title,
            dir,
            filter,
            options=options,
        )
        return file_path  # Return the file path

    # Prompt user to select file save name/path
    def save_file(title, dir, filter):
        options = QFileDialog.Options()  # Define the options for the file dialog
        file_path, _ = QFileDialog.getSaveFileName(  # Get the save file name
            None,
            title,
            dir,
            filter,
            options=options,
        )
        return file_path  # Return the file path

    # Prompt user to input text
    def input_text(title, label):
        name, ok = QInputDialog.getText(None, title, label)  # Get the text input from the user
        if ok:  # If the input is valid
            return name  # Return the name

    def error(message):
        msg = QMessageBox()  # Create a message box
        msg.setIcon(QMessageBox.Critical)  # Set the icon to critical
        msg.setText("Error")  # Set the text to "Error"
        msg.setInformativeText(message)  # Set the informative text to the message
        msg.setWindowTitle("Error")  # Set the window title to "Error"
        msg.exec_()  # Execute the message box
