from PluginInterface import PluginInterface
from .LocalController import LocalController
from .LocalWindow import LocalWindow


class TestPlugin(PluginInterface):
    def __init__(self, main_controller):
        super().__init__()
        self.local_controller = LocalController(LocalWindow(), main_controller)
        self.main_controller = main_controller
        print(f"initializing TestPlugin")

    def execute(self):
        # Implement the method
        pass

    def load(self):
        print(f"TestPlugin Loaded")

        # Implement the method
        pass

    def unload(self):
        # Implement the method
        pass

    def open(self):
        print(f"test plugin open")
        self.local_controller.open()
