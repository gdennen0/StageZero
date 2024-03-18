from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QDockWidget
from PyQt5.QtCore import Qt

class EventToolsWidget(QDockWidget):
    def __init__(self, title="Event Properties", parent=None):
        super().__init__(title, parent)
        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.widget = QWidget()
        self.setWidget(self.widget)
        self.initialize()
        self.topLevelChanged.connect(self.collapseDockWidget)

    def initialize(self):
        # Initialize the main layout for this widget
        self.main_layout = QVBoxLayout(self.widget)
        self.main_layout.setSpacing(5)  # Set spacing between buttons

        # Create action buttons
        self.create_action_button("Delete")
        self.create_nudge_buttons()
        self.create_action_button("Change Layer")

        # Add a stretch below the last button
        self.main_layout.addStretch(1)

    def create_action_button(self, action_name):
        # Create a button for the action
        action_button = QPushButton(action_name)
        self.main_layout.addWidget(action_button)

    def create_nudge_buttons(self):
        # Create a horizontal layout for the nudge buttons
        nudge_layout = QHBoxLayout()

        # Create nudge -1 and nudge +1 buttons
        nudge_minus_button = QPushButton("Nudge -1")
        nudge_plus_button = QPushButton("Nudge +1")
        nudge_layout.addWidget(nudge_minus_button)
        nudge_layout.addWidget(nudge_plus_button)

        # Add the nudge layout to the main layout
        self.main_layout.addLayout(nudge_layout)

    def collapseDockWidget(self, topLevel):
        if topLevel:
            self.setFeatures(QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetFloatable)
        else:
            self.setFeatures(QDockWidget.AllDockWidgetFeatures)