import numpy as np
from pyqtgraph import PlotCurveItem
from constants import SONG_PLOT_RESOLUTION

class WaveformPlotItem(PlotCurveItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def set_waveform_data(self, ticks, song_data):
        adjusted_ticks, adjusted_song_data = self.adjust_resolution(ticks, song_data)
        self.setData(
            x=adjusted_ticks, 
            y=adjusted_song_data, 
            pen=('w'),
            shadowPen=None,
            fillLevel=.50,
            fillOutline=None,
            brush=None,
            # antialias=
            stepMode=None,
            connect='all',
            # compositionMode=
            skipFiniteCheck=False,
            )  # Size of the area under the curve (if applicable)

    def adjust_resolution(self, ticks, song_data):
        print(f"[WaveformPlotItem][adjust_resolution] | Adjusting song waveform plot resolution to {SONG_PLOT_RESOLUTION}%")
        resolution_factor = SONG_PLOT_RESOLUTION / 100
        adjusted_length = int(len(song_data) * resolution_factor)
        adjusted_ticks = np.linspace(ticks[0], ticks[-1], adjusted_length)
        adjusted_song_data = np.interp(adjusted_ticks, ticks, song_data)
        return adjusted_ticks, adjusted_song_data

