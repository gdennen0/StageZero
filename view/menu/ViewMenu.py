from PyQt5.QtWidgets import QAction


class ViewMenu:
    def __init__(self, main_menu):
        self.view_menu = main_menu.addMenu("&View")
        self.create_actions(main_menu)

    def create_actions(self, main_menu):
        self.tools_action = QAction("&Tools", main_menu)
        self.graphs_action = QAction("&Graphs", main_menu)

        self.view_menu.addAction(self.tools_action)
        self.view_menu.addAction(self.graphs_action)
