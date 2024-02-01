import os


class PluginWindowController:
    def __init__(self, main_controller):
        self.view = main_controller.view.plugins_window
        self.model = main_controller.model
        self.init_connections()
        self.refresh_plugins()  # Initial refresh when the controller is created

    def init_connections(self):
        self.view.refresh_button.clicked.connect(self.refresh_plugins)
        self.view.open_button.clicked.connect(self.open_plugin)
        self.view.plugin_list.itemSelectionChanged.connect(self.plugin_selected)

    def plugin_selected(self):
        selected_items = self.view.plugin_list.selectedItems()
        if selected_items:
            plugin_name = selected_items[0].text()
            print(f"Selected plugin: {plugin_name}")
        else:
            print("No plugin selected.")

    def refresh_plugins(self):
        # Clear the current list
        self.view.plugin_list.clear()

        # Fetch and list the plugins
        plugin_dir = os.path.join(os.getcwd(), "plugins")
        if not os.path.exists(plugin_dir):
            os.makedirs(plugin_dir)  # Create the plugins directory if it doesn't exist
        plugins = os.listdir(plugin_dir)

        # Populate the QListWidget with plugin names
        for plugin in plugins:
            self.view.plugin_list.addItem(plugin)

    def open_plugin(self):
        # Get the selected plugin
        selected_items = self.view.plugin_list.selectedItems()
        if selected_items:
            plugin_name = selected_items[0].text().replace(".py", "")
            print(f"Opening plugin: {plugin_name}")
            self.model.plugin.plugins[plugin_name].open()
            # TODO: Implement the logic to open the selected plugin
        else:
            print("No plugin selected.")
