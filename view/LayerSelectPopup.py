from PyQt5.QtWidgets import QDialog, QListWidget, QVBoxLayout, QPushButton

def open_layer_selection_popup(layer_names):
    layer_selection_dialog = QDialog()
    layer_selection_dialog.setWindowTitle('Select a Layer')
    popup_layout = QVBoxLayout(layer_selection_dialog)
    # This method now creates a standalone dialog for layer selection
    layer_list_widget = QListWidget()
    layer_list_widget.addItems(layer_names)

    # Create and add the accept button at the bottom of the dialog
    accept_button = QPushButton("Accept")
    layer_selection_dialog.accept_button = accept_button  # Set the accept_button as an attribute of layer_selection_dialog
    layer_selection_dialog.layer_list_widget = layer_list_widget  # Expose the layer_list_widget

    popup_layout.addWidget(layer_list_widget)
    popup_layout.addWidget(accept_button)
    layer_selection_dialog.setLayout(popup_layout)
    

    return layer_selection_dialog
