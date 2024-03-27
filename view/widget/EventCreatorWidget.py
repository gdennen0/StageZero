from PyQt5.QtWidgets import (
    QDialog,  # Dialog window
    QLineEdit,  # One-line text editor
    QColorDialog,  # Dialog widget for specifying colors
    QPushButton,  # Command button
    QVBoxLayout,  # Box layout with a vertical direction
    QLabel,  # Label widget
    QHBoxLayout,  # Box layout with a horizontal direction
)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QCheckBox, QComboBox

class EventCreatorWidget(QDialog):  # Widget for editing events
    changes_saved = pyqtSignal(object)

    def __init__(self, layers):
        super().__init__()  # Call the constructor of the parent class
        self.layout = QVBoxLayout(self)  # Set the layout to vertical box layout
        self.layers = layers

        # Name editor setup
        self.name_layout = QHBoxLayout()
        self.name_label = QLabel("Name:", self)
        self.name = QLineEdit("Default", self)
        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.name)

        self.layer_layout = QHBoxLayout()
        self.layer_label = QLabel("Layer:", self)
        self.layer = QComboBox(self)
        self.layer.addItems(self.layers)
        self.layer_layout.addWidget(self.layer_label)
        self.layer_layout.addWidget(self.layer)

        # Frame number setup
        self.frame_number_layout = QHBoxLayout()
        self.frame_number_label = QLabel("Frame Number:", self)
        self.frame_number = QLineEdit("1", self)
        self.frame_number_layout.addWidget(self.frame_number_label)
        self.frame_number_layout.addWidget(self.frame_number)
        
        # Color editor setup
        self.color_layout = QHBoxLayout()
        self.color_label = QLabel("Color:", self)
        self.color = QLineEdit("#ffffff", self)
        self.color.mousePressEvent = self.open_color_dialog
        self.color_layout.addWidget(self.color_label)
        self.color_layout.addWidget(self.color)
        
        # Multiple events checkbox setup
        self.multiple_events_layout = QHBoxLayout()
        self.multiple_events_checkbox = QCheckBox("Add multiple events", self)
        self.multiple_events_checkbox.stateChanged.connect(self.toggle_event_details_editability)
        self.multiple_events_layout.addWidget(self.multiple_events_checkbox)
        
        # Event quantity setup
        self.event_qty_layout = QHBoxLayout()
        self.event_qty_label = QLabel("Event Quantity:", self)
        self.event_qty = QLineEdit("1", self)
        self.event_qty.setReadOnly(True)  # Initially set to read-only
        self.event_qty_layout.addWidget(self.event_qty_label)
        self.event_qty_layout.addWidget(self.event_qty)
        
        # Event spacing setup
        self.event_spacing_layout = QHBoxLayout()
        self.event_spacing_label = QLabel("Event Spacing:", self)
        self.event_spacing = QLineEdit("1", self)
        self.event_spacing.setReadOnly(True)  # Initially set to read-only
        self.event_spacing_layout.addWidget(self.event_spacing_label)
        self.event_spacing_layout.addWidget(self.event_spacing)
        
        # Create events button setup
        self.create_events = QPushButton("Create Event(s)")
        self.create_events.clicked.connect(self.emit_changes_saved)

        # Adding layouts to the main layout
        self.layout.addLayout(self.name_layout)
        self.layout.addLayout(self.layer_layout)
        self.layout.addLayout(self.frame_number_layout)
        self.layout.addLayout(self.color_layout)
        self.layout.addLayout(self.multiple_events_layout)
        self.layout.addLayout(self.event_qty_layout)
        self.layout.addLayout(self.event_spacing_layout)
        self.layout.addWidget(self.create_events)  

    def open_color_dialog(self, event):  # Open the color dialog
        # Open the color dialog and get the selected color
        color = QColorDialog.getColor()
        # If a color was selected (the user didn't cancel the dialog), update the QLineEdit with the selected color
        if color.isValid():
            self.color.setText(color.name())

    def toggle_event_details_editability(self):
        # Toggle the editability of event quantity and spacing based on the checkbox state
        is_checked = self.multiple_events_checkbox.isChecked()
        self.event_qty.setReadOnly(not is_checked)
        self.event_spacing.setReadOnly(not is_checked)

    def package_data(self):
        event_data = {
            "frame_number": int(self.frame_number.text()),
            "parent_layer_name": str(self.layer.currentText()), 
            "event_name": str(self.name.text()),
            "event_color": str(self.color.text()),
            "event_qty": int(self.event_qty.text()),
            "event_spacing": int(self.event_spacing.text()),
        }
        return event_data

    def emit_changes_saved(self):
        # Package the data
        packaged_data = self.package_data()
        # Emit the changes_saved signal with the packaged data
        self.changes_saved.emit(packaged_data)

    # def validate_and_create_events(self):
    #     # Validate inputs
    #     if not self.name.text().strip():
    #         QMessageBox.warning(self, "Input Error", "Name cannot be empty.")
    #         return
    #     if not self.frame_number.text().isdigit():
    #         QMessageBox.warning(self, "Input Error", "Frame Number must be an integer.")
    #         return
    #     if not QColor(self.color.text()).isValid():
    #         QMessageBox.warning(self, "Input Error", "Invalid color input.")
    #         return
    #     if self.multiple_events_checkbox.isChecked():
    #         if not self.event_qty.text().isdigit() or not self.event_spacing.text().isdigit():
    #             QMessageBox.warning(self, "Input Error", "Event Quantity and Event Spacing must be integers.")
    #             return
    #     # Proceed to create events with validated inputs
    #     self.create_events_with_validated_inputs()

    # def create_events_with_validated_inputs(self):
    #     # Logic to create events with validated inputs goes here
    #     pass

