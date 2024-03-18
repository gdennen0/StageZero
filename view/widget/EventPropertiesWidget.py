from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDockWidget
from PyQt5.QtCore import Qt

class EventPropertiesWidget(QDockWidget):
    def __init__(self, title="Event Properties", parent=None):
        super().__init__(title, parent)
        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.widget = QWidget()
        self.setWidget(self.widget)
        self.line_items = {}
        self.initialize()

    def initialize(self):
        # Initialize the main layout for this widget
        self.main_layout = QVBoxLayout(self.widget)
        self.main_layout.setSpacing(5)  # Set spacing between elements

        # Create property fields
        self.line_items["Name"] = self.create_property_field("Name")
        self.line_items["Color"] = self.create_property_field("Color")
        self.line_items["Layer"] = self.create_property_field("Layer")
        self.line_items["Frame"] = self.create_property_field("Frame")

        # Add a stretch below the last element
        self.main_layout.addStretch(1)

    def create_property_field(self, property_name):
        # Create a horizontal layout for the property
        property_layout = QHBoxLayout()

        # Create a label for the property
        property_label = QLabel(property_name)
        property_layout.addWidget(property_label)

        # Create an editable line item for the property
        property_edit = QLineEdit()
        property_layout.addWidget(property_edit)

        # Add the property layout to the main layout
        self.main_layout.addLayout(property_layout)

        return property_edit


    def update(self, event_item):
        # Update the line items with the properties of the LayerPlotItem instance
        self.line_items["Name"].setText(event_item.name)
        self.line_items["Color"].setText(str(event_item.color))
        self.line_items["Layer"].setText(event_item.parent_layer)
        self.line_items["Frame"].setText(str(event_item.frame_number))

    