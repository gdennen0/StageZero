"""
Module: ProjectController

This module is responsible for managing the project lifecycle. It includes functionality to create, save, and load projects.
It interacts with the main controller, model, and view to perform these operations. The ProjectController class is the main class in this module.

Arguments:
    main_controller (object): An instance of the main controller. It is used to access the model and view.

Returns:
    None. The class methods perform actions but do not return any value.

"""

from view import DialogWindow
from PopupManager import PopupManager
import os

class ProjectController:
    def __init__(self, main_controller):
        self.model = main_controller.model  # Assign model reference
        self.main_controller = main_controller  # Assign main_controller reference
        self.view = main_controller.view  # Assign view reference
        self.connect_signals()

    def connect_signals(self):
        self.view.launch_window.new_project_button.clicked.connect(self.new_project)  # Connecting the new_project_button click signal to the new_project method
        self.view.launch_window.load_project_button.clicked.connect(self.load_project)  # Connecting the load_project_button click signal to the load_project method

    def new_project(self):
        self.model.project_name = "Untitled"  # Setting the project name in the model
        self.main_controller.open_main_window()

    def load_project(self):
        path = DialogWindow.open_file("Open Location", "saves/")
        if os.path.exists(path):
            pass
        else:
            return
        self.model.load(path)
        print(f"[ProjectController][load_project] | Project Loaded from {path}")
        self.view.open_main_window()
        self.view.close_launch_window()

        self.main_controller.song_controller.initialize()
        self.main_controller.song_overview_controller.refresh()  # Load the song data into the song overview plot
        self.main_controller.layer_controller.refresh()  # initialize the layer widget
        self.main_controller.song_select_controller.refresh()  # Update the song select widget dropdown items

    def save_as(self):
        self.model.save_path = DialogWindow.save_file("Save Location")
        self.model.save()

    def save(self):
        if self.model.save_path is not None:
            self.model.save()

        else:
            PopupManager.show_info("Info", "Project has not been saved yet")
            self.save_as()

    def reload_project(self):
        path = DialogWindow.open_file("Open Location", "saves/")
        self.model.load(path)
        self.main_controller.layer_controller.refresh()
        self.main_controller.song_overview_controller.refresh()
        self.main_controller.audio_playback_controller.refresh()
        self.main_controller.song_select_controller.refresh()  # Update the song select widget dropdown items

        print(f"Project Loaded from {path}")
