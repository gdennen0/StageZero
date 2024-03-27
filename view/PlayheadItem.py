from pyqtgraph import InfiniteLine, mkPen
from PyQt5.QtCore import pyqtSignal

class PlayheadItem(InfiniteLine):
    # sigPositionChanged = pyqtSignal(float)  # Signal to emit the new position

    def __init__(self):
        super().__init__(angle=90, movable=True, pen=mkPen(color="w", width=2))
    #     self.sigPositionChangeFinished.connect(self.emitPositionChanged)

    # def emitPositionChanged(self):
    #     self.sigPositionChanged.emit(self.value())
    
