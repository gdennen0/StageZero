from PluginInterface import PluginInterface
from .LocalController import LocalController
from .LocalWindow import LocalWindow


PLUGIN_NAME = "NodeReformer"


class NodeReformer(PluginInterface):
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
