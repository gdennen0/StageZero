import json
import os
from view.FilterEditorWindow import FilterEditorWindow

class FilterEditorController:
    def __init__(self):
        self.filter_editor_window = FilterEditorWindow()

    def connect_signals(self):
        self.filter_editor_window.filter_list_widget.itemSelectionChanged.connect(self.load_filter_properties)
        self.filter_editor_window.save_button.clicked.connect(lambda: (self.saveParametersToFile({
            "filter_name": self.filter_editor_window.filter_name_input.text(),
            "filter_type": self.filter_editor_window.filter_type_combo_box.currentText(),
            "cutoff_frequency": self.filter_editor_window.cutoff_frequency_input.text(),
            # Add more parameters as needed
        }), self.filter_editor_window.update_filter_list()))
        self.filter_editor_window.delete_button.clicked.connect(self.delete_filter)

    def load_filter_properties(self):
        file_name = self.filter_editor_window.filter_list_widget.currentItem().text()
        with open(f'filters/{file_name}', 'r') as file:
            properties = json.load(file)
        self.filter_editor_window.filter_name_input.setText(properties.get('filter_name', ''))
        self.filter_editor_window.filter_type_combo_box.setCurrentText(properties.get('filter_type', 'Low-pass'))
        self.filter_editor_window.cutoff_frequency_input.setText(properties.get('cutoff_frequency', ''))
        # Load more properties as needed

    def delete_filter(self):
        selected_item = self.filter_editor_window.filter_list_widget.currentItem()
        if selected_item:
            os.remove(f'filters/{selected_item.text()}')
            self.filter_editor_window.update_filter_list()

    def saveParametersToFile(self, params):
        # Logic to save parameters to a file in the filter folder with the filter_name as the file name
        file_name = params.get('filter_name', 'default_filter') + '.json'  # Default to 'default_filter.json' if no name is provided
        with open(f'filters/{file_name}', 'w') as file:
            json.dump(params, file)

    def open(self):
            self.filter_editor_window.show() 
            self.connect_signals()