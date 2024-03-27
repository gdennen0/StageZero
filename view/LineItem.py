from pyqtgraph import InfiniteLine, mkPen

class LineItem(InfiniteLine):
    def __init__(self):
        self.frame_number = None
        self.type = None
        super().__init__(angle=90, movable=False, pen=mkPen(color="w", width=2))

    def set_frame_number(self, frame_number):
        self.frame_number = frame_number
        self.setPos((frame_number, 0))

    def set_color(self, color):
        self.setPen(mkPen(color=color, width=2))

    def set_type(self, type):
        self.type = type
