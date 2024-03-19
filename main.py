import sys
from model import MainModel
from view import MainView
from controller import MainController

from PyQt5.QtWidgets import (
    QApplication,
)

from stylesheet import global_stylesheet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainController(MainModel(), MainView())
    main.initialize_app()

    app.setStyleSheet(global_stylesheet)
    sys.exit(app.exec_())
