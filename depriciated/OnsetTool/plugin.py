from PluginInterface import PluginInterface
from .LocalController import LocalController
from .LocalWindow import LocalWindow

"""
    Here should be the main controller for your plugin. The file name must be plugin.py for now TODO: make this read the file name 
    
    All of the plugins outward facing methods should be built out here as this is the top layer of the local plugin
"""

PLUGIN_NAME = "OnsetTool"


class OnsetTool(PluginInterface):
    def __init__(self):
        super().__init__()
        self.local_controller = None
        self.main_controller = None

    def load(self, main_controller):
        self.local_controller = LocalController(LocalWindow(), main_controller)
        self.main_controller = main_controller
        print(f"{PLUGIN_NAME} Loaded")

    def unload(self):
        self.local_controller = None
        self.main_controller = None

    def open(self):
        print(f"Opening {PLUGIN_NAME}'s main window")
        self.local_controller.open()
