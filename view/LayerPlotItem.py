from pyqtgraph import PlotDataItem, mkPen
from PyQt5.QtCore import Qt, QPointF, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QPen, QHelpEvent, QColor
from PyQt5.QtWidgets import QGraphicsItem


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

from pyqtgraph import ScatterPlotItem
from PyQt5.QtWidgets import QToolTip


class LayerPlotItem(ScatterPlotItem):
    sigPositionChanged = pyqtSignal(int, QPointF)  # Signal emitting the new position
    sigPositionDrag = pyqtSignal(QPointF)
    sigMouseRightClicked = pyqtSignal(str, int)  # New signal for mouse click events
    sigEventSelected = pyqtSignal(object)
    sigAdditionalEventSelected = pyqtSignal(object)
    sigEventDragStart = pyqtSignal()
    sigEventDragEnd = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_layer_index = None
        self.parent_layer_name = None # Not implemented yet
        self.frame_num = None
        self.dragPoint = None
        self.dragOffset = None
        self.setFlag(
            QGraphicsItem.ItemIsFocusable, True
        )  # Allow the item to receive focus
        self.setFocus()  # Request focus

    def __str__(self):
        spot = self.points()[0]
        x, y = spot.pos()  # Get the x, y position
        size = spot.size()  # Get the size of the spot
        symbol = spot.symbol()  # Get the symbol
        brush = spot.brush().color().name()  # Get the brush (fill color)
        pen = spot.pen().color().name()  # Get the pen (outline)

        return f"Pos: (x:{x} y:{y}), Size: {size}, Symbol {symbol}, Brush: {brush}, Pen: {pen} "

    def refresh_tooltip_text(self):
        tooltip_text = f"Name: {self.name()} | Layer: {self.parent_layer_index} | Frame: {self.parent_layer_index}"
        self.setToolTip(tooltip_text)

    def set_frame_num(self, frame_num):
        print(f"set frame number: {frame_num}")
        self.frame_num = int(frame_num)
        self.refresh_tooltip_text()

    def set_layer_number(self, layer_number):
        self.layer_number = int(layer_number)
        self.refresh_tooltip_text()
    
    def set_layer_name(self, layer_name):
        self.parent_layer_name = layer_name
        self.refresh_tooltip_text()

    def mouseClickEvent(self, ev):
        if ev.button() == Qt.LeftButton and not ev.modifiers():
            print("LayerPlotItem Left Click")
            self.sigEventSelected.emit(self)
            ev.accept()
        if ev.button() == Qt.LeftButton and ev.modifiers() == Qt.ShiftModifier:
            print("LayerPlotItem Left Click + Shift")
            self.sigAdditionalEventSelected.emit(self)
            ev.accept()

        if ev.button() == Qt.RightButton:
            print("Right Click")
            self.sigMouseRightClicked.emit(
                self.parent_layer_name, self.frame_num
            )  # Emit the signal with the click position

    def mouseDragEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            if ev.isStart():
                # This block will only execute at the start of the drag
                print("Drag Start")
                self.dragOffset = self.points()[0].pos() - ev.buttonDownPos(
                    Qt.LeftButton
                )
                self.dragPoint = True
                self.dragStart = ev.buttonDownPos()
                self.sigEventDragStart.emit()
                ev.accept()

            if self.dragPoint:
                new_pos = ev.pos() + self.dragOffset
                pos_delta = new_pos - self.dragStart

                print(f"New Pos {new_pos}, pos delta {pos_delta}")
                self.sigPositionDrag.emit(pos_delta)
                ev.accept()

            if ev.isFinish():
                self.sigEventDragEnd.emit()
                pass
        else:
            ev.ignore()

    def select(self, selected=True):
        """Mark this item as selected and change the border color."""
        if selected:
            self.setPen(
                mkPen(QColor("orange"), width=2)
            )  # Change border color to orange
            print(f"selected event")
            print(self.frame_num)

    def unselect(self):
        self.setPen(mkPen(QColor("white"), width=1))
        print(f"unselected event")
        print({self.frame_num})

    def set_x_position(self, x_pos):
        """
        Set the x position of this object and move the event on the plot.
        :param pos_delta: The delta to add to the current x position.
        """
        if self.points():
            print(f"set x pos {x_pos}")
            data = self.getData()
            data[0][0] = x_pos  # Set the x position equal to x_pos
            self.setData(*data)

    def nudge_x_position(self, amount):
        print(f"nudge x pos {amount}")
        data = self.getData()
        original_pos = data[0][0] # Set the x position equal to x_pos
        new_pos = original_pos + amount
        data[0][0] = new_pos
        self.setData(*data)
            
    def set_y_position(self, y_pos):
        if self.points():
            print(f"set y pos {y_pos}")
            data = self.getData()
            data[1][0] = y_pos + .5 # Set the y position equal to y_pos
            self.setData(*data)

    def event(self, event):
        # print(f"Event type: {event.type()}")
        return super().event(event)
