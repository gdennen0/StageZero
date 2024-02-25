from abc import ABC, abstractmethod


class PluginInterface(ABC):
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def unload(self):
        pass
