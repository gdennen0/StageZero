

"""
Module: EventItem

This module defines the EventItem class which represents an event in the application.
Each EventItem object has the following attributes:
    - name: The name of the event
    - color: The color of the event in RGB format

Arguments:
    - event_name: A string representing the name of the event. Default is "Default".
    - color: A tuple representing the color of the event in RGB format. Default is (255,255,255).

Returns:
    - An instance of EventItem with the given name and color.

"""


class EventItem:
    def __init__(self, event_name="Default", color=(255,255,255)):
        self.name = event_name  # The name of the event
        self.color = color  # The color of the event
