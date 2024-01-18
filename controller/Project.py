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

        self.view.open_main_window()  # Opening the main window with the project name

    def load_project(self):
        # functions to load the project file
        print(f"Begin Loading Project")

