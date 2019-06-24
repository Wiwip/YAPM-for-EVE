import sys
import logging
from queue import Queue

from PyQt5.QtWidgets import QApplication

from esi.esi_queries import AsyncCharacterQueries
from interface.mainwindow_implementation import MainWindow
from profile_manager.folder_browser import EVEWalker, FolderModel, AccountFile, FolderProfiles


def main():
    logging.basicConfig(format='%(levelname)s| %(message)s', level=logging.DEBUG)

    shared_queue = Queue()
    shared_dict = {}

    AccountFile.names_dict = shared_dict
    FolderProfiles.shared_queue = shared_queue

    # Creates the model shared by all the app to share relevant data.
    model = FolderModel()
    model.character_names = shared_dict

    walker = EVEWalker(model)
    walker.generate()

    char_name_svc = AsyncCharacterQueries(shared_queue, shared_dict)
    char_name_svc.start()

    # Starts the UI
    app = QApplication(sys.argv)
    window = MainWindow(model)
    window.show()

    exit_code = app.exec_()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()



