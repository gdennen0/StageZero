"""
Module: PlotClickHandler

This module defines the PlotClickHandler class which is responsible for handling the clicks on the plot in the application.
It interacts with the main controller, model, and view of the application to perform various operations based on the current playback mode.

Arguments:
    main_controller (object): The main controller of the application. It is used to interact with other parts of the application.

Returns:
    None. This module is used for its side effects of handling clicks on the plot.

The PlotClickHandler class has several methods to handle clicks based on the current playback mode. 
The handle_click method checks the current playback mode and calls the appropriate method to handle the click. 
For example, if the playback mode is "Record", it calls the handle_record_click method.
"""

import math
from view import DialogWindow


class PlotClickHandler:
    # This class handles the clicks on the plot
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.model = main_controller.model

    def handle_click(self, scene_pos, plot_pos_raw):
        # This function handles the click based on the current playback mode
        playback_mode = self.main_controller.playback_mode_controller.get_current_mode()

        if playback_mode == "Record":
            # If the playback mode is "Record", handle the click accordingly
            self.handle_record_click(scene_pos, plot_pos_raw)
        # Add more elif conditions here for other playback modes

        if playback_mode == "Edit":
            # If the playback mode is "Edit", handle the click accordingly
            self.handle_edit_click(scene_pos, plot_pos_raw)

        if playback_mode == "Play":
            # If the playback mode is "Play", do nothing
            print(f"Playback mode: Play selected, doing nothing")

    def handle_record_click(self, scene_pos, plot_pos_raw):
        # This function handles the click when the playback mode is "Record"
        matched_layer_index = math.floor(plot_pos_raw.y())
        print(f"matched layer index: {matched_layer_index}")
        matched_layer_name = self.model.loaded_stack.layers[matched_layer_index].name
        matched_frame = self.match_click_to_frame(scene_pos, plot_pos_raw)

        print(f"User Click: {matched_layer_name} | frame: {matched_frame}")
        # Add the EventItem to the appropriate layer in the LayerModel
        if matched_layer_index < len(self.model.loaded_stack.layers):
            self.model.loaded_stack.layers[matched_layer_index].add(matched_frame)
        else:
            print("ERROR: Layer doesn't exist at index")

        # add event to appropritate PlotDataGroup
        self.main_controller.event_controller.add_new_event_to_plot(
            matched_layer_name, matched_frame
        )
        # self.main_controller.layer_controller.refresh()

    def handle_edit_click(self, scene_pos, plot_pos_raw):
        # This function handles the click when the playback mode is "Edit"
        # matched_layer_index = math.floor(plot_pos_raw.y())
        # matched_frame = self.match_click_to_frame(scene_pos, plot_pos_raw)
        # matched_layer_name = self.model.loaded_stack.layers[matched_layer_index].name

        # print(f"User Click: {matched_layer_name} | frame: {matched_frame}")
        # try:
        #     event_object = self.model.loaded_stack.layers[matched_layer_index].objects[
        #         matched_frame
        #     ]
        # except KeyError:
        #     DialogWindow.error(
        #         f"Error: Event at frame {matched_frame} does not exist within {matched_layer_index}."
        #     )
        #     return

        # self.main_controller.event_controller.edit_event(event_object)
        pass

    def match_click_to_frame(self, scene_pos, plot_pos):
        # This function matches the click to a frame
        # print(f"Matching click raw x: {scene_pos} / plot pos x {plot_pos}")
        frame_number = int(round(plot_pos.x()))
        # print(f"--> Matched to frame: {frame_number}")
        return frame_number
