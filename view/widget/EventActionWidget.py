from PyQt5.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class EventActionWidget(QDockWidget):
    def __init__(self,title="Event Actions", parent=None):
        super().__init__(title, parent)
        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.widget = QWidget()
        self.setWidget(self.widget)
        self.initialize()


    def initialize(self):
        # Initialize the main layout for this widget
        self.main_layout = QVBoxLayout(self.widget)
        self.main_layout.setSpacing(5)  # Set spacing between elements

        # Create action buttons
        self.create_delete_button()
        self.create_nudge_buttons()
        self.create_change_layer_button()
        self.main_layout.addStretch(1) # add a space so add event is at the bottom
        self.create_add_event_button()

    def create_delete_button(self):
        # Create a button for the action
        self.delete_button = QPushButton("Delete")
        self.main_layout.addWidget(self.delete_button)

    def create_change_layer_button(self):
        # Create a button for the action
        self.change_layer_button = QPushButton("Change Layer")
        self.main_layout.addWidget(self.change_layer_button)

    def create_nudge_buttons(self):
        # Create a horizontal layout for the nudge buttons
        self.nudge_layout = QHBoxLayout()

        # Create nudge -1 and nudge +1 buttons
        self.nudge_minus_button = QPushButton("Nudge -1")
        self.nudge_plus_button = QPushButton("Nudge +1")
        self.nudge_layout.addWidget(self.nudge_minus_button)
        self.nudge_layout.addWidget(self.nudge_plus_button)

        # Add the nudge layout to the main layout
        self.main_layout.addLayout(self.nudge_layout)

    def create_add_event_button(self):
        self.create_event_button = QPushButton("Add")
        self.main_layout.addWidget(self.create_event_button)