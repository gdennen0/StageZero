import tools
from view.LayerSelectPopup import open_layer_selection_popup


class LocalController:
    def __init__(self, local_view, main_controller):
        self.local_view = local_view
        self.main_controller = main_controller
        self.stack = main_controller.model.stack
        self.model = main_controller.model
        self.view = main_controller.view
        self.beats = None
        self.selected_layer_name = None
        self.init_connections()

    def init_connections(self):
        self.local_view.count_button.clicked.connect(self.estimate_bpm)
        self.local_view.add_events_to_layer_button.clicked.connect(
            self.add_events_to_layer
        )

    def open(self):
        self.local_view.open()
        self.estimate_bpm()

    def estimate_bpm(self):
        song_object = self.model.loaded_song
        tempo, self.beats = tools.estimate_bpm(song_object)
        self.update_bpm_label(int(tempo))

    def update_bpm_label(self, bpm):
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

    # add the events to a new layer functionality
    def add_events_to_layer(self):
        print(f"Add Events to layer selected")
        if self.beats is not None:
            layer_names = [layer.name for layer in self.model.loaded_stack.layers]
            # Store the popup as an attribute to keep the reference
            self.layer_selection_popup = open_layer_selection_popup(layer_names)
            self.layer_selection_popup.layer_list_widget.itemSelectionChanged.connect(
                self.on_layer_selected
            )
            self.layer_selection_popup.accept_button.clicked.connect(
                self.on_add_to_layer_button_clicked
            )

            # Show the dialog non-modally
            self.layer_selection_popup.show()
        else:
            print(f"Beat list is None")

    def on_layer_selected(self):
        selected_items = self.layer_selection_popup.layer_list_widget.selectedItems()
        if selected_items:
            self.selected_layer_name = selected_items[0].text()
            print(f"Layer {self.selected_layer_name} selected")

    def on_add_to_layer_button_clicked(self):
        if self.selected_layer_name is None:
            print(f"ERROR: Please select a valid layer")
            return
        self.model.add_events_to_layer(self.selected_layer_name, self.beats)
        self.main_controller.layer_controller.refresh()
        self.layer_selection_popup.close()
