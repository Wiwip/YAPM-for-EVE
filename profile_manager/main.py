import sys

import logging
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication

from application import ProfileManager
from interface.mainwindow_implementation import MainWindow


def main():
    logging.basicConfig(format='%(levelname)s | %(message)s', level=logging.DEBUG)

    # Creates the application
    manager = ProfileManager()

    # Creates the UI
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    # engine.load('interface\ProfileManagerWindow.qml')

    window = MainWindow(manager)

    try:
        window.show()
        sys.exit(app.exec_())
    finally:
        manager.quit()
        pass


if __name__ == '__main__':
    main()



