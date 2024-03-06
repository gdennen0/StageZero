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
from view.PlotDataGroup import PlotDataGroup
from .PlotClickHandler import PlotClickHandler


class LayerController:
    # This class manages the layers in the application.
    def __init__(self, main_controller):
        self.plot_layer_items = {}

        self.main_controller = main_controller
        self.stack = main_controller.model.stack
        self.model = main_controller.model
        self.view = main_controller.view
        self.layer_widget = self.view.main_window.stack.layer_widget
        self.layer_plot = self.view.main_window.stack.layer_widget.layer_plot
        self.song_overview_plot = self.view.main_window.song_overview.song_plot

        self.layer_plot.setXLink(self.song_overview_plot)

        self.connect_signals()
        self.connect_layer_plot_signals()

    def connect_signals(self):
        # Connect the remove and add layer buttons to their respective functions
        self.view.main_window.layer_control.btnRemove.clicked.connect(self.remove_layer)
        self.view.main_window.layer_control.btnAdd.clicked.connect(self.add_layer)

    def connect_layer_plot_signals(self):
        self.layer_plot.scene().sigMouseClicked.connect(self.click)

    def refresh(self):
        # Clear the layer plot and reinitialize it
        self.layer_plot.clear()
        x_axis = self.model.loaded_song.x_axis
        self.update_layer_names()
        y_values = np.zeros(self.model.loaded_song.frame_qty)
        num_layers = len(self.model.loaded_stack.layers)
        self.layer_plot.plot(x_axis, y_values, pen=None)
        self.set_layer_plot_limits(0, self.model.loaded_song.frame_qty, 0, num_layers)
        self.add_layers_to_plot()
        self.reload_playhead()
        self.update_layer_plot_height()

    def add_layers_to_plot(self):
        layer_names = [layer.name for layer in self.model.loaded_stack.layers]
        for layer_name in layer_names:
            self.add_plot_layer(layer_name)

    def replot_layer_plot(self):
        print(f"replot layer plot")
        # Replot the layer plot
        self.layer_plot = self.view.main_window.stack.layer_widget.layer_plot
        self.layer_plot.replot()

    def init_playhead(self):
        # Initialize the vertical line in the layer widget
        self.layer_widget.init_playhead()

    def reload_playhead(self):
        self.layer_widget.reload_playhead()

    def refresh_plot_data_item(self):
        # item = self.model.loaded_stack.layers[layer_name].objects[frame_number].plot_data_item
        # self.replot_layer_plot()
        pass

    def add_layer(self):
        # Add a new layer to the stack
        if self.model.stack.objects != None:
            layer_name = DialogWindow.input_text("Enter Layer Name", "Layer Name")
            while len(layer_name) > 20:
                layer_name = DialogWindow.input_text(
                    "Name too long. Enter up to 20 characters", "Layer Name"
                )
            self.add_model_layer(layer_name)
            self.add_plot_layer(layer_name)

    def remove_layer(self):
        # Remove a layer from the stack
        layer_name = DialogWindow.input_text("Enter Layer Name", "Layer Name")
        stack = self.model.stack.objects[self.model.stack.loaded_stack]
        stack.remove_layer_from_model(layer_name)
        self.refresh()

    def add_model_layer(self, layer_name):
        # Add a new layer to the model
        self.model.loaded_stack.create_layer(layer_name)

    def add_plot_layer(self, layer_name):
        # Add a new layer to the plot
        print(f"add plot layer {layer_name}")
        self.load_plot_layer_data(layer_name)
        self.update_layer_names()
        self.update_layer_plot_height()
        # self.refresh_plot_widget_layer(layer_name)

    def load_plot_layer_data(self, layer_name):
        # Refresh a single layer in the layer plot by name
        layer_index = self.model.loaded_stack.get_layer_index(layer_name)
        layer_object = self.model.loaded_stack.layers[layer_index]
        plot_layer_data = layer_object.get_plot_layer_data()

        self.layer_widget.remove_items(plot_layer_data)
        self.main_controller.event_controller.add_plot_layer_data(plot_layer_data)
        layer_qty = self.model.loaded_stack.get_layer_qty()
        self.set_layer_plot_limits(yMax=layer_qty)

    def update_layer_names(self):
        # Update the names of the layers
        loaded_stack = self.model.loaded_stack
        # loaded_stack = self.model.stack.objects[self.model.stack.loaded_stack]
        print(
            f"update layer name loaded stack {loaded_stack} type {type(loaded_stack)}"
        )
        # layer_names = [layer.name for layer in loaded_stack]
        layer_names = []
        for layer in loaded_stack.layers:
            print(f"layer {layer}")
            layer_names.append(layer.name)

        self.layer_widget.update_layer_names(layer_names)

    def update_layer_plot_height(self):
        # Update the height of the layer plot
        layer_height = 50  # You can adjust this value as needed
        offset = 18  # This encompasses the x axis height
        num_layers = len(self.model.loaded_stack.layers)
        total_height = num_layers * layer_height + offset
        self.view.main_window.stack.layer_widget.layer_plot.setFixedHeight(total_height)

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
        # Auto re-zoom the plot to fit the new changed limits
        # But only zoom out the y axis 100%
        self.layer_plot.getViewBox().setRange(yRange=(yMin, yMax), padding=0)

    def handle_position_change(self, current_frame, new_frame_object):
        new_frame_x = int(new_frame_object.x())
        new_frame_y = int(new_frame_object.y())
        print(
            f"handle_pos_change | start position: {current_frame} | new x position: {new_frame_x}"
        )
        self.model.loaded_stack.move_event(
            new_frame_y, current_frame, new_frame_x
        )  # new_frame_y=layer index | current_frame=current index | new_frame_x =new index

    def handle_right_click(self, layer_index, frame_num):
        try:
            model_object = self.model.loaded_stack.layers[layer_index].objects[
                frame_num
            ]
        except KeyError:
            DialogWindow.error(
                f"Model Error: Event at frame {frame_num} does not exist in layer {layer_index}."
            )
            return
        layer_name = self.model.loaded_stack.get_layer_name(
            layer_index
        )  # TODO: update all these unnecessary conversions to find list/dict indexes
        self.main_controller.event_controller.edit_event(layer_name, model_object)

    def click(self, event):
        scene_pos = event.scenePos()
        plot_pos = self.layer_plot.plotItem.vb.mapSceneToView(scene_pos)
        print(f"[PLOT CLICK] scene: {scene_pos} | plot: {plot_pos} ")
        self.plot_click_handler = PlotClickHandler(self.main_controller)
        self.plot_click_handler.handle_click(scene_pos, plot_pos)

    def update_playhead_position(self, frame_number):
        # Update the position of the vertical line
        self.playhead = self.layer_widget.playhead
        self.playhead.setPos(float(frame_number))

    def tally_events(event_data):
        # Count the number of events in the event data
        return sum(1 for value in event_data.values() if value is not None)
