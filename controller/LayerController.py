"""
Module: LayerController

This module defines the LayerController class, which manages the layers in the application. It is responsible for initializing, updating, and managing the layers in the application's stack. It also connects the layer control buttons to their respective functions and handles the plotting of layers.

Arguments:
    main_controller (object): The main controller of the application. It is used to access the model, view, and other controllers of the application.

Returns:
    None. The LayerController class does not return any value but it modifies the state of the application by managing the layers in the stack.
"""

import math
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from view import DialogWindow
from view.LayerPlotItem import LayerPlotItem
from constants import LAYER_HEIGHT


class LayerController:
    # This class manages the layers in the application.
    def __init__(self, main_controller):
        self.plot_layer_items = {}

        self.main_controller = main_controller
        self.stack = main_controller.model.stack
        self.model = main_controller.model
        self.view = main_controller.view
        self.layer_widget = self.view.main_window.stage_widget.stack.layer_widget
        self.layer_plot = self.view.main_window.stage_widget.stack.layer_widget.layer_plot
        self.song_overview_plot = self.view.main_window.stage_widget.song_overview.song_plot
        self.layer_plot.setXLink(self.song_overview_plot)
        self.add_playhead()
        self.connect_signals()

    def connect_signals(self):
        # Connect the remove and add layer buttons to their respective functions
        self.view.main_window.stage_widget.layer_control.btnRemove.clicked.connect(self.remove_layer)
        self.view.main_window.stage_widget.layer_control.btnAdd.clicked.connect(self.add_layer)

    def refresh(self):
        self.refresh_layers()

    def refresh_layers(self):
        self.add_layers_to_plot()
        self.reset_y_axis_ticks()
        self.reset_x_axis_max_length()

    def reset_x_axis_max_length(self):
        x_axis = self.model.loaded_song.x_axis
        self.layer_widget.set_plot_x_max(x_axis[-1])

    def reset_y_axis_ticks(self):
        ticks = self.generate_ticks()           
        self.layer_widget.y_axis.setTicks([[value for value in ticks ]])

    def add_layers_to_plot(self):
        layer_names = [layer_item.layer_name for layer_key, layer_item in self.model.loaded_stack.layers.items()]
        for layer_name in layer_names:
            self.add_plot_layer(layer_name)

    def add_plot_layer(self, layer_name):
        print(f"[LayerController][add_plot_layer] | name: {layer_name}")
        self.load_plot_layer_data(layer_name)
        self.reset_y_axis_ticks()
        self.update_layer_plot_height()

    def load_plot_layer_data(self, layer_name):
        layer_object = self.model.loaded_stack.layers[layer_name]
        plot_layer_data = layer_object.get_plot_layer_data()
        self.main_controller.event_controller.add_plot_layer_data(plot_layer_data)
        layer_qty = self.model.loaded_stack.get_layer_qty()
        self.set_layer_plot_limits(yMax=layer_qty)

    def add_playhead(self):
        self.layer_widget.add_playhead(self.model.stack.playhead)

    def add_line(self, layer_name, frame_number): #TODO Implement this feature further in the future
        self.model.loaded_stack.layers[layer_name].add(frame_number, color=None, name=None, type="line")

    def add_layer(self):
        # Add a new layer to the stack
        if self.model.stack.objects != None:
            layer_name = DialogWindow.input_text("[Layer_Controller][add_layer] | Enter Layer Name", "Layer Name")
            while len(layer_name) > 20:
                layer_name = DialogWindow.input_text("[Layer_Controller][add_layer] | Name too long. Enter up to 20 characters", "Layer Name")
            self.add_model_layer(layer_name)
            self.add_plot_layer(layer_name)

    def remove_layer(self):
        # Remove a layer from the stack
        layer_name = DialogWindow.input_text("Enter Layer Name", "Layer Name")
        stack = self.model.stack.objects[self.model.stack.loaded_stack]
        stack.remove_layer_from_model(layer_name)
        self.refresh()

    def add_model_layer(self, layer_name): # Add a new layer to the model
        self.model.loaded_stack.create_layer(layer_name)

    def update_y_axis_layer_names(self):
        layer_names = []
        for layer_key, layer_item in self.model.loaded_stack.layers.items():
            layer_names.append(layer_key)

        self.layer_widget.update_layer_names(layer_names)

    def update_layer_plot_height(self): # Update the height of the layer plot
        layer_height = LAYER_HEIGHT  # You can adjust this value in the constants file
        offset = 18  # This encompasses the x axis height
        num_layers = len(self.model.loaded_stack.layers)
        total_height = num_layers * layer_height + offset
        self.view.main_window.stage_widget.stack.layer_widget.layer_plot.setFixedHeight(total_height)

    def set_layer_plot_limits(self, xMin=0, xMax=None, yMin=0, yMax=None):
        # Set the limits of the layer plot
        limits = {}

        if xMin is not None:
            limits["xMin"] = xMin
        if xMax is not None:
            limits["xMax"] = xMax
        if yMin is not None:
            limits["yMin"] = yMin
        if yMax is not None:
            limits["yMax"] = yMax

        self.layer_plot.setLimits(**limits)
        self.layer_plot.getViewBox().setRange(yRange=(yMin, yMax), padding=0)

    def handle_position_change(self, current_frame, event):
        new_frame_x = int(event.x())
        new_frame_y = int(event.y())
        layer_name = event.parent_layer_name
        self.model.loaded_stack.move_event(layer_name, current_frame, new_frame_x)
        print(f"[LayerController][handle_pos_change] | start position: {current_frame} | new x position: {new_frame_x}")


    def handle_right_click(self, layer_name, frame_num):
        try:
            model_object = self.model.loaded_stack.layers[layer_name].objects[frame_num]
        except KeyError:
            DialogWindow.error(f"Model Error: Event at frame {frame_num} does not exist in layer {layer_name}.")
            return
        self.main_controller.event_controller.edit_event(layer_name, model_object)

    def generate_ticks(self):
        layer_keys = list(self.model.loaded_stack.layers.keys())
        ticks = []
        counter = 0
        for layer_key in layer_keys:
            ticks.append((counter, ""))
            counter += 0.5
            ticks.append((counter, str(layer_key)))
            counter += 0.5
            ticks.append((counter, ""))

        return ticks
