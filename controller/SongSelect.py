
"""
Module: SongSelectController

This module is responsible for managing the song selection process in the application. It provides a dropdown menu for the user to select a song from the available options. 
The SongSelectController class is initialized with a reference to the main controller, which is used to access the view and model components of the application. 
The selected song is stored in the 'selected_song' attribute.

The 'connect_signals' method connects the UI signals to the appropriate slots in this controller. 
The 'generate_dropdown_items' method populates the dropdown menu with the available songs. 
The 'on_song_selected' method handles the event when a song is selected from the dropdown menu. 
The 'update_dropdown' method clears and repopulates the dropdown menu.

Arguments:
    main_controller: A reference to the main controller of the application.

Returns:
    None
"""



class SongSelectController:
    def __init__(self, main_controller):
        self.main_controller = main_controller  # Assigning main controller reference
        self.view = main_controller.view  # Assigning view reference
        self.model = main_controller.model  # Assigning model reference
        self.selected_song = None
        self.generate_dropdown_items()  # Generating the dropdown items
        self.connect_signals()  # Connecting the UI signals to slots in this controller

    def connect_signals(self):
        self.view.main_window.song_select_menu.song_selector.currentIndexChanged.connect(
            self.on_song_selected
        )  # Connecting the song_selector currentIndexChanged signal to the on_song_selected method
        self.view.main_window.song_select_menu.add_new_song.clicked.connect(
            self.main_controller.song_controller.add_song
        )  # Connecting the add_new_song clicked signal to the add_song method in the song controller

    def generate_dropdown_items(self):
        # Add the selected song to the dropdown menu
        if self.model.loaded_song != None:  # Checking if a song is loaded, if its not loaded dont proceed
            self.view.main_window.song_select_menu.song_selector.addItem(
                self.model.song.loaded_song
            )  # Adding the loaded song to the song_selector dropdown menu so it is at the top of the menu
        # add the remaining songs to the dropdown menu
        for song_name in self.model.song.objects:  # Iterating over the model song objects
            if song_name != self.model.loaded_song.name:  # Checking if the song is not the loaded song because we already loaded that
                self.view.main_window.song_select_menu.song_selector.addItem(song_name)  # Adding the song to the song_selector dropdown menu

    def on_song_selected(self, index):
        # Handle what happens when a song is selected
        if index == -1:  # Checking if the index is -1 (if the song_selector does not have any items in it)
            return  # If the index is -1, return
        selected_song = self.view.main_window.song_select_menu.song_selector.itemText(
            index
        )  # Getting the selected songs name from the song_selector dropdown menu given the song_selector index
        if selected_song == self.model.loaded_song.name:
            return
        else:
            print(f"Selected song: {selected_song} index: {index}")  # Printing the selected song and index
            self.main_controller.song_controller.load_song(selected_song)  # Loading the selected song with the song_controller

    def update_dropdown(self):
        # Clear the dropdown
        self.view.main_window.song_select_menu.song_selector.clear()
        # Generate and place the dropdown Items
        self.generate_dropdown_items()