# StageZeroDocumentation:

Dependencies

    - Python
    - PyQt5
    - librosa
    - numpy
    - pyqtgraph
    - vlc
    - threading

    here are the pip commands you'll need to use:
        pip install 
            librosa
            Pyqtgraph
            Pyqt5
            Pyqt5 - tools
            python-vlc

Modules

    Models
        - MainModel: The main model that holds the project name, song, and stack.
        - SongModel: Manages song item instances.
        - SongItem: Represents a song with attributes like name, path, song data, sample rate, length, and frame quantity.
        - StackModel: Manages the stack of layers.
        - LayerModel: Manages layer item instances and event item instances.
        - EventModel: Represents an event with a name, objects, and plot data item.
        - LayerItem: Represents a layer with a name and an event.
        - EventItem: Represents an event with a name and color.

    Views
        - MainView: The main view that holds the launch window and main window.
        - LaunchWindow: The initial window that allows users to create or load a project.
        - MainWindow: The main window that displays the song selection menu, song overview, audio playback command, layer control, stack, and playback mode.
        - AudioPlaybackCommandWidget: The widget that allows users to control audio playback.
        - PlaybackModeWidget: The widget that allows users to select the playback mode.
        - EventEditorWidget: The widget that allows users to edit events.
        - LayerControlWidget: The widget that allows users to control layers.
        - StackWidget: The widget that displays the stack of layers.
        - LayerWidget: The widget that displays a layer.
        - CustomAxis: The custom axis for the plot.
        - SongSelectWidget: The widget that allows users to select a song.
        - SongOverviewWidget: The widget that displays an overview of the song.

    Controllers
        - MainController: The main controller that initializes all other controllers.
        - ProjectController: The controller that manages the project.
        - AudioPlaybackController: The controller that manages audio playback.
        - TimeUpdateThread: The thread that updates the time.
        - SongController: The controller that manages the song.
        - StackController: The controller that manages the stack.
        - LayerController: The controller that manages the layers.
        - EventController: The controller that manages the events.
        - SongSelectController: The controller that manages song selection.
        - SongOverviewController: The controller that manages the song overview.
        - PlaybackModeController: The controller that manages the playback mode.

    Utility
        DialogWindow
            This class encapsulates any dialog/popup window for prompting user interaction. It includes methods for opening a file, saving a file, inputting text, and displaying an error message.
