"""
Module: EventModel

This module defines the EventModel class which represents an event in the application.
Each event has a name and an associated dictionary of event objects, and a plot data item.

Arguments:
    - name: The name of the event

Returns:
    - An instance of EventModel with the given name, an empty dictionary for storing event objects, and a None value for plot data item.

The EventModel class provides a method to add event items to its dictionary of objects. Each event item is an instance of the EventItem class.
"""

from .EventItem import EventItem
from pprint import pprint


class EventModel:
    def __init__(self):
        self.objects = {}  # Dictionary to store event objects
        self.layer_name = None
        self.layer_number = None

    def get_event(self, frame_number):
        if frame_number in self.objects:
            return self.objects[frame_number]
        else:
            print(f"[EventModel][get_event] | could not locate event at frame '{frame_number}'")
        
    def nudge_event(self, original_frame, amount):
        event = self.objects[original_frame]
        new_frame = original_frame + amount
        self.delete(original_frame)
        self.add(new_frame)
        event.frame_number = new_frame
        event.plot_data_item.frame_num = new_frame
        event.plot_data_item.nudge_x_position(amount)
        self.objects[new_frame] = event
        
    def set_layer_name(self, layer_name):
        self.layer_name = layer_name

    def set_layer_number(self, number):
        print(f"[EventModel][set_layer_number] | Setting layer number to {number}")
        self.layer_number = number

    def delete(self, frame_number):
        if frame_number in self.objects:
            del self.objects[frame_number]
            print(f"[EventModel][delete] | Frame number {frame_number} deleted from event objects.")
        else:
            print(f"[EventModel][delete] | No event object found for frame number {frame_number}. for delete")

    def add(self, frame_number, color=None, name=None, type="event"):
        if type=="event":
            if frame_number in self.objects and not None:
                print(f"[EventModel][add] | Data already exists for frame number '{frame_number}', frame not added")
                return
            event = EventItem()
            event.set_parent_layer_name(self.layer_name)
            event.set_parent_layer_number(self.layer_number)
            event.set_frame_number(frame_number)
            if color:
                event.set_color(color)
            if name:
                event.set_name(name)

            self.objects[frame_number] = event  # Add an event item to the dictionary
            print(f"[EventModel][add] | Adding EventItem instance at frame '{frame_number}'")

    def update_data(self, frame_number, data):
        if frame_number not in self.objects:
            print(f"no frame exists at frame: {frame_number}")
            return
        self.objects[frame_number] = data
        self.objects[frame_number].frame_number = frame_number
        print(f"attempting to update frame {frame_number} data")

    def generate_plot_layer_data_items(self):
        for event_key, event in self.objects.items():
            event.generate_layer_plot_item()

    def get_plot_layer_data(self):
        plot_layer_objects = [event.plot_data_item for event in self.objects.values()]
        return plot_layer_objects
