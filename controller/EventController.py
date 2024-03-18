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
from pprint import pprint
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton
from view.LayerSelectPopup import open_layer_selection_popup


class EventController:    
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.stack = main_controller.model.stack
        self.model = main_controller.model
        self.view = main_controller.view
        self.layer_widget = self.view.main_window.stage_widget.stack.layer_widget
        self.layer_plot = self.view.main_window.stage_widget.stack.layer_widget.layer_plot
        self.selected_events = []
        self.connect_event_properties_widget_signals()

    def connect_point_signals(self, plot_data_item):
        plot_data_item.sigClicked.connect(self.main_controller.layer_controller.click)
        plot_data_item.sigMouseRightClicked.connect(self.main_controller.layer_controller.handle_right_click)
        self.view.main_window.stage_widget.stack.layer_widget.connectCustomViewBoxSignal("sigItemsSelected", self.select_roi_events)
        plot_data_item.sigPositionDrag.connect(self.drag_selected_events)
        plot_data_item.sigEventSelected.connect(self.select_event)
        plot_data_item.sigAdditionalEventSelected.connect(self.select_additional_event)
        plot_data_item.sigEventDragStart.connect(self.start_drag)
        plot_data_item.sigEventDragEnd.connect(self.end_drag)

    def connect_event_properties_widget_signals(self):
        self.view.main_window.event_properties_widget.line_items["Name"].textChanged.connect(self.update_event_name)
        self.view.main_window.event_properties_widget.line_items["Color"].textChanged.connect(self.update_event_color)
        self.view.main_window.event_properties_widget.line_items["Layer"].textChanged.connect(self.update_event_layer)
        self.view.main_window.event_properties_widget.line_items["Frame"].textChanged.connect(self.update_event_frame)
        self.view.main_window.event_action_widget.delete_button.clicked.connect(self.delete_selected_events)
        self.view.main_window.event_action_widget.nudge_minus_button.clicked.connect(self.nudge_event_minus)
        self.view.main_window.event_action_widget.nudge_plus_button.clicked.connect(self.nudge_event_plus)
        self.view.main_window.event_action_widget.change_layer_button.clicked.connect(self.change_event_layer)

    def update_event_name(self, new_name ):
        print(f"update_event_name {new_name}")
        for event in self.selected_events:
            event.name = new_name
            self.model.loaded_stack.layers[event.parent_layer_name].objects[event.frame_num].name = new_name

    def update_event_color(self):
        print("update_event_color")

    def update_event_layer(self):
        print("update_event_layer")

    def update_event_frame(self):
        print("update_event_frame")

    def change_event_layer(self):
        if not self.selected_events:
            print("No events selected.")
            return

        layer_names = [layer_item.layer_name for layer_key, layer_item in self.model.loaded_stack.layers.items()]
        self.layer_selection_popup = open_layer_selection_popup(layer_names)

        def on_layer_selected():
            selected_layer_items = self.layer_selection_popup.layer_list_widget.selectedItems()
            if selected_layer_items:
                self.selected_layer_name = selected_layer_items[0].text()
                print(f"Selected layer: {self.selected_layer_name}")

        def on_accept():
            print(f"Moving selected events to layer index {self.selected_layer_name}")
            for event in self.selected_events:
                original_layer_name = event.parent_layer_name
                self.model.loaded_stack.change_event_layer(original_layer_name, self.selected_layer_name, event.frame_num)
                self.layer_widget.remove_item(event)
                updated_plot_data_item = self.model.loaded_stack.layers[self.selected_layer_name].objects[event.frame_num].plot_data_item
                self.layer_widget.add_plot_item(updated_plot_data_item)
            self.layer_selection_popup.close()

        self.layer_selection_popup.layer_list_widget.itemSelectionChanged.connect(on_layer_selected)
        self.layer_selection_popup.accept_button.clicked.connect(on_accept)

        self.layer_selection_popup.show()


    def nudge_event_minus(self):
        print(f"nudge events minus")
        for event in self.selected_events:
            self.model.loaded_stack.layers[event.parent_layer_name].nudge_event(event.frame_num, -1)

    def nudge_event_plus(self):
        print(f"nudge events plus")
        for event in self.selected_events:
            self.model.loaded_stack.layers[event.parent_layer_name].nudge_event(event.frame_num, 1)

    def delete_selected_events(self):
        for event in self.selected_events:
            self.model.loaded_stack.delete_event(event.parent_layer_name, event.frame_num)
            self.layer_widget.remove_item(event)


    def clear_event_plot(self, layer_name):
        # This function clears the event plot
        widget = self.main_controller.layer_controller.get_widget_by_name(layer_name)
        widget.event_plot.clear()

    def add_new_event_to_plot(self, layer_name, frame_number):
        # This function adds an event to the plot
        print(f"layer '{layer_name}' adding event at frame {frame_number}")
        self.model.loaded_stack.layers[layer_name].objects[
            frame_number
        ].generate_layer_plot_item()
        plot_data_item = (
            self.model.loaded_stack.layers[layer_name]
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

    def start_drag(self):
        # Call this method when the drag operation starts
        print(f"start drag controller")
        self.initial_positions = {
            event: event.frame_num for event in self.selected_events
        }
        print(f"initial positions {self.initial_positions}")
        print(f"Selected Events For Drag:")
        pprint(self.selected_events)

    def drag_selected_events(self, pos_delta):
        # Ensure initial positions are captured before calling this method
        for event in self.selected_events:
            initial_pos_x = self.initial_positions[event]
            new_pos_x = initial_pos_x + pos_delta.x()
            event.set_x_position(new_pos_x)

    def end_drag(self):
        # Call this method when the drag operation ends
        self.update_event_model(self.selected_events)
        self.initial_positions.clear()

    def update_event_model(self, events):
        for event in events:
            data = event.getData()
            current_frame = event.frame_num
            layer_name = event.parent_layer_name
            new_frame_x = int(data[0][0])
            # new_frame_y = int(data[1][0])
            print(f"Moving frame: {current_frame} ---> {new_frame_x}")
            self.model.loaded_stack.move_event(
                layer_name, current_frame, new_frame_x
            )  # new_frame_y=layer index | current_frame=current index | new_frame_x =new index
            event.frame_num = new_frame_x

    def handle_position_change(self, current_frame, event):
        new_frame_x = int(event.x())
        # new_frame_y = int(event.y())
        layer_name = event.parent_layer_name
        print(
            f"handle_pos_change | start position: {current_frame} | new x position: {new_frame_x}"
        )
        self.model.loaded_stack.move_event(
            layer_name, current_frame, new_frame_x
        )  # new_frame_y=layer index | current_frame=current index | new_frame_x =new index

    def select_event(self, event):
        for selected_event in self.selected_events:
            print(f"event {selected_event.frame_num}")
            selected_event.unselect()

        self.selected_events = []
        if event is not None:
            self.selected_events.append(event)
            event.select()
            layer_key = event.parent_layer_name
            print(f"layer '{layer_key}' frame number: {event.frame_num}")
            event_item = self.model.loaded_stack.layers[layer_key].get_event(event.frame_num)
            self.view.main_window.event_properties_widget.update(event_item)


    def select_additional_event(self, event):
        if event not in self.selected_events:
            self.selected_events.append(event)
            layer_key = event.parent_layer_name
            print(f"layer '{layer_key}' frame number: {event.frame_num}")
            event_item = self.model.loaded_stack.layers[layer_key].get_event(event.frame_num)
            self.view.main_window.event_properties_widget.update(event_item)

    def select_roi_events(self, events):
        for event in events:
            self.select_additional_event(event)

    def edit_event(self, layer_name, model_object):
        # This function edits an event
        print(f"edit_event \n layer:{layer_name}")
        model_object
        self.editor = EventEditorWidget(model_object)
        self.editor.changes_saved.connect(
            self.main_controller.layer_controller.refresh_plot_data_item
        )
        self.editor.exec_()
