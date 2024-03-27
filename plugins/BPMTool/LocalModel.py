from pyqtgraph import InfiniteLine, mkPen

class LocalModel:
    def __init__(self):
        self.bpm_lines = []


    def add_bpm_line(self, frame_number):
        line = BPMLine()
        line.set_frame_number()
        self.bpm_lines.append(line)
        pass


class BPMLine(InfiniteLine):
    def __init__(self):
        self.frame_number = None
        super().__init__(angle=90, movable=False, pen=mkPen(color="w", width=2))

    def set_frame_number(self, frame_number):
        self.frame_number = frame_number
        self.setPos((frame_number, 0))
