from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QLabel,  # For displaying text or images
    QVBoxLayout,  # Box layout with a vertical direction
    QPushButton,  # Command button
)


class LocalWindow(QWidget):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.setWindowTitle("Graphs")
        self.initialize()

    def initialize(self):
        self.layout = QVBoxLayout(self)

        self.count_button = QPushButton("Count", self)
        self.add_events_to_layer_button = QPushButton("Add BPM events to layer", self)
        self.bpm_label = QLabel("BPM", self)
        self.bpm_label.setStyleSheet("font-size: 24pt")

        self.layout.addWidget(self.bpm_label)
        self.layout.addWidget(self.count_button)
        self.layout.addWidget(self.add_events_to_layer_button)

    def open(self):
        self.show()
