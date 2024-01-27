import importlib
import os
from PluginInterface import PluginInterface
import sys


class PluginModel:
    def __init__(self):
        self.plugins = {}

    def load_plugins(self, main_controller):
        self.loader = PluginLoader("plugins", main_controller)
        self.loader.load_plugins()
        self.plugins = self.loader.plugins

        for plugin in self.plugins.values():
            plugin.load()

    def reload_plugins(self):
        self.unload_plugins()
        self.load_plugins()

    def unload_plugins(self):
        for plugin in self.plugins.values():
            plugin.unload()

    def execute_plugin(self, plugin_name):
        if plugin_name in self.plugins:
            self.plugins[plugin_name].execute()

    def init_plugins(self, main_controller):
        self.main_controller = main_controller


class PluginLoader:
    def __init__(self, plugin_directory, main_controller):
        self.plugins = {}
        self.plugin_directory = plugin_directory
        self.main_controller = main_controller

    def load_plugins(self):
        # Add the plugin directory to the Python path
        plugin_path = os.path.abspath(self.plugin_directory)
        if plugin_path not in sys.path:
            sys.path.append(plugin_path)

        for item in os.listdir(self.plugin_directory):
            item_path = os.path.join(self.plugin_directory, item)
            if os.path.isdir(item_path):
                # Assuming the initialization file is named 'plugin.py'
                init_file_path = os.path.join(item_path, "plugin.py")
                if os.path.isfile(init_file_path):
                    # Construct the module name
                    module_name = f"{item}.plugin"
                    full_module_name = f"plugins.{module_name}"
                    try:
                        module = importlib.import_module(full_module_name)
                        for attribute_name in dir(module):
                            attribute = getattr(module, attribute_name)
                            if (
                                issubclass(attribute, PluginInterface)
                                and attribute is not PluginInterface
                            ):
                                # Initialize the plugin and store it with the folder name as the key
                                self.plugins[item] = attribute(self.main_controller)
                    except Exception as e:
                        print(f"Failed to load plugin {item}: {e}")
