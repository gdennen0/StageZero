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

from view.LayerPlotItem import LayerPlotItem
import pyqtgraph as pg
from PyQt5.QtGui import QColor


class EventItem:
    def __init__(self, event_name="Default", color=(255, 255, 255)):
        self.frame_number = None
        self.parent_layer_name = None
        self.parent_layer_number = None
        self.event_name = event_name  # The name of the event
        self.color = color  # The color of the event
        self.plot_data_item = None

    def to_dict(self):
        return {
            "frame_number": self.frame_number,
            "parent_layer_name": self.parent_layer_name,
            "parent_layer_number": self.parent_layer_number,
            "name": self.event_name,
            "color": str(self.color),
            # Exclude "plot_data_item" from serialization
        }

    def deserialize(self, data):
        self.frame_number = data.get("frame_number")
        self.parent_layer_name = data.get("parent_layer_name")
        self.parent_layer_number = data.get("parent_layer_number")
        self.event_name = data.get("name")
        self.generate_layer_plot_item()
        color_str = data.get("color", "(100, 100, 100)")
        self.set_color(color_str)

    def set_color(self, color):
        # Gobbles up either #HEX or RGB values
        if color.startswith("#"):  # Check if color is in hex format
            color = color.lstrip("#")
            try:
                self.color = tuple(
                    int(color[i : i + 2], 16) for i in (0, 2, 4)
                )  # Convert hex to RGB
                self.plot_data_item.setBrush(self.color)
            except ValueError:
                raise ValueError("Invalid hex color format")
        elif "," in color:  # Check if color is in "255,255,255" string format
            try:
                self.color = tuple(map(int, color.strip("()").split(",")))
                self.plot_data_item.setBrush(self.color)
            except ValueError:
                raise ValueError("Invalid RGB string format")
        else:
            raise ValueError(
                "Color must be in hex (#RRGGBB) or RGB (255,255,255) format"
            )

    def set_frame_number(self, frame_number):
        if not isinstance(frame_number, int):
            raise ValueError("Frame number must be an integer")
        self.frame_number = frame_number

    def set_parent_layer_number(self, parent_layer_number):
        self.parent_layer_number = parent_layer_number
        print(f"set parent layer index to {parent_layer_number}")

    def set_parent_layer_name(self, parent_layer_name):
        self.parent_layer_name = parent_layer_name
        print(f"set parent layer name to '{parent_layer_name}'")

    def update_pdi(self):
        self.plot_data_item = self.generate_layer_plot_item()

    def delete_pdi(self):
        self.plot_data_item = None

    def generate_layer_plot_item(self):
        # translates model data to layerPlotItem
        self.plot_data_item = self.create_point(
            self.event_name, self.frame_number, self.parent_layer_name, self.parent_layer_number, self.color
        )


    def create_point(self, event_name, frame_num, parent_layer_name, parent_layer_number, color):
        adj_layer_number = parent_layer_number + 0.5
        print(f"create_point, color {color}")
        plot_point = LayerPlotItem(
            x=[frame_num],
            y=[adj_layer_number],
            symbol="d",
            brush=pg.mkBrush(color),
            pen=pg.mkPen(QColor("white"), width=1),
            hoverable=True,
            hoverPen=pg.mkPen("orange"),
            size=12,
            name=event_name,
        )
        plot_point.set_frame_num(frame_num)
        plot_point.set_layer_name(parent_layer_name)
        plot_point.set_layer_number(parent_layer_number)
        return plot_point
