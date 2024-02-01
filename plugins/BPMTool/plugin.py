from PluginInterface import PluginInterface
from .LocalController import LocalController
from .LocalWindow import LocalWindow

"""
    All of the plugins outward facing methods should be built out here as this is the top layer of the local plugin
"""

PLUGIN_NAME = "BPMTool"

class BPMTool(PluginInterface):
    def __init__(self):
        super().__init__()
        self.local_controller = None
        self.main_controller = None

    def execute(self):
        # Implement the method
        pass

    def load(self, main_controller):
        self.local_controller = LocalController(LocalWindow(), main_controller)
        self.main_controller = main_controller
        print(f"TestPlugin Loaded")

    def unload(self):
        self.local_controller = None
        self.main_controller = None

    def open(self):
        print(f"Opening {PLUGIN_NAME}'s main window")
        self.local_controller.open()
