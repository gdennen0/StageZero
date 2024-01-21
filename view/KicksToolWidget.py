from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QLabel,  # For displaying text or images
    QVBoxLayout,  # Box layout with a vertical direction
    QPushButton,
    QListWidget,  # Command button
)

class KicksToolWidget(QWidget):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.initialize()

    def initialize(self):
        self.event_count = 0
        self.layer_selection_popup = QListWidget()
        self.layout = QVBoxLayout(self)    
        # Label / Title
        self.filter_type_label = QLabel("Detect Kick Events")
        self.event_count_label = QLabel(f"{self.event_count} events found")
        # Buttons
        self.process_kick_events_button = QPushButton(f"Process current song")
        self.add_events_to_layer_button = QPushButton(f"Add Kick Events to Layer", self)

        #add to layout
        self.layout.addWidget(self.filter_type_label)
        self.layout.addWidget(self.event_count_label)

        self.layout.addWidget(self.process_kick_events_button)
        self.layout.addWidget(self.add_events_to_layer_button)

    def update_event_count_label(self, event_count):
        # Just sets the label widget text
        self.event_count = event_count
        self.event_count_label.setText(f"{self.event_count} events found")

    def open_layer_selection_popup(self, layer_names):
        # Opens up a popup to select which layer. this will change to its own standard module eventually 
        print("opening layer selection popup")
        self.layer_selection_popup.addItems(layer_names)
        self.layer_selection_popup.setWindowTitle('Select a Layer')
        self.layer_selection_popup.show()
