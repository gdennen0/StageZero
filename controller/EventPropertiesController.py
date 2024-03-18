class EventPropertiesController:
    # This class controls the events
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.stack = main_controller.model.stack
        self.model = main_controller.model
        self.view = main_controller.view
        # Connect to EventController's updatePropertiesWidget signal

        

