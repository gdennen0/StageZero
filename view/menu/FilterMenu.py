from PyQt5.QtWidgets import QAction


class FilterMenu:
    def __init__(self, main_menu):
        self.filter_menu = main_menu.addMenu("&Filter")
        self.create_actions(main_menu)

    def create_actions(self, main_menu):
        self.edit_filters_action = QAction("&Edit Filters", main_menu)
        self.filter_audio_action = QAction("&Filter Audio", main_menu)

        self.filter_menu.addAction(self.edit_filters_action)
        self.filter_menu.addAction(self.filter_audio_action)
