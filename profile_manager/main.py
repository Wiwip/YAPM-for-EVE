import logging
import sys

from PyQt5.QtWidgets import QApplication

from application import ProfileManager
from interface.mainwindow_implementation import MainWindow


def main():
    logging.basicConfig(format='%(levelname)s | %(message)s', level=logging.DEBUG)

    # Creates the application
    manager = ProfileManager()

    # Creates the UI
    app = QApplication(sys.argv)
    window = MainWindow(manager)

    try:
        window.show()
        sys.exit(app.exec_())
    finally:
        manager.quit()


if __name__ == '__main__':
    main()



