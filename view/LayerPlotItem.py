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
    sigMouseRightClicked = pyqtSignal(int, int)  # New signal for mouse click events
    sigEventSelected = pyqtSignal(object)
    sigAdditionalEventSelected = pyqtSignal(object)
    sigEventDragStart = pyqtSignal()
    sigEventDragEnd = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer_index = None
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
        tooltip_text = f"Name: {self.name()} | Layer: {self.layer_index} | Frame: {self.layer_index}"
        self.setToolTip(tooltip_text)

    def set_frame_num(self, frame_num):
        print(f"set frame number: {frame_num}")
        self.frame_num = frame_num
        self.refresh_tooltip_text()

    def set_layer_index(self, layer_index):
        self.layer_index = layer_index
        self.refresh_tooltip_text()

    def mouseClickEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            print("Left Click")
            self.sigEventSelected.emit(self)
            ev.accept()
        if ev.button() == Qt.LeftButton and ev.modifiers() == Qt.ShiftModifier:
            print("Left Click + Shift")
            self.sigAdditionalEventSelected.emit(self)
            ev.accept()
        
        if ev.button() == Qt.RightButton:
            print("Right Click")
            self.sigMouseRightClicked.emit(
                self.layer_index, self.frame_num
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
    # def mouseDragEvent(self, ev):
    #     if ev.button() == Qt.LeftButton:
    #         if ev.isStart():
    #             # This block will only execute at the start of the drag
    #             print("Drag Start")
    #             self.dragOffset = self.points()[0].pos() - ev.buttonDownPos(
    #                 Qt.LeftButton
    #             )
    #             self.dragIndex = 0
    #             self.dragPoint = True
    #             self.dragStart = ev.buttonDownPos()
    #             ev.accept()

    #         if self.dragPoint:
    #             # This block executes throughout the drag after initialization
    #             # print("Dragging")
    #             newPos = ev.pos() + self.dragOffset
    #             if self.dragIndex is not None:
    #                 data = self.getData()
    #                 data[0][self.dragIndex] = newPos.x()
    #                 # data[1][self.dragIndex] = newPos.y()
    #                 self.setData(*data)
    #             ev.accept()

    #         if ev.isFinish():
    #             # print(f"Finished Drag {ev.lastPos()}")
    #             newPos = ev.lastPos()
    #             newPos.setX(round(newPos.x()))

    #             self.sigPositionChanged.emit(self.frame_num, newPos)
    #             self.set_x_position(newPos.x())
    #     else:
    #         ev.ignore()

    # def mouseDragEvent(self, ev):
    #     if ev.button() == Qt.LeftButton:
    #         if self.isSelected:  # Assuming isSelected is a property that indicates if the item is selected
    #             if ev.isStart():
    #                 # This block will only execute at the start of the drag
    #                 self.dragOffset = self.pos() - ev.buttonDownPos(Qt.LeftButton)
    #                 ev.accept()

    #             if ev.isFinish():
    #                 # At the end of the drag, update the position for all selected items
    #                 newPos = ev.pos() + self.dragOffset
    #                 self.updatePositionForAllSelected(newPos)
    #                 ev.accept()
    #             else:
    #                 # During the drag, we don't do anything because we'll move all items at once at the end
    #                 ev.ignore()
    #         else:
    #             # If the item is not selected, ignore the drag event
    #             ev.ignore()
    #     else:
    #         ev.ignore()

    # def updatePositionForAllSelected(self, newPos):
    #     # This method should move all selected items to the new position.
    #     # You'll need to adjust this logic based on how you track selected items.
    #     # for item in self.getAllSelectedItems():  # You need to implement this method
    #     #     item.setPos(newPos)
    #     #     item.sigPositionChanged.emit(item.frame_num, newPos)  # Emit position changed signal
    #     pass

    # def getAllSelectedItems(self):
    #     # This method should return a list of all selected LayerPlotItems.
    #     # Implementation depends on how you're tracking selected items.
    #     # For example, this could be a class method that checks a static list of all items,
    #     # or it might query a parent or controller object that tracks selected items.
    #     pass

    # def set_selected(self, selected=True):
    #     """Mark this item as selected and change the border color."""
    #     if selected:
    #         self.setPen(mkPen(QColor("orange"), width=2))  # Change border color to orange
    #     else:
    #         self.setPen(mkPen(QColor("w"), width=1))  # Change back to default or previous color
    #     self.enable_dragging(selected)
    def select(self, selected=True):
        """Mark this item as selected and change the border color."""
        if selected:
            self.setPen(mkPen(QColor("orange"), width=2))  # Change border color to orange
        else:
            self.setPen(mkPen(QColor("w"), width=1))  # Change back to default or previous color
        # self.enable_dragging(selected)

    def enable_dragging(self, enable=True):
        """Enable or disable dragging for this item."""
        self.setFlag(QGraphicsItem.ItemIsMovable, enable)

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
            self.frame_num = x_pos  # Update frame_num accordingly
            # self.setPos(x_pos, self.pos().y())  # Update position
            # self.update()  # Refresh the item

    def event(self, event):
        # print(f"Event type: {event.type()}")
        return super().event(event)
