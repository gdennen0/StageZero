from PyQt5.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from .EventPropertiesWidget import EventPropertiesWidget

class SidebarWidget(QDockWidget):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        self.setMinimumWidth(250)
        self.setMaximumWidth(350)
        self.initialize()

    def initialize(self):
        # Initialize the main widget and layout for this dock widget
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        # Create the first section as a dock widget
        self.first_section_dock = QDockWidget("First Section", self)
        self.first_section_dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        first_section_widget = EventPropertiesWidget()
        self.first_section_dock.setWidget(first_section_widget)

        # Create the second section as a dock widget
        self.second_section_dock = QDockWidget("Second Section", self)
        self.second_section_dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        second_section_widget = QWidget()
        second_section_layout = QVBoxLayout(second_section_widget)
        second_section_layout.addWidget(QLabel("Content of the second section"))
        self.second_section_dock.setWidget(second_section_widget)

        # Add the dock widgets to the main window or parent widget
        if self.parent():
            self.parent().addDockWidget(Qt.RightDockWidgetArea, self.first_section_dock)
            self.parent().addDockWidget(Qt.RightDockWidgetArea, self.second_section_dock)

        # Add a placeholder widget to this dock widget to maintain structure
        self.setWidget(self.main_widget)