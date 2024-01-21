import tools
from functools import partial
from analyze import AudioClassifier as ac

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
        self.view.tools_window.onset.remove_from_song_overview_button.clicked.connect(partial(self.remove_onsets_from_song_overview, "all-pass"))
        self.view.tools_window.onset.filter_type_dropdown.currentIndexChanged.connect(self.on_filter_type_selected)


    def add_onsets_to_song_overview(self):
        print(f"Adding Onsets to Song Overview")
        song_object = self.model.loaded_song
        onsets = tools.detect_onsets(song_object)
        self.main_controller.song_overview_controller.paint_onset_lines(onsets, "all-pass")

    def remove_onsets_from_song_overview(self, onset_type):
        print(f"Removing Onsets from Song Overview")
        self.main_controller.song_overview_controller.remove_onset_lines(onset_type)


    def on_filter_type_selected(self, index):
        filter_type = self.view.tools_window.onset.filter_type_dropdown.itemText(index)
        print(f"Selected filter type: {filter_type}")
        self.add_filter_widget(filter_type)
        self.add_filter_data_to_song_model(filter_type)

    def add_filter_widget(self, filter_type):
        self.view.tools_window.onset.add_filter(filter_type)
        self.view.tools_window.onset.onset_filter_widgets[filter_type].paint_to_song_overview_button.clicked.connect(partial(self.add_filter_onsets_to_song_overview, filter_type))
        self.view.tools_window.onset.onset_filter_widgets[filter_type].remove_from_song_overview_button.clicked.connect(partial(self.remove_filter_onsets_from_song_overview, filter_type))

        print(f"adding filter {filter_type}")
    
    def add_filter_data_to_song_model(self, filter_type):
        song_object = self.model.loaded_song
        sample_rate = self.model.loaded_song.original_sample_rate

        if filter_type not in self.model.loaded_song.filter:
            filtered_data = self.filter_data(song_object, filter_type)
            self.model.loaded_song.add_filtered_data(filter_type, filtered_data, sample_rate)



    def add_filter_onsets_to_song_overview(self, filter_type):
        print(f"adding {filter_type} filter onsets from song overview plot")
        filtered_song_data = self.model.loaded_song.filter[filter_type].filtered_data
        sample_rate = self.model.loaded_song.filter[filter_type].sample_rate
            
        onsets = tools.detect_onsets(song_data=filtered_song_data, sample_rate=sample_rate)
        self.main_controller.song_overview_controller.paint_onset_lines(onsets, "lo-pass")

    def remove_filter_onsets_from_song_overview(self, filter_type):
        print(f"removing {filter_type} filter onsets from song overview plot")
        self.main_controller.song_overview_controller.remove_onset_lines(filter_type)


    def filter_data(self, song_object, filter_type):
        if filter_type == "lo-pass":
            filtered_song_data = tools.apply_lo_pass_filter(song_object)
            return filtered_song_data


class KicksToolController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.stack = main_controller.model.stack
        self.model = main_controller.model
        self.view = main_controller.view
        self.events = None
        self.init_connections()

    def init_connections(self):
        self.view.tools_window.kick.process_kick_events_button.clicked.connect(self.process_kick_events)
        self.view.tools_window.kick.add_events_to_layer_button.clicked.connect(self.add_events_to_layer)
        self.view.tools_window.kick.layer_selection_popup.itemSelectionChanged.connect(self.on_layer_selected)
    # def add_events_to_layer(self, layer_index, events):

    # Pass pass the song path to the Kick Tool CNN module


    # add the events to a new layer functionality
    def add_events_to_layer(self):
        print(f"Add Events to layer selected")
        if self.events is not None:
            layer_names = [layer.name for layer in self.model.loaded_stack.layers]
            self.view.tools_window.kick.open_layer_selection_popup(layer_names)
            # self.view.tools_window.kick.layer_selection_popup.itemClicked.connect(self.on_layer_selected)


    def on_layer_selected(self):
        selected_items = self.view.tools_window.kick.layer_selection_popup.selectedItems()
        if selected_items:
            layer_name = selected_items[0].text()
            self.model.add_events_to_layer(layer_name, self.events)
            self.main_controller.layer_controller.reload_layer_plot()
            print(f"Layer {layer_name} selected")

    # def add_events_to_layer(self, layer_index, events):
    #     layer_name = self.view.tools_window.kick.open_layer_selection_popup()
    #     self.model.add_events_to_layer(layer_name, events)

    def process_kick_events(self):
        song_path = self.model.loaded_song.path
        self.events = ac.Kicks.detect(song_path)
        self.view.tools_window.kick.update_event_count_label(len(self.events))

