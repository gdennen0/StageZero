import tools

class BpmToolController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.stack = main_controller.model.stack
        self.model = main_controller.model
        self.view = main_controller.view
        self.init_connections()

    def init_connections(self):
        self.view.tools_window.bpm.count_button.clicked.connect(self.estimate_bpm)
        self.view.tools_window.bpm.paint_to_song_overview_button.clicked.connect(self.add_beats_to_song_overview)
        self.view.tools_window.bpm.remove_from_song_overview_button.clicked.connect(self.remove_beats_from_song_overview)
    
    def estimate_bpm(self):
        song_object = self.model.loaded_song
        tempo, beats = tools.estimate_bpm(song_object)
        # tempo is returned as a float
        # beats is returned as an np.ndarray

        self.update_time_label(int(tempo))

    def update_time_label(self, bpm):
        # Update the time label
        bpm_tool_widget = self.view.tools_window.bpm

        bpm_label_string = f"Tempo: {bpm}"
        print(bpm_label_string)

        bpm_tool_widget.bpm_label.setText(bpm_label_string)

    def add_beats_to_song_overview(self):
        song_object = self.model.loaded_song
        _, beats = tools.estimate_bpm(song_object)
        self.main_controller.song_overview_controller.paint_beat_lines(beats)

    def remove_beats_from_song_overview(self):
        self.main_controller.song_overview_controller.remove_beat_lines()


class OnsetDetectionToolController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.stack = main_controller.model.stack
        self.model = main_controller.model
        self.view = main_controller.view
        self.init_connections()

    def init_connections(self):
        self.view.tools_window.onset.paint_to_song_overview_button.clicked.connect(self.add_onsets_to_song_overview)
        self.view.tools_window.onset.remove_from_song_overview_button.clicked.connect(self.remove_onsets_from_song_overview)
    
    def add_onsets_to_song_overview(self):
        print(f"Adding Onsets to Song Overview")
        song_object = self.model.loaded_song
        onsets = tools.detect_onsets(song_object)
        self.main_controller.song_overview_controller.paint_onset_lines(onsets)

    def remove_onsets_from_song_overview(self):
        print(f"Removing Onsets from Song Overview")
        self.main_controller.song_overview_controller.remove_onset_lines()
