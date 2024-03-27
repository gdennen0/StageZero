"""
Module: StackController

This module is responsible for managing the stack lifecycle in the application. It includes functionality to create, change, and get information about stacks.

Arguments:
    main_controller (object): A reference to the main controller of the application. This is used to access the model and view components of the MVC architecture.

Returns:
    None. This module is used for its side effects of manipulating the stack state in the model and updating the view accordingly.

The StackController class is initialized with a reference to the main controller. It uses this reference to access the model and view components of the application. The class provides methods to create a new stack, change the selected stack, get the currently loaded stack, and set the number of frames for a stack. These methods manipulate the stack state in the model and update the view accordingly.
"""
class StackController:
    def __init__(self, main_controller):
        # Initialize with references to main controller, model, and view
        self.main_controller = main_controller
        self.model = main_controller.model
        self.view = main_controller.view

    def create_stack(self, stack_name):
        # Create a new stack with the given name
        print(f"Creating stack {stack_name}")
        self.model.stack.create_stack(stack_name)
        self.set_stack_frame_qty(stack_name)

    def change_stack(self, stack_name):
        # Change the selected stack to the one with the given name
        self.model.stack.selected_stack = stack_name
        self.main_controller.layer_controller.init_plot(stack_name)

    def reload_stack(self):
        # Change the selected stack to the one with the given name
        self.main_controller.layer_controller.init_plot(self.model.loaded_stack.name)

    def get_loaded_stack(self):
        # Return the currently loaded stack
        return self.model.stack.loaded_stack

    def set_stack_frame_qty(self, stack_name):
        # Set the number of frames for the stack with the given name
        frame_qty = self.model.song.objects[stack_name].frame_qty
        self.model.stack.objects[stack_name].set_frame_qty(frame_qty)
