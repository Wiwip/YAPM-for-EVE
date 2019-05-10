import sys
from PyQt5.QtWidgets import QApplication
from interface.mainwindow_implementation import MainWindow
from profile_manager.folder_browser import EVEWalker, FolderModel
from interface.mainwindow import Ui_MainWindow


def main():
    model = FolderModel()

    walker = EVEWalker(model)
    walker.generate()

    app = QApplication(sys.argv)
    window = MainWindow(model)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



