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
        - MainModel: The main model that holds the project name, song, and stack instances. Essentially the parent class for all of the model subclasses
            - song is an instance of the SongModel class
            - stack is an instance of the StackModel class

        - SongModel: Manages song item instances.
            - SongItem: Represents a song with attributes like name, path, song data, sample rate, length, and frame quantity.
       
        - StackModel: Manages the stack of layers.
            - LayerModel: Manages layer item instances and event item instances.
                - LayerItem: Represents a layer with a name and an event. Holds an instance of EventModel.
                    - EventModel: Manages Event Item objects, and handles prep/storage of the plot data item.
                        - EventItem: Represents a single event with a name and color.

    Views
        - MainView: The main view that holds the launch window and main window. Parent to all windows.      

            - LaunchWindow: The initial window that allows users to create or load a project.        
            - MainWindow: The main window that displays the song selection menu, song overview, audio playback command, layer control, stack, and playback mode.
                - SongSelectWidget: The widget that allows users to select a song.
                - SongOverviewWidget: The widget that displays an overview of the song.
                - PlaybackModeWidget: The widget that allows users to select the playback mode.
                - AudioPlaybackCommandWidget: The widget that allows users to control audio playback.
                - LayerControlWidget: The widget that allows users to control layers.
                - StackWidget: The widget that displays the stack of layers.
                    - Hold the Scroll area for the LayerWidget
                        - LayerWidget: The widget that displays the layer_plot
            
            Auxillary:
            - EventEditorWidget: The popup widget that allows users to edit events.
            - CustomAxis: The custom axis for the layerWidget plot, eventually expand this to SongOverviewPlot as well

    Controllers
        - MainController: The main controller that initializes all other controllers. This is the central point for data flow in the program. 
            - ProjectController: The controller that manages the project.
            - AudioPlaybackController: The controller that manages audio playback & Stopping/Starting of the clock.
            - SongController: The controller that manages the SongModel instance.
            - StackController: The controller that manages the StackModel instance.
            - LayerController: The controller that manages the LayerModel instance.
            - EventController: The controller that manages the EventItem instances.

            Widget Controllers:
            - SongSelectController: The controller that manages the data/logic behind the SongSelectWidget.
            - SongOverviewController: The controller that manages the data/logic behind the SongOverviewWidget.
            - PlaybackModeController: The controller that manages the data/logic behind the PlaybackModeWidget.

        Misc:
            - TimeUpdateThread: The thread that updates the time and emits signals. 
    Utility
        DialogWindow
            This class encapsulates any dialog/popup window for prompting user interaction. It includes methods for opening a file, saving a file, inputting text, and displaying an error message.
