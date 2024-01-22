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
from PyQt5.QtCore import Qt
from view import DialogWindow
from controller.PlotClickHandler import PlotClickHandler

class LayerController:
    # This class manages the layers in the application.
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.stack = main_controller.model.stack
        self.model = main_controller.model
        self.view = main_controller.view
        self.plot_click_handler = PlotClickHandler(main_controller)
        self.connect_signals()

    def connect_signals(self):
        # Connect the remove and add layer buttons to their respective functions
        self.view.main_window.layer_control.btnRemove.clicked.connect(self.remove_layer)
        self.view.main_window.layer_control.btnAdd.clicked.connect(self.add_layer)

    def init_plot(self, stack_name):
        # Initialize the plot for the given stack
        layer_plot = self.view.main_window.stack.layer_widget.layer_plot
        song_overview_plot = self.view.main_window.song_overview.song_plot
        frame_qty = self.model.stack.objects[stack_name].frame_qty

        x_ticks = np.arange(0, frame_qty, 1)
        y_values = np.zeros(frame_qty)

        num_layers = len(self.model.stack.objects[stack_name].layers)

        # Plot the layer plot and link it to the song_overview_plot
        layer_plot.plot(x_ticks, y_values, pen=None)
        layer_plot.setXLink(song_overview_plot)

        self.init_playhead()
        self.set_layer_plot_limits(0, frame_qty, 0, num_layers)
        self.connect_layer_plot_signals(layer_plot)

    def reload_layer_plot(self):
        # Clear the layer plot and reinitialize it
        self.view.main_window.stack.layer_widget.layer_plot.clear()
        layers = self.model.stack.objects[self.model.stack.loaded_stack].layers
        self.init_plot(self.model.stack.loaded_stack)
        self.update_layer_plot_height()

        for index, layer in enumerate(layers):
            self.add_plot_layer(layer.name)

    def replot_layer_plot(self):
        # Replot the layer plot
        layer_plot = self.view.main_window.stack.layer_widget.layer_plot
        layer_plot.replot()

    def add_layer(self):
        # Add a new layer to the stack
        if self.model.stack.objects != None:
            layer_name = DialogWindow.input_text("Enter Layer Name", "Layer Name")
            while len(layer_name) > 20:
                layer_name = DialogWindow.input_text("Name too long. Enter up to 20 characters", "Layer Name")
            self.add_model_layer(layer_name)
            self.add_plot_layer(layer_name)

    def remove_layer(self):
        # Remove a layer from the stack
        layer_name = DialogWindow.input_text("Enter Layer Name", "Layer Name")
        stack = self.model.stack.objects[self.model.stack.loaded_stack]
        stack.remove_layer_from_model(layer_name)
        self.main_controller.layer_controller.reload_layer_plot()

    def add_model_layer(self, layer_name):
        # Add a new layer to the model
        self.model.stack.objects[self.model.loaded_song.name].create_layer(layer_name)

    def add_plot_layer(self, layer_name):
        # Add a new layer to the plot
        stack = self.model.loaded_stack
        layer_plot = self.view.main_window.stack.layer_widget.layer_plot
        self.refresh_plot_data_item(layer_name)
        layer_plot_item = stack.layers[stack.get_layer_index(layer_name)].plot_data_item
        layer_plot.addItem(layer_plot_item)

        self.update_layer_names()
        self.update_layer_plot_height()
        self.refresh_plot_widget_layer(layer_name)

    def refresh_plot_widget_layer(self, layer_name):
        # Refresh the layer plot widget
        stack = self.model.stack.objects[self.model.song.loaded_song]
        plot = self.view.main_window.stack.layer_widget.layer_plot

        layer_index = stack.get_layer_index(layer_name)
        layer_plot_item = stack.layers[layer_index].plot_data_item

        plot.removeItem(layer_plot_item)
        plot.addItem(stack.layers[layer_index].plot_data_item)

        layer_qty = stack.get_layer_qty()
        self.set_layer_plot_limits(yMax=layer_qty)

    def update_layer_names(self):
        # Update the names of the layers
        loaded_stack = self.model.loaded_stack
        layer_names = [
            layer.name
            for layer in loaded_stack.layers
        ]
        self.view.main_window.stack.layer_widget.update_layer_names(layer_names)

    def update_layer_plot_height(self):
        # Update the height of the layer plot
        layer_height = 50  # You can adjust this value as needed
        offset = 18 # This encompasses the x axis height 
        num_layers = len(self.model.stack.objects[self.model.stack.loaded_stack].layers)

        total_height = num_layers * layer_height + offset

        self.view.main_window.stack.layer_widget.layer_plot.setFixedHeight(total_height)

    def set_layer_plot_limits(self, xMin=0, xMax=None, yMin=0, yMax=None):
        # Set the limits of the layer plot
        layer_plot = self.view.main_window.stack.layer_widget.layer_plot
        limits = {}

        if xMin is not None:
            limits["xMin"] = xMin
        if xMax is not None:
            limits["xMax"] = xMax
        if yMin is not None:
            limits["yMin"] = yMin
        if yMax is not None:
            limits["yMax"] = yMax

        layer_plot.setLimits(**limits)
        # Auto re-zoom the plot to fit the new changed limits
        # But only zoom out the y axis 100%
        layer_plot.getViewBox().setRange(yRange=(yMin, yMax), padding=0)

    def refresh_plot_data_item(self, layer_name):
        # Refresh the plot data item for the given layer
        stack = self.model.stack.objects[self.model.song.loaded_song]
        # translate raw data to plot data
        plottable_data = self.translate_raw_data_to_plot_data(layer_name)
        # get the layer plot item
        stack.set_event_plot_data_item(layer_name, plottable_data)

    def translate_raw_data_to_plot_data(self, layer_name):
        # Translate the raw data of a layer to plottable data
        stack = self.model.stack.objects[self.model.loaded_song.name]
        raw_data = stack.get_layer_raw_data(layer_name)
        layer_index = stack.get_layer_index(layer_name)

        present_events_array = [(key, (layer_index + 0.5)) for key, value in raw_data.items() if value is not None]

        plottable_data = np.array(present_events_array)
        return plottable_data

    def calculate_frame_quantity(self, length_ms, fps):
        # Calculate the number of frames for a given length and fps
        frame_qty = math.ceil((length_ms / 1000) * fps)
        print(f"# of frames for {(length_ms / 1000)}seconds @ {fps}fps is {frame_qty}")
        return frame_qty

    def init_playhead(self):
        # Initialize the vertical line in the layer widget
        layer_widget = self.view.main_window.stack.layer_widget
        layer_widget.init_playhead()
        self.main_controller.audio_playback_controller.time_update_thread.time_updated.connect(
            self.update_playhead_position
        )

    def update_playhead_position(self, frame_number):
        # Update the position of the vertical line
        playhead = self.view.main_window.stack.layer_widget.playhead
        playhead.setPos(float(frame_number))

    def tally_events(event_data):
        # Count the number of events in the event data
        return sum(1 for value in event_data.values() if value is not None)

    def on_plot_click(self, event, event_plot):
        # Handle a click on the plot
        if event.button() == Qt.LeftButton:
            scene_pos = event.scenePos()
            plot_pos = event_plot.plotItem.vb.mapSceneToView(scene_pos)
            print(f"[PLOT CLICK] scene: {scene_pos} | plot: {plot_pos} ")
            self.plot_click_handler.handle_click(scene_pos, plot_pos)

    def connect_layer_plot_signals(self, layer_plot):
        # Connect the plot click signal to the on_plot_click function
        layer_plot.scene().sigMouseClicked.connect(
            lambda event, layer_plot=layer_plot: self.on_plot_click(event, layer_plot)
        )

    def disconnect_layer_plot_signals(self, layer_plot):
        # Disconnect the plot click signal from the on_plot_click function
        try:
            layer_plot.scene().sigMouseClicked.disconnect(
                lambda event, layer_plot=layer_plot: self.on_plot_click(event, layer_plot)
            )
        except TypeError:
            print("No signals connected to the plot.")
