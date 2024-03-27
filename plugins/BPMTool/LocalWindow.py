from PyQt5.QtWidgets import (
    QWidget,  # Base class for all user interface objects
    QLabel,  # For displaying text or images
    QVBoxLayout,  # Box layout with a vertical direction
    QPushButton,  # Command button
)

from PyQt5.QtWidgets import QComboBox, QLineEdit, QColorDialog
from PyQt5.QtCore import pyqtSignal

class LocalWindow(QWidget):
    add_to_layer_signal = pyqtSignal(str,str)
    add_to_song_signal = pyqtSignal(str,str)
    remove_from_song_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.setWindowTitle("Graphs")
        self.initialize()

    def initialize(self):
        self.layout = QVBoxLayout(self)

        self.bpm_label = QLabel("BPM", self)
        self.bpm_label.setStyleSheet("font-size: 24pt")
        self.color_line_edit = QLineEdit(self)
        self.color_line_edit.setPlaceholderText("Click to select color")
        self.color_line_edit.mousePressEvent = self.on_color_line_edit_click

        self.count_button = QPushButton("Count", self)
        self.add_to_layer_button = QPushButton("Add events to layer", self)    
        self.add_beat_lines_button = QPushButton("Add lines to song overview", self)
        self.remove_beat_lines_button = QPushButton("Remove lines to song overview", self)

        self.layout.addWidget(self.bpm_label)
        self.layout.addWidget(self.count_button)

        self.layout.addWidget(self.color_line_edit)
        self.layout.addWidget(self.add_to_layer_button)
        self.layout.addWidget(self.add_beat_lines_button)
        self.layout.addWidget(self.remove_beat_lines_button)

        self.add_to_layer_button.clicked.connect(self.emit_add_to_layer_signal)
        self.add_beat_lines_button.clicked.connect(self.emit_add_beat_lines_signal)
        self.remove_beat_lines_button.clicked.connect(self.emit_remove_beat_lines_signal)

    def emit_add_to_layer_signal(self):
        color = self.color_line_edit.text()
        event_type = "bpm"
        self.add_to_layer_signal.emit(color, event_type)

    def emit_add_beat_lines_signal(self):
        color = self.color_line_edit.text()
        line_type = "bpm"
        self.add_to_song_signal.emit(color, line_type)

    def emit_remove_beat_lines_signal(self):
        color = self.color_line_edit.text()
        line_type = "bpm"
        self.remove_from_song_signal.emit(line_type)

    def on_color_line_edit_click(self, event):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_line_edit.setText(color.name())
            self.color_line_edit.setStyleSheet(f"background-color: {color.name()}")

    def open(self):
        self.show()
