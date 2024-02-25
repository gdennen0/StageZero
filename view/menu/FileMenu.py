from PyQt5.QtWidgets import QAction


class FileMenu:
    def __init__(self, main_menu):
        self.file_menu = main_menu.addMenu("&File")
        self.create_actions(main_menu)

    def create_actions(self, main_menu):
        self.save_action = QAction("&Save", main_menu)
        self.save_as_action = QAction("&Save as", main_menu)
        self.load_action = QAction("Load", main_menu)
        self.exit_action = QAction("&Exit", main_menu)

        self.save_action.setShortcut("Ctrl+S")
        self.exit_action.setShortcut("Ctrl+Q")

        self.file_menu.addAction(self.save_as_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.exit_action)
        self.file_menu.addAction(self.load_action)
