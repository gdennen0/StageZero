"""
Module: LayerItem

This module defines the LayerItem class which represents a layer in the application.
Each LayerItem object has the following attributes:
    - name: The name of the layer
    - event: An instance of the EventModel class

Arguments:
    - layer_name: A string representing the name of the layer. This is passed to the constructor of the LayerItem class.

Returns:
    - An instance of the LayerItem class with the specified layer name and an associated EventModel instance.

This module is part of the model layer of the application, and it works in conjunction with other model classes like StackModel and EventModel.
It is responsible for managing the data related to a single layer in the application. The LayerItem class provides a way to encapsulate the data and operations
related to a layer, making it easier to manage and manipulate layers in the application.
"""


from .EventModel import EventModel


class LayerItem:
    def __init__(self, layer_name):
        self.name = layer_name  # The name of the layer
        self.event = EventModel()  # The event model
