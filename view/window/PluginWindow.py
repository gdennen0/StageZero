from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QListWidget,
)


class PluginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main layout
        self.layout = QVBoxLayout()

        # Title and Refresh Button
        self.title_layout = QHBoxLayout()
        self.title_label = QLabel("Plugins")
        self.refresh_button = QPushButton("Refresh")
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addWidget(self.refresh_button)
        self.layout.addLayout(self.title_layout)

        # List of plugins
        self.plugin_list = QListWidget()
        self.layout.addWidget(self.plugin_list)

        # Open Button
        self.open_button = QPushButton("Open")
        self.layout.addWidget(self.open_button)

        # Set the layout to the QWidget
        self.setLayout(self.layout)

    def refresh_plugins(self):
        # TODO: Implement the method to refresh the list of plugins
        print("Refreshing plugins...")

    def open_plugin(self):
        # TODO: Implement the method to open the selected plugin
        print("Opening plugin...")

    def open(self):
        self.show()
