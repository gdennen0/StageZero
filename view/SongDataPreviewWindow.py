from PyQt5.QtWidgets import QWidget, QVBoxLayout
from pyqtgraph import PlotWidget

class SongDataPreviewWindow(QWidget):
    def __init__(self, parent=None):
        super(SongDataPreviewWindow, self).__init__(parent)
        self.song_data = None
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Song Data Preview')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.plot_widget = PlotWidget()
        self.layout.addWidget(self.plot_widget)


    def open(self, song_data, axis_data):
        self.plot_widget.clear()
        # self.plot_widget.setLimits(  # Set the limits for the song plot
        #     xMin=0,
        #     xMax=axis_data[-1],
        #     yMin=0,
        #     yMax=1,
        #     minYRange=1,
        #     maxYRange=1,
        # )
        # song_data = song_data[:len(axis_data)]
        self.plot_widget.plot(song_data)
        self.show()