from PyQt5.QtWidgets import QAction


class ViewMenu:
    def __init__(self, main_menu):
        self.view_menu = main_menu.addMenu("&View")
        self.create_actions(main_menu)

    def create_actions(self, main_menu):
        self.plugin_action = QAction("&Plugin", main_menu)
        self.view_menu.addAction(self.plugin_action)
