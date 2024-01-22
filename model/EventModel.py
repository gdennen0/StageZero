

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

class EventModel:
    def __init__(self, name):
        self.objects = {}  # Dictionary to store event objects
        self.plot_data_item = None  # The plot data item
        self.name = name
        
    def add(self, frame_number):
        # adds an instance of EventItem to self.objects
        if frame_number in self.objects:
            print(f"Data already exists for frame number {frame_number}, frame not added")
            return
        self.objects[frame_number] = EventItem()  # Add an event item to the dictionary