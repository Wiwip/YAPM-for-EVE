import logging

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QComboBox

import copy_manager
import eve_backup
from application import ProfileManager
from folder_browser import FolderProfiles
from interface.mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self, manager: ProfileManager):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.manager = manager

        # Creates the model for the origin combobox list view
        self.install_dropdown_model = QStandardItemModel()
        self.profile_dropdown_model = QStandardItemModel()
        self.OriginListInstallationModel = QStandardItemModel()
        self.ui.comboBoxOriginInstalls.setModel(self.install_dropdown_model)
        # self.ui.comboBoxOriginProfiles.setModel(self.profile_origin)
        self.ui.listViewOriginAccounts.setModel(self.OriginListInstallationModel)

        # Creates the model for the destination combobox list view
        self.DestinationListInstallationModel = QStandardItemModel()
        self.ui.listViewDestinationAccounts.setModel(self.DestinationListInstallationModel)

        self.refresh()
        self.connect_all()

    def refresh(self):
        self.populate_installations()

        self.manager.model.active_origin_install = self.manager.model.get_install(self.install_origin)
        self.manager.model.active_dest_install = self.manager.model.get_install(self.install_destination)

        # Populate the profiles on refresh calls
        self.populate_profiles(self.ui.comboBoxOriginProfiles, self.manager.model.active_origin_install)
        self.populate_profiles(self.ui.comboBoxDestinationProfiles, self.manager.model.active_origin_install)

        self.manager.model.active_origin_profile = self.manager.model.active_origin_install.get_profile(self.profile_origin)
        self.manager.model.active_dest_profile = self.manager.model.active_dest_install.get_profile(self.profile_destination)

        # Populate the user accounts on refresh calls)
        self.populate_accounts(self.OriginListInstallationModel, self.manager.model.active_origin_profile)
        self.populate_accounts(self.DestinationListInstallationModel, self.manager.model.active_dest_profile, checkable=True)

    def connect_all(self):
        # Callback for installations
        self.ui.comboBoxOriginInstalls.currentIndexChanged.connect(self.origin_install_combo_callback)
        self.ui.comboBoxDestinationInstalls.currentIndexChanged.connect(self.dest_install_combo_callback)

        # Callback for profiles
        self.ui.comboBoxOriginProfiles.currentIndexChanged.connect(self.origin_profile_combo_callback)
        self.ui.comboBoxDestinationProfiles.currentIndexChanged.connect(self.dest_profile_combo_callback)

        self.ui.actionBackup_Tranquility.triggered.connect(self.backup_tranquility)
        self.ui.actionRestore_Tranquility.triggered.connect(self.restore_tranquility)
        self.ui.pushButtonCopy.clicked.connect(self.copy_cb)
        self.ui.actionRefresh.triggered.connect(self.refresh)
        self.ui.pushButtonSelectAll.clicked.connect(self.select_all)
        self.ui.pushButtonDeselectAll.clicked.connect(self.deselect_all)
        self.manager.char_name_svc.notify_update.connect(self.on_char_updates)

    def populate_installations(self):
        """
        Populates the combobox listing the installations
        :return:
        """
        remember_origin = self.install_origin
        remember_destination = self.install_destination

        self.ui.comboBoxOriginInstalls.clear()
        self.ui.comboBoxDestinationInstalls.clear()

        for i in self.manager.model.installations:
            item = QStandardItem(i)
            item.setData(self.manager.model.installations[i])
            self.install_dropdown_model.appendRow(item)
            self.ui.comboBoxDestinationInstalls.addItem(i)  # TODO

        # Restore the index if the text still exists
        index = self.ui.comboBoxOriginInstalls.findText(remember_origin)
        if index >= 0:
            self.ui.comboBoxOriginInstalls.setCurrentIndex(index)

        # Restore the index if the text still exists
        index = self.ui.comboBoxDestinationInstalls.findText(remember_destination)
        if index >= 0:
            self.ui.comboBoxDestinationInstalls.setCurrentIndex(index)

    def origin_install_combo_callback(self, i):
        try:
            self.manager.model.active_origin_install = self.manager.model.get_install(self.install_origin)
            self.populate_profiles(self.ui.comboBoxOriginProfiles, self.manager.model.active_origin_install)
        except AttributeError:
            pass

    def dest_install_combo_callback(self, i):
        try:
            self.manager.model.active_dest_install = self.manager.model.get_install(self.install_destination)
            self.populate_profiles(self.ui.comboBoxDestinationProfiles, self.manager.model.active_dest_install)
        except AttributeError:
            pass

    def origin_profile_combo_callback(self, i):
        try:
            self.manager.model.active_origin_profile = self.manager.model.active_origin_install.get_profile(self.profile_origin)
            self.populate_accounts(self.OriginListInstallationModel, self.manager.model.active_origin_profile)
        except AttributeError:
            pass

    def dest_profile_combo_callback(self, i):
        try:
            self.manager.model.active_dest_profile = self.manager.model.active_dest_install.get_profile(self.profile_destination)
            self.populate_accounts(self.DestinationListInstallationModel, self.manager.model.active_dest_profile, checkable=True)
        except AttributeError:
            pass

    def populate_profiles(self, dropdown: QComboBox, install):
        """
        The methods updates the lists in the combobox for both origin and destination settings.
        :return:
        """
        # Remembers previous selection
        last_text = dropdown.currentText()

        # Populates the destination dropdown
        dropdown.clear()
        try:
            for i in install.profiles:
                dropdown.addItem(i)

            # Restore the index if the text still exists
            index = dropdown.findText(last_text)
            if index >= 0:
                dropdown.setCurrentIndex(index)
        except AttributeError as e:
            print("No profile selected. {}".format(e))

    def populate_accounts(self, list_model: QStandardItemModel, active_profile: FolderProfiles, checkable=False):
        """
        The methods updates the lists in the combobox for both origin and destination settings.
        :param active_profile: The active profile where we'll get the user list to populate
        :param list_model: The Qt item model we'll be adding the items to
        :param checked: Will the checked property be enabled
        :return: None
        """
        list_model.clear()

        try:
            for i in active_profile.users:
                item = QStandardItem(i.name)
                item.setCheckable(checkable)
                item.setEditable(False)
                item.setData(i)
                list_model.appendRow(item)

        # Catch error if profile is empty. Ignore.
        except TypeError:
            pass
        except AttributeError:
            pass

    def backup_tranquility(self):
        eve_backup.backup_eve_information('Tranquility Backup')

    def restore_tranquility(self):
        eve_backup.restore_eve_information('Tranquility Backup')

    def select_all(self):
        for i in range(self.DestinationListInstallationModel.rowCount()):
            item = self.DestinationListInstallationModel.item(i)
            item.setCheckState(2)

    def deselect_all(self):
        for i in range(self.DestinationListInstallationModel.rowCount()):
            item = self.DestinationListInstallationModel.item(i)
            item.setCheckState(0)

    def copy_cb(self):
        dest_files = []

        origin = self.OriginListInstallationModel.itemFromIndex(self.ui.listViewOriginAccounts.currentIndex())
        origin_character = origin.data().path
        logging.info("Copying users using source {} character".format(origin_character))

        for i in range(self.DestinationListInstallationModel.rowCount()):
            item = self.DestinationListInstallationModel.item(i)
            if item.checkState():
                dest_files.append(item.data().path)

        copy_manager.copy_files(origin_character, dest_files)

    @pyqtSlot()
    def on_char_updates(self):
        self.refresh()

    @property
    def install_origin(self):
        return str(self.ui.comboBoxOriginInstalls.currentText())

    @property
    def install_destination(self):
        return str(self.ui.comboBoxDestinationInstalls.currentText())

    @property
    def profile_origin(self):
        return str(self.ui.comboBoxOriginProfiles.currentText())

    @property
    def profile_destination(self):
        return str(self.ui.comboBoxDestinationProfiles.currentText())


