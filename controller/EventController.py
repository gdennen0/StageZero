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
from PyQt5.QtCore import Qt


class EventController:
    # This class controls the events
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.stack = main_controller.model.stack
        self.model = main_controller.model
        self.view = main_controller.view
        self.layer_plot = self.view.main_window.stack.layer_widget.layer_plot
        self.selected_events = []
        
    def clear_event_plot(self, layer_name):
        # This function clears the event plot
        widget = self.main_controller.layer_controller.get_widget_by_name(layer_name)
        widget.event_plot.clear()

    def add_new_event_to_plot(self, layer_name, frame_number):
        # This function adds an event to the plot
        print(f"layer: {layer_name}, adding event at frame {frame_number}")
        layer_index = self.model.loaded_stack.get_layer_index(layer_name)
        self.model.loaded_stack.layers[layer_index].objects[
            frame_number
        ].generate_layer_plot_item()
        plot_data_item = (
            self.model.loaded_stack.layers[layer_index]
            .objects[frame_number]
            .plot_data_item
        )
        self.connect_point_signals(plot_data_item)
        self.layer_plot.addItem(plot_data_item)
        # self.main_controller.layer_controller.replot_layer(layer_name)

    def add_event_to_plot(self, event):
        self.connect_point_signals(event)
        self.layer_plot.addItem(event)

    def add_plot_layer_data(self, plot_layer_data):
        if plot_layer_data:
            print(f"plot_layer_data {plot_layer_data}")
            for event in plot_layer_data:
                self.add_event_to_plot(event)
                print(f"adding plot data item: {event}")
        else:
            print("Warning: There are no items in the event group.")

    def connect_point_signals(self, plot_data_item):
        print(f"Connecting Point Signal {plot_data_item}")
        plot_data_item.sigClicked.connect(self.main_controller.layer_controller.click)
        # plot_data_item.sigPositionChanged.connect(
        #     self.main_controller.layer_controller.handle_position_change
        # )
        plot_data_item.sigMouseRightClicked.connect(
            self.main_controller.layer_controller.handle_right_click
        )
        # self.view.main_window.stack.layer_widget.connectCustomViewBoxSignal("sigItemsSelected", self.select_events)
        plot_data_item.sigPositionDrag.connect(
            self.drag_selected_events
        )        
        plot_data_item.sigEventSelected.connect(
            self.select_event
        )
        plot_data_item.sigAdditionalEventSelected.connect(
            self.select_additional_event
        )
        plot_data_item.sigEventDragStart.connect(
            self.start_drag
        )
        plot_data_item.sigEventDragEnd.connect(
            self.end_drag
        )
    def start_drag(self):
        # Call this method when the drag operation starts
        print(f"start drag controller")
        self.initial_positions = {event: event.frame_num for event in self.selected_events}
        print(f"initial positions {self.initial_positions}")

    def drag_selected_events(self, pos_delta):
        # Ensure initial positions are captured before calling this method
        for event in self.selected_events:
            initial_pos_x = self.initial_positions[event]
            new_pos_x = initial_pos_x + pos_delta.x()
            event.set_x_position(new_pos_x)

    def end_drag(self):
        # Call this method when the drag operation ends
        self.initial_positions.clear()

    def select_event(self, event):
        print(f"selecting event")
        self.selected_events = []
        self.selected_events.append(event)
        event.select()

    def select_additional_event(self, event):
        print(f"selecting event")
        self.selected_events.append(event)
        event.select()


    def edit_event(self, layer_name, model_object):
        # This function edits an event
        print(f"edit_event \n layer:{layer_name}")
        model_object
        self.editor = EventEditorWidget(model_object)
        self.editor.changes_saved.connect(
            self.main_controller.layer_controller.refresh_plot_data_item
        )
        self.editor.exec_()

    # def select_events(self, items):
    #     self.selected_items = items
    #     for item in items: 
    #         item.set_selected(True)

    # def deselect_events(self):
    #     for item in self.selected_items:
    #         item.set_selected(False)
    #     self.selected_items = []

    # def handle_drag_event(self, selected_events, drag_offset):
    #     for event in selected_events:
    #         if event.isStart():
    #             self.drag_offset = newPos - event.buttonDownPos(Qt.LeftButton)
    #         elif event.isFinish():
    #             for item in self.selected_items:
    #                 item.setPos(item.pos() + self.drag_offset)
    #                 # Emit position changed signal if needed

    #     if ev.button() == Qt.LeftButton:
    #         if ev.isStart():
    #             # This block will only execute at the start of the drag
    #             print("Drag Start")
    #             self.dragOffset = self.points()[0].pos() - ev.buttonDownPos(
    #                 Qt.LeftButton
    #             )
    #             self.dragIndex = 0
    #             self.dragPoint = True
    #             self.dragStart = ev.buttonDownPos()
    #             ev.accept()

    #         if self.dragPoint:
    #             # This block executes throughout the drag after initialization
    #             # print("Dragging")
    #             newPos = ev.pos() + self.dragOffset
    #             if self.dragIndex is not None:
    #                 data = self.getData()
    #                 data[0][self.dragIndex] = newPos.x()
    #                 # data[1][self.dragIndex] = newPos.y()
    #                 self.setData(*data)
    #             ev.accept()

    #         if ev.isFinish():
    #             # print(f"Finished Drag {ev.lastPos()}")
    #             newPos = ev.lastPos()
    #             newPos.setX(round(newPos.x()))

    #             self.sigPositionChanged.emit(self.frame_num, newPos)
    #             self.set_x_position(newPos.x())
    #     else:
    #         ev.ignore()