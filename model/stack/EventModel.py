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
    def __init__(self, name):
        self.objects = {}  # Dictionary to store event objects
        self.name = name
        self.layer_index = None

    def get_event(self, frame_number):
        if frame_number in self.objects:
            return self.objects[frame_number]
        else:
            print(f"could not locate event at frame; {frame_number}")
        
    def nudge_event(self, original_frame, amount):
        event = self.objects[original_frame]
        new_frame = original_frame + amount
        self.delete(original_frame)
        self.add(new_frame)
        event.frame_number = new_frame
        event.plot_data_item.frame_num = new_frame
        event.plot_data_item.nudge_x_position(amount)
        self.objects[new_frame] = event

    def set_index(self, layer_index):
        print(f"Setting layer index to {layer_index}")
        self.layer_index = layer_index

    def delete(self, frame_number):
        if frame_number in self.objects:
            del self.objects[frame_number]
            print(f"Frame number {frame_number} deleted from event objects.")
        else:
            print(f"No event object found for frame number {frame_number}. for delete")

    def add(self, frame_number):
        # adds an instance of EventItem to self.objects
        print(f"start list objects:")
        pprint(self.objects)
        if frame_number in self.objects and not None:
            print(
                f"Data already exists for frame number {frame_number}, frame not added"
            )
            return
        event = EventItem()
        event.parent_layer = self.name
        event.parent_layer_index = self.layer_index
        event.frame_number = frame_number
        self.objects[frame_number] = event  # Add an event item to the dictionary
        print(f"adding event at frame {frame_number}")
        print(f"end list objects:")
        pprint(self.objects)

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
