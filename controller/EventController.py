"""
Module: EventController

This module defines the EventController class which is responsible for controlling the events in the application.
It interacts with the main controller, model, and view of the application to perform various operations related to events.
It provides functionalities to clear event plot, add event to plot and edit an event.

Arguments:
    main_controller (object): An instance of the main controller class. It is used to interact with the model and view of the application.

Returns:
    None. The class constructor initializes the main controller, model, view, and stack for the EventController instance.
    The methods of this class perform operations on these instances but do not return any value.
"""

from view import EventEditorWidget


class EventController:
    # This class controls the events
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.stack = main_controller.model.stack
        self.model = main_controller.model
        self.view = main_controller.view

    def clear_event_plot(self, layer_name):
        # This function clears the event plot
        widget = self.main_controller.layer_controller.get_widget_by_name(layer_name)
        widget.event_plot.clear()

    def add_event_to_plot(self, layer_name, frame_number):
        # This function adds an event to the plot
        print(f"layer: {layer_name}, adding event at frame {frame_number}")
        self.main_controller.layer_controller.replot_layer(layer_name)

    def edit_event(self, event_object):
        # This function edits an event
        self.editor = EventEditorWidget(event_object)
        self.editor.exec_()