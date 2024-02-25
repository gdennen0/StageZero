from PyQt5.QtWidgets import QMessageBox


class PopupManager:
    @staticmethod
    def show_info(title, message, parent=None):
        QMessageBox.information(parent, title, message)

    @staticmethod
    def show_warning(title, message, parent=None):
        QMessageBox.warning(parent, title, message)

    @staticmethod
    def show_error(title, message, parent=None):
        QMessageBox.critical(parent, title, message)

    # Add more methods for different types of popups or custom dialogs as needed
