from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from pyqtgraph import PlotWidget, AxisItem, InfiniteLine, mkPen


class SongDataPreviewWindow(QWidget):
    window_closed = pyqtSignal()  # Define the signal

    def __init__(self, parent=None):
        super(SongDataPreviewWindow, self).__init__(parent)
        self.song_data = None
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle("Song Data Preview")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.plot_widget = PlotWidget()
        self.layout.addWidget(self.plot_widget)

    def open(self, song_data, axis_data):
        self.plot_widget.plot(axis_data, song_data)
        self.plot_widget.setLimits(  # Set the limits for the song plot
            xMin=0,
            xMax=axis_data[-1],
            yMin=0,
            yMax=1,
            minYRange=1,
            maxYRange=1,
        )

        # Create audio player controls
        self.play_button = QPushButton("Play", self)
        self.pause_button = QPushButton("Pause", self)
        self.reset_button = QPushButton("Reset", self)

        # Add buttons to layout
        self.layout.addWidget(self.play_button)
        self.layout.addWidget(self.pause_button)
        self.layout.addWidget(self.reset_button)

        self.show()

    def init_playhead(self):
        line_specs = mkPen(color="w", width=2)  # Define the specifications for the line
        self.playhead = InfiniteLine(
            angle=90, movable=True, pen=line_specs
        )  # Create an infinite line
        self.plot_widget.addItem(self.playhead)  # Add the line to the song plot

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
