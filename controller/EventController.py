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

from view import EventEditorWidget, EventCreatorWidget
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
        self.connect_event_action_widget_signals()

    def connect_event_properties_widget_signals(self):
        self.view.main_window.event_properties_widget.line_items["Name"].textChanged.connect(self.update_event_name)
        self.view.main_window.event_properties_widget.sigUpdateColor.connect(self.update_event_color)
        self.view.main_window.event_properties_widget.line_items["Layer"].textChanged.connect(self.update_event_layer)
        self.view.main_window.event_properties_widget.line_items["Frame"].textChanged.connect(self.update_event_frame)

    def connect_event_action_widget_signals(self):
        self.view.main_window.event_action_widget.delete_button.clicked.connect(self.delete_selected_events)
        self.view.main_window.event_action_widget.nudge_minus_button.clicked.connect(self.nudge_event_minus)
        self.view.main_window.event_action_widget.nudge_plus_button.clicked.connect(self.nudge_event_plus)
        self.view.main_window.event_action_widget.change_layer_button.clicked.connect(self.change_event_layer)
        self.view.main_window.event_action_widget.create_event_button.clicked.connect(self.open_new_event_dialog)

    def open_new_event_dialog(self):
        self.add_new_event_window = EventCreatorWidget(self.model.loaded_stack.layers)
        self.add_new_event_window.changes_saved.connect(self.add_new_event)
        self.add_new_event_window.exec_()

    # Public Functions
    def add(self, layer_name, frame_number, color=None, name=None):
        if color:
            self.model.loaded_stack.layers[layer_name].add(frame_number, color=color, name=None, type="event")
        if name:
            self.model.loaded_stack.layers[layer_name].add(frame_number, color=None, name=name, type="event")
        else:
            self.model.loaded_stack.layers[layer_name].add(frame_number, color=None, name=None, type="event")

        self.add_new_event_to_plot(layer_name, frame_number)

    def unpackage_data(self, event_data):
        frame_number = event_data["frame_number"]
        parent_layer_name = event_data["parent_layer_name"]
        parent_layer_number = event_data["parent_layer_number"]
        event_name = event_data["event_name"]
        color = event_data["color"]

    def add_new_event(self, package_data):
        print(f"add new event")
        # popup window to ask which frame and which layer
        # check box to add multiple events spaced evenly every x frames
        frame_number = package_data["frame_number"]
        layer_name = package_data["parent_layer_name"]
        name = package_data["event_name"]
        color = package_data["event_color"]
        event_qty = package_data["event_qty"]
        event_spacing = package_data["event_spacing"]

        if event_qty > 1:
            print(f"[EventController][add_new_event] | Adding multiple events at frames:")
            frame_number_start = frame_number
            event_counter = frame_number_start
            for _ in range(event_qty):
                print(f"[EventController][add_new_event] | --->frame counter: {event_counter}")
                self.model.loaded_stack.add_event_to_layer(layer_name, event_counter, event_name=name, event_color=color)
                self.add_new_event_to_plot(layer_name, event_counter)
                event_counter += event_spacing

        elif event_qty == 1:
            self.model.loaded_stack.add_event_to_layer(layer_name, frame_number, event_name=name, event_color=color)
            self.add_new_event_to_plot(layer_name, frame_number)
        pass

    def update_event_name(self, new_name ):
        print(f"[EventController][update_event_name] | name {new_name}")
        for event in self.selected_events:
            event.name = new_name
            self.model.loaded_stack.layers[event.parent_layer_name].objects[event.frame_num].name = new_name

    def update_event_color(self, color):
        print(f"[EventController][update_event_color] | color: {color}")
        for event in self.selected_events:
            event_model_item = self.model.loaded_stack.layers[event.parent_layer_name].objects[event.frame_num]
            event_model_item.set_color(color)
        pass

    def update_event_layer(self): #TODO update_event_layer
        # print("update_event_layer")
        pass
    def update_event_frame(self): #TODO update_event_frame
        # print("update_event_frame")
        pass

    def change_event_layer(self): 
        if not self.selected_events:
            print("[EventController][change_event_layer]| No events selected.")
            return
        
        layer_names = [layer_item.layer_name for layer_key, layer_item in self.model.loaded_stack.layers.items()]
        self.layer_selection_popup = open_layer_selection_popup(layer_names)

        def on_layer_selected():
            selected_layer_items = self.layer_selection_popup.layer_list_widget.selectedItems()
            if selected_layer_items:
                self.selected_layer_name = selected_layer_items[0].text()
                print(f"[EventController][change_event_layer][on_layer_selected] | Selected layer: {self.selected_layer_name}")

        def on_accept():
            print(f"[EventController][change_event_layer][on_accept] | Moving selected events to layer index {self.selected_layer_name}")
            for event in self.selected_events:
                original_layer_name = event.parent_layer_name
                self.model.loaded_stack.change_event_layer(original_layer_name, self.selected_layer_name, event.frame_num)
            self.layer_selection_popup.close()

        self.layer_selection_popup.layer_list_widget.itemSelectionChanged.connect(on_layer_selected)
        self.layer_selection_popup.accept_button.clicked.connect(on_accept)

        self.layer_selection_popup.show()


    def nudge_event_minus(self, increment=-1):
        print(f"[EventController][nudge_event_minus] | nudge events minus")
        for event in self.selected_events:
            self.model.loaded_stack.layers[event.parent_layer_name].nudge_event(event.frame_num, increment)

    def nudge_event_plus(self, increment=1):
        print(f"[EventController][nudge_event_plus] | nudge events plus")
        for event in self.selected_events:
            self.model.loaded_stack.layers[event.parent_layer_name].nudge_event(event.frame_num, increment)

    def delete_selected_events(self):
        for event in self.selected_events:
            self.model.loaded_stack.delete_event(event.parent_layer_name, event.frame_num)
            self.layer_widget.remove_item(event)

    def add_new_event_to_plot(self, layer_name, frame_number):
        # This function adds an event to the plot
        print(f"[EventController][add_new_event_to_plot] | layer '{layer_name}' adding event at frame '{frame_number}'")
        self.model.loaded_stack.layers[layer_name].objects[frame_number].generate_layer_plot_item()
        plot_data_item = (self.model.loaded_stack.layers[layer_name].objects[frame_number].plot_data_item)
        self.main_controller.action.stack.connect_event_signal(plot_data_item)
        self.layer_plot.addItem(plot_data_item)

    def add_event_list_to_plot(self, layer_name, frame_number_list):
        for frame_number in frame_number_list:
            self.add_new_event_to_plot(layer_name, frame_number)

    def add_event_to_plot(self, event):
        self.main_controller.action.stack.connect_event_signal(event)
        self.layer_plot.addItem(event)

    def add_plot_layer_data(self, plot_layer_data):
        if plot_layer_data:
            for event in plot_layer_data:
                self.add_event_to_plot(event)
                print(f"[EventController][add_plot_layer_data] | Adding plot data item: {event}")
        else:
            print("[EventController][add_plot_layer_data] | Warning: There are no items in the event group.")

    def start_drag(self):
        self.initial_positions = {event: event.frame_num for event in self.selected_events}

    def drag_selected_events(self, pos_delta):
        # Ensure initial positions are captured before calling this method
        for event in self.selected_events:
            initial_pos_x = self.initial_positions[event]
            new_pos_x = initial_pos_x + pos_delta.x()
            event.set_x_position(new_pos_x)

    def end_drag(self): # Call this method when the drag operation ends
        self.update_event_model(self.selected_events)
        self.initial_positions.clear()

    def update_event_model(self, events):
        for event in events:
            data = event.getData()
            current_frame = event.frame_num
            layer_name = event.parent_layer_name
            new_frame_x = int(data[0][0])
            # new_frame_y = int(data[1][0])
            print(f"[EventController][update_event_model] | Moving frame: {current_frame} ---> {new_frame_x}")
            self.model.loaded_stack.move_event(layer_name, current_frame, new_frame_x)  # new_frame_y=layer index | current_frame=current index | new_frame_x =new index
            event.frame_num = new_frame_x

    def handle_position_change(self, current_frame, event):
        new_frame_x = int(event.x())
        layer_name = event.parent_layer_name
        print(f"[EventController][handle_pos_change] | start position: {current_frame} | new x position: {new_frame_x}")
        self.model.loaded_stack.move_event(layer_name, current_frame, new_frame_x)  # new_frame_y=layer index | current_frame=current index | new_frame_x =new index

    def clear_selection(self):
        for selected_event in self.selected_events:
            selected_event.unselect() 

    def select_event(self, event):
        self.clear_selection()
        self.selected_events = []
        if event is not None:
            self.selected_events.append(event)
            event.select()
            layer_key = event.parent_layer_name
            print(f"[EventController][select_event] | Selected event:\n-->layer '{layer_key}'\n-->frame number '{event.frame_num}'")
            event_item = self.model.loaded_stack.layers[layer_key].get_event(event.frame_num)
            self.view.main_window.event_properties_widget.update(event_item)

    def add_event_to_selection(self, event):
        if event not in self.selected_events:
            self.selected_events.append(event)
            event.select()
            layer_key = event.parent_layer_name
            print(f"[EventController][add_event_to_selection] | Added event to selection:\n-->layer '{layer_key}'\n-->frame number '{event.frame_num}'")
            event_item = self.model.loaded_stack.layers[layer_key].get_event(event.frame_num)
            self.view.main_window.event_properties_widget.update(event_item)

    def select_roi_events(self, events):
        for event in events:
            self.add_event_to_selection(event)

    def edit_event(self, layer_name, frame_number): # This function edits an event
        print(f"[EventController][edit_event] | Editing event \n layer '{layer_name}'")
        model_object = self.model.loaded_stack.get_event_data(layer_name, frame_number)
        self.editor = EventEditorWidget(model_object)
        self.editor.changes_saved.connect(self.main_controller.layer_controller.refresh_plot_data_item)
        self.editor.exec_()

    def clear_plot_events(self):
        for layer_name, layer in self.model.loaded_stack.layers.items():
            # print(f"[EventController][clear_all_events] | iterating thru layer '{layer_name}'")
            for event_number, event in layer.objects.items():
                print(f"[EventController][clear_plot_events] | Clearing layer '{layer_name}' event '{event.frame_number}'")
                self.layer_widget.remove_item(event.plot_data_item)
        pass

