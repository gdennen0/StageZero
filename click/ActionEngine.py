from PyQt5.QtCore import Qt, QPointF
from pyqtgraph import RectROI
from view.LayerPlotItem import LayerPlotItem

class Action:
    def __init__(self, main_controller):
        self.status = main_controller.playback_mode_controller.get_current_mode()
        self.stack = StackAction(main_controller)

class StackAction:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.layer_widget = main_controller.view.main_window.stage_widget.stack.layer_widget

        self.event = EventAction(main_controller)
        self.layer = LayerAction(main_controller)
        self.connect_layer_signal(self.layer_widget.layer_plot)

    def connect_event_signal(self, plot_data_item):
        plot_data_item.sigEventClick.connect(self.main_controller.action.stack.event.click)
        plot_data_item.sigEventDrag.connect(self.main_controller.action.stack.event.drag)

    def connect_layer_signal(self, layer_plot):
        viewbox = layer_plot.getViewBox()
        viewbox.sigLayerDrag.connect(self.layer.roi_drag)
        viewbox.sigLayerClick.connect(self.layer.click)

class EventAction:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        pass

    def click(self, ev, object):
        if ev.button() == Qt.LeftButton and not ev.modifiers():
            self.main_controller.event_controller.select_event(object)
            ev.accept()

        if ev.button() == Qt.LeftButton and ev.modifiers() == Qt.ShiftModifier:
            self.main_controller.event_controller.add_event_to_selection(object)
            ev.accept()

        if ev.button() == Qt.RightButton:
            self.main_controller.event_controller.edit_event(object.parent_layer_name, object.frame_num)
            ev.accept()

    def drag(self, ev, object):
        if object in self.main_controller.event_controller.selected_events:
            if ev.button() == Qt.LeftButton:
                if ev.isStart():
                    # This block will only execute at the start of the drag
                    print("Drag Start")
                    object.dragOffset = object.points()[0].pos() - ev.buttonDownPos(
                        Qt.LeftButton
                    )
                    object.dragPoint = True
                    object.dragStart = ev.buttonDownPos()
                    self.main_controller.event_controller.start_drag()
                    ev.accept()

                if object.dragPoint:
                    new_pos = ev.pos() + object.dragOffset
                    pos_delta = new_pos - object.dragStart

                    print(f"New Pos {new_pos}, pos delta {pos_delta}")
                    self.main_controller.event_controller.drag_selected_events(pos_delta)
                    ev.accept()
                else:
                    pass
                    
                if ev.isFinish():
                    self.main_controller.event_controller.end_drag()
                    pass
            else:
                ev.ignore()

class LayerAction:
    def __init__(self, main_controller):
        self.main_controller = main_controller

    def click(self, ev, viewbox):
        if ev.button() == Qt.LeftButton and not ev.modifiers():
            self.main_controller.event_controller.clear_selection()
            print(f"cleared selection")
            # ev.accept()
        elif ev.button() == Qt.LeftButton and ev.modifiers() == Qt.ShiftModifier:
            # ev.accept()
            pass

    def roi_drag(self, ev, viewbox):
        print(f"EV {ev}, vb: {viewbox}")
        if ev.button() == Qt.LeftButton and ev.modifiers() == Qt.ShiftModifier:
            ev.accept()
            pos = ev.scenePos()
            if ev.isStart():
                # Drag start
                print(f"unmapped:{pos}")
                viewbox.dragStartPos =  viewbox.mapSceneToView(pos)
                print(f"mapped: { viewbox.dragStartPos}")
                viewbox.roi = RectROI([viewbox.dragStartPos.x(), viewbox.dragStartPos.y()], [1, 1], pen="w")
                viewbox.addItem(viewbox.roi)
            elif ev.isFinish():
                # Drag finish, select items within ROI
                self.get_items_in_roi(viewbox)
                viewbox.removeItem(viewbox.roi)
                viewbox.roi = None
                viewbox.dragStartPos = None
            else:
                # Drag update
                if viewbox.roi and viewbox.dragStartPos:
                    currentPos = viewbox.mapSceneToView(pos)
                    viewbox.roi.setSize(
                        [
                            currentPos.x() - viewbox.dragStartPos.x(),
                            currentPos.y() - viewbox.dragStartPos.y(),
                        ]
                    )
        else:
            # super(CustomViewBox, self).mouseDragEvent(ev, axis)
            pass

    def get_items_in_roi(self, viewbox):
        # Get the bounds of the ROI
        roi_bounds = viewbox.roi.mapRectToParent(viewbox.roi.boundingRect())
        print(f"ROI BOUNDS: {roi_bounds}")
        # List to hold items within the ROI
        selected_items = []

        # Iterate over all items in the ViewBox
        for item in viewbox.allChildren():
            # Check if the item is an instance of LayerPlotItem
            if isinstance(item, LayerPlotItem):
                data = item.getData()
                x_data, y_data = data
                if roi_bounds.contains(QPointF(x_data[0], y_data[0])):
                    # item.set_selected(True)
                    selected_items.append(item)

        print(f"Selected items: {selected_items}")
        self.main_controller.event_controller.select_roi_events(selected_items)
        # self.sigItemsSelected.emit(selected_items)

    # def clear_selection(self):
    #     for item in self.allChildren():
    #         if isinstance(item, LayerPlotItem):
    #             item.set_selected(False)