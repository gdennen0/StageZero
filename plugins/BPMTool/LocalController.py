import tools


class LocalController:
    def __init__(self, local_view, main_controller):
        self.local_view = local_view
        self.main_controller = main_controller
        self.stack = main_controller.model.stack
        self.model = main_controller.model
        self.view = main_controller.view
        self.init_connections()

    def init_connections(self):
        self.local_view.count_button.clicked.connect(self.estimate_bpm)
        self.local_view.paint_to_song_overview_button.clicked.connect(
            self.add_beats_to_song_overview
        )
        self.local_view.remove_from_song_overview_button.clicked.connect(
            self.remove_beats_from_song_overview
        )

    def open(self):
        self.local_view.open()

    def estimate_bpm(self):
        song_object = self.model.loaded_song
        tempo, beats = tools.estimate_bpm(song_object)
        # tempo is returned as a float
        # beats is returned as an np.ndarray

        self.update_time_label(int(tempo))

    def update_time_label(self, bpm):
        # Update the time label
        bpm_label_string = f"Tempo: {bpm}"
        # print(bpm_label_string)

        self.local_view.bpm_label.setText(bpm_label_string)

    def add_beats_to_song_overview(self):
        song_object = self.model.loaded_song
        _, beats = tools.estimate_bpm(song_object)
        self.main_controller.song_overview_controller.paint_beat_lines(beats)

    def remove_beats_from_song_overview(self):
        self.main_controller.song_overview_controller.remove_beat_lines()
