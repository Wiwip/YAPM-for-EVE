from PyQt5.QtGui import QWindow, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow

from folder_browser import FolderModel
from interface.mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self, model: FolderModel):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = model

        # Creates the model for the origin combobox list view
        self.OriginListInstallationModel = QStandardItemModel(self.ui.comboBoxOriginSelection)
        self.ui.listViewOriginAccounts.setModel(self.OriginListInstallationModel)

        # Creates the model for the destination combobox list view
        self.DestinationListInstallationModel = QStandardItemModel(self.ui.comboBoxOriginSelection)

        self.refresh()
        self.connect_all()

    def refresh(self):
        self.populate_installations()
        self.update_profiles()

    def connect_all(self):
        self.ui.comboBoxOriginSelection.currentIndexChanged.connect(self.origin_combo_callback)

    def populate_installations(self):
        """
        Populates the combobox listing the installations
        :return:
        """
        for i in self.model.installations:
            self.ui.comboBoxOriginSelection.addItem(i)
            self.ui.comboBoxDestinationSelection.addItem(i)

    def update_profiles(self):
        """
        The methods updates the lists in the combobox for both origin and destination settings.
        :return:
        """
        self.ui.comboBoxOriginSettings.clear()
        install = self.model.get_install(self.ui.comboBoxOriginSelection.currentText())
        for i in install.profiles:
            self.ui.comboBoxOriginSettings.addItem(i.name)

        self.ui.comboBoxDestinationSettings.clear()
        install = self.model.get_install(self.ui.comboBoxDestinationSelection.currentText())
        for i in install.profiles:
            self.ui.comboBoxDestinationSettings.addItem(i.name)

    def origin_combo_callback(self, i):
        self.update_profiles()

    def origin_combo_callback(self, i):
        self.update_profiles()

    def update_users_combobox(self):
        """
        The methods updates the lists in the combobox for both origin and destination settings.
        :return:
        """
        pass
