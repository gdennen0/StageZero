from pyqtgraph import PlotDataItem
from PyQt5.QtCore import Qt



"""
Module: ClickablePlotDataItem

This module defines the ClickablePlotDataItem class, which is a subclass of the PlotDataItem class from pyqtgraph.
The ClickablePlotDataItem class is designed to handle mouse click events on a plot data item in a PyQt5 application.

Arguments: 
*args, **kwargs - These are arbitrary argument lists and keyword-argument dictionaries respectively. They are used to allow the passing of any number of arguments and keyword arguments from the function call to the parent constructor.

Returns: 
This module does not return any value. It defines a class that can be instantiated to create objects that handle mouse click events on plot data items.

The ClickablePlotDataItem class has a constructor method (__init__) that calls the parent constructor to initialize the object. 
It also has a method (mouseClickEvent) that handles mouse click events. If the left mouse button is clicked, the event is accepted and a message is printed.
"""


class ClickablePlotDataItem(PlotDataItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call the parent constructor

    def mouseClickEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            ev.accept()  # Accept the event
            print("PlotDataItem clicked")  # Print a message
