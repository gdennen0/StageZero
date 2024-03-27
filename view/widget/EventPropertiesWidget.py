from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDockWidget, QColorDialog
from PyQt5.QtCore import Qt, pyqtSignal

class EventPropertiesWidget(QDockWidget):
    sigUpdateColor = pyqtSignal(str)

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
        self.line_items["Layer"] = self.create_property_field("Layer", editable=False)
        self.line_items["Frame"] = self.create_property_field("Frame", editable=False)

        # Add a stretch below the last element
        self.main_layout.addStretch(1)

        self.line_items["Color"].mousePressEvent = self.open_color_dialog

    def create_property_field(self, property_name, editable=True):
        property_layout = QHBoxLayout()
        property_label = QLabel(property_name)
        property_layout.addWidget(property_label)
        property_edit = QLineEdit()
        if not editable:
            property_edit.setReadOnly(True)
        property_layout.addWidget(property_edit)
        self.main_layout.addLayout(property_layout)

        return property_edit
    
    def update(self, event_item):
        # Update the line items with the properties of the LayerPlotItem instance
        self.line_items["Name"].setText(event_item.event_name)
        self.line_items["Color"].setText(str(event_item.color))
        self.line_items["Layer"].setText(event_item.parent_layer_name)
        self.line_items["Frame"].setText(str(event_item.frame_number))

    def open_color_dialog(self, event):  # Open the color dialog
        # Open the color dialog and get the selected color
        color = QColorDialog.getColor()
        # If a color was selected (the user didn't cancel the dialog), update the QLineEdit with the selected color
        if color.isValid():
            self.line_items["Color"].setText(color.name())
            new_color = color.name()
            self.sigUpdateColor.emit(new_color)