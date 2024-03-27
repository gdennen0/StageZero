from PyQt5.QtCore import QObject, pyqtSignal

class PlayheadController:
    sigPlayheadPosChange = pyqtSignal(int)

    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.view = main_controller.view
        self.model = main_controller.model
        self.song_overview_widget = (main_controller.view.main_window.stage_widget.song_overview)
        self.add_song_playhead_to_plot()
        self.connect_song_playhead()

    def add_song_playhead_to_plot(self):
        self.song_overview_widget.add_playhead(self.model.song.playhead)

    def connect_song_playhead(self):
        self.model.song.playhead.sigPositionChangeFinished.connect(self.on_pos_change)
        self.model.stack.playhead.sigPositionChangeFinished.connect(self.on_pos_change)

    def on_pos_change(self, playhead):
        rounded_playhead_position = int(playhead.value())
        self.update_playhead_location(rounded_playhead_position)
        self.main_controller.audio_playback_controller.goto(rounded_playhead_position)
        print(f"[PlayheadController][on_pos_change] | Position changed to '{rounded_playhead_position}")

    def update_playhead_location(self, location):
        self.model.song.playhead.setPos(location)
        self.model.stack.playhead.setPos(location)
        pass


