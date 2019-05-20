from PyQt5.QtGui import QWindow, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow

from folder_browser import FolderModel, FolderProfiles
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
        self.model.active_origin_install = self.model.get_install(str(self.ui.comboBoxOriginSelection.currentText()))
        self.model.active_dest_install = self.model.get_install(str(self.ui.comboBoxDestinationSelection.currentText()))

        self.populate_installations()
        self.populate_profiles()

    def connect_all(self):
        # Callback for installations
        self.ui.comboBoxOriginSelection.currentIndexChanged.connect(self.origin_install_combo_callback)
        self.ui.comboBoxDestinationSelection.currentIndexChanged.connect(self.dest_install_combo_callback)

        # Callback for profiles
        self.ui.comboBoxOriginSettings.currentIndexChanged.connect(self.origin_profile_combo_callback)
        self.ui.comboBoxDestinationSettings.currentIndexChanged.connect(self.dest_profile_combo_callback)

    def populate_installations(self):
        """
        Populates the combobox listing the installations
        :return:
        """
        for i in self.model.installations:
            self.ui.comboBoxOriginSelection.addItem(i)
            self.ui.comboBoxDestinationSelection.addItem(i)

    def origin_install_combo_callback(self, i):
        self.model.active_origin_install = self.model.get_install(str(self.ui.comboBoxOriginSelection.currentText()))
        self.populate_profiles()

    def dest_install_combo_callback(self, i):
        self.model.active_dest_install = self.model.get_install(str(self.ui.comboBoxDestinationSelection.currentText()))
        self.populate_profiles()

    def populate_profiles(self):
        """
        The methods updates the lists in the combobox for both origin and destination settings.
        :return:
        """
        # Populates the origin dropdown
        self.ui.comboBoxOriginSettings.clear()
        install = self.model.active_origin_install
        try:
            for i in install.profiles:
                self.ui.comboBoxOriginSettings.addItem(i)
        except AttributeError as e:
            print(e)

        # Populates the destination dropdown
        self.ui.comboBoxDestinationSettings.clear()
        install = self.model.active_dest_install
        try:
            for i in install.profiles:
                self.ui.comboBoxDestinationSettings.addItem(i)
        except AttributeError as e:
            print(e)

        # Update the characters specifics
        self.populate_accounts()

    def origin_profile_combo_callback(self, i):
        pass
        #self.model.active_origin_profile = self.model.active_origin_install.get_install(self.ui.comboBoxOriginSelection.currentText())

    def dest_profile_combo_callback(self, i):
        pass
        #self.model.active_dest_profile = self.model.active_dest_install.get_install(self.ui.comboBoxDestinationSelection.currentText())

    def populate_accounts(self):
        """
        The methods updates the lists in the combobox for both origin and destination settings.
        :return:
        """
        try:
            for i in self.model.active_origin_profile:
                pass
                #self.OriginListInstallationModel.appendRow(i)
        except TypeError:
            pass
