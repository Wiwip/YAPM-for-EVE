import logging
import subprocess

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QComboBox

import copy_manager
import data
import eve_backup
from application import ProfileManager
from data import Profile
from eve_utils import get_eve_path
from interface.mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self, manager: ProfileManager):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.manager = manager
        self.model = manager.model

        # Creates the model for the origin combobox list view
        self.server_origin_model = QStandardItemModel()
        self.profile_origin_model = QStandardItemModel()
        self.account_origin_model = QStandardItemModel()
        self.ui.comboBoxOriginInstalls.setModel(self.server_origin_model)
        self.ui.comboBoxOriginProfiles.setModel(self.profile_origin_model)
        self.ui.listViewOriginAccounts.setModel(self.account_origin_model)

        # Creates the model for the destination combobox list view
        self.server_dest_model = QStandardItemModel()
        self.profile_dest_model = QStandardItemModel()
        self.account_dest_model = QStandardItemModel()
        self.ui.comboBoxDestinationInstalls.setModel(self.server_dest_model)
        self.ui.comboBoxDestinationProfiles.setModel(self.profile_dest_model)
        self.ui.listViewDestinationAccounts.setModel(self.account_dest_model)

        self.model.active_origin_server = self.model.get_default_server()
        self.model.active_dest_server = self.model.get_default_server()
        self.model.active_origin_profile = self.model.active_origin_server.get_default()
        self.model.active_dest_profile = self.model.active_dest_server.get_default()

        self.refresh()
        self.connect_all()

    def refresh(self):
        """

        :return:
        """
        self.populate_servers()

        # Populate the profiles on refresh calls
        self.populate_profiles(self.profile_origin_model, self.ui.comboBoxOriginProfiles,
                               self.model.active_origin_server, self.model.active_origin_profile)
        self.populate_profiles(self.profile_dest_model, self.ui.comboBoxDestinationProfiles,
                               self.model.active_origin_server, self.model.active_dest_profile)

        # Populate the user accounts on refresh calls)
        self.populate_accounts(self.account_origin_model, self.model.active_origin_profile)
        self.populate_accounts(self.account_dest_model, self.model.active_dest_profile, checkable=True)

    def clear_models(self):
        self.server_origin_model.clear()
        self.profile_origin_model.clear()
        self.account_origin_model.clear()

        self.server_dest_model.clear()
        self.profile_dest_model.clear()
        self.account_dest_model.clear()

    def connect_all(self):
        # Callback for installations
        self.ui.comboBoxOriginInstalls.currentIndexChanged.connect(self.origin_install_combo_callback)
        self.ui.comboBoxDestinationInstalls.currentIndexChanged.connect(self.dest_install_combo_callback)

        # Callback for profiles
        self.ui.comboBoxOriginProfiles.currentIndexChanged.connect(self.origin_profile_combo_callback)
        self.ui.comboBoxDestinationProfiles.currentIndexChanged.connect(self.dest_profile_combo_callback)

        self.ui.actionBackup_Tranquility.triggered.connect(self.backup_tranquility)
        self.ui.actionRestore_Tranquility.triggered.connect(self.restore_tranquility)
        self.ui.actionOpen_EVE_data_location.triggered.connect(self.open_eve_folder)
        self.ui.pushButtonCopy.clicked.connect(self.copy_cb)
        self.ui.actionRefresh.triggered.connect(self.manual_refresh)
        self.ui.pushButtonSelectAll.clicked.connect(self.select_all)
        self.ui.pushButtonDeselectAll.clicked.connect(self.deselect_all)
        self.manager.char_name_svc.notify_update.connect(self.on_char_updates)

    def populate_servers(self):
        """
        Populates the combobox listing the installations
        :return:
        """
        # Add data for all servers
        for i in self.manager.model.servers:
            # If the data isn't already in the model, add it.
            if not self.ui.comboBoxOriginInstalls.findData(self.manager.model.servers[i]) >= 0:
                item = QStandardItem(self.manager.model.servers[i].pretty_name)
                item.setData(self.manager.model.servers[i], QtCore.Qt.UserRole)
                self.server_origin_model.appendRow(item)

            if not self.ui.comboBoxDestinationInstalls.findData(self.manager.model.servers[i]) >= 0:
                item = QStandardItem(self.manager.model.servers[i].pretty_name)
                item.setData(self.manager.model.servers[i], QtCore.Qt.UserRole)
                self.server_dest_model.appendRow(item)

        # Restore the index
        index = self.ui.comboBoxOriginInstalls.findData(self.model.active_origin_server)
        if index >= 0:
            self.ui.comboBoxOriginInstalls.blockSignals(True)
            self.ui.comboBoxOriginInstalls.setCurrentIndex(index)
            self.ui.comboBoxOriginInstalls.blockSignals(False)

        # Restore the index
        index = self.ui.comboBoxDestinationInstalls.findData(self.model.active_dest_server)
        if index >= 0:
            self.ui.comboBoxDestinationInstalls.blockSignals(True)
            self.ui.comboBoxDestinationInstalls.setCurrentIndex(index)
            self.ui.comboBoxDestinationInstalls.blockSignals(False)

    def populate_profiles(self, model: QStandardItemModel, combobox: QComboBox,
                          server: data.Server, profile: data.Profile):
        """
        The methods updates the lists in the combobox for both origin and destination settings.
        :return:
        """
        # Populates the dropdown
        try:
            for i in server.profiles:
                if not combobox.findData(server.profiles[i]) >= 0:
                    item = QStandardItem(i)
                    item.setData(server.profiles[i], QtCore.Qt.UserRole)
                    model.appendRow(item)

            # Restore the index if the text still exists
            index = combobox.findData(profile)
            if index >= 0:
                combobox.blockSignals(True)
                combobox.setCurrentIndex(index)
                combobox.blockSignals(False)
        except AttributeError as e:
            print("No profile selected. {}".format(e))

    def populate_accounts(self, list_model: QStandardItemModel, profile: Profile, checkable=False):
        """
        The methods updates the lists in the combobox for both origin and destination settings.
        :param checkable: Can the accounts be checked?
        :param profile: The active profile where we'll get the user list to populate
        :param list_model: The Qt item model we'll be adding the items to
        :return: None
        """
        list_model.clear()

        try:
            for i in profile.accounts:
                item = QStandardItem(i.name)
                item.setCheckable(checkable)
                item.setEditable(False)
                item.setData(i, QtCore.Qt.UserRole)
                list_model.appendRow(item)

        # Catch error if profile is empty. Ignore.
        except TypeError as e:
            print("Type error. {}".format(e))
        except AttributeError as e2:
            print("Attribute error. {}".format(e2))

    def origin_install_combo_callback(self, i):
        """
        Callback coming from changing the server in the UI
        :param i: The new index
        :return: None
        """
        index = self.ui.comboBoxOriginInstalls.currentIndex()
        item = self.ui.comboBoxOriginInstalls.itemData(index, QtCore.Qt.UserRole)
        self.model.active_origin_server = item

        # If servers were changed, clear profiles before repopulating
        self.profile_origin_model.clear()
        self.populate_profiles(self.profile_origin_model, self.ui.comboBoxOriginProfiles,
                               self.model.active_origin_server, self.model.active_origin_profile)

    def dest_install_combo_callback(self, i):
        item = self.ui.comboBoxDestinationInstalls.currentData(QtCore.Qt.UserRole)
        self.model.active_dest_install = item

        # Clear model if manually changed
        self.profile_dest_model.clear()
        self.populate_profiles(self.profile_dest_model, self.ui.comboBoxDestinationProfiles,
                               self.model.active_dest_install, self.model.active_dest_profile)

    def origin_profile_combo_callback(self, i):
        item = self.ui.comboBoxOriginProfiles.currentData(QtCore.Qt.UserRole)
        self.model.active_origin_profile = item

        # Clear accounts manually if profiles were changed
        self.account_origin_model.clear()
        self.populate_accounts(self.account_origin_model,
                               self.manager.model.active_origin_profile)

    def dest_profile_combo_callback(self, i):
        item = self.ui.comboBoxDestinationProfiles.currentData(QtCore.Qt.UserRole)
        self.model.active_dest_profile = item

        # Clear accounts manually if profiles were changed
        self.account_dest_model.clear()
        self.populate_accounts(self.account_dest_model,
                               self.model.active_dest_profile,
                               checkable=True)

    def backup_tranquility(self):
        eve_backup.backup_eve_information('Tranquility Backup')

    def restore_tranquility(self):
        eve_backup.restore_eve_information('Tranquility Backup')

    def select_all(self):
        for i in range(self.account_dest_model.rowCount()):
            item = self.account_dest_model.item(i)
            item.setCheckState(2)

    def deselect_all(self):
        for i in range(self.account_dest_model.rowCount()):
            item = self.account_dest_model.item(i)
            item.setCheckState(0)

    def copy_cb(self):
        dest_files = []

        origin = self.account_origin_model.itemFromIndex(self.ui.listViewOriginAccounts.currentIndex())
        origin_character = origin.data().path
        logging.info("Copying users using source {} character".format(origin_character))

        for i in range(self.account_dest_model.rowCount()):
            item = self.account_dest_model.item(i)
            if item.checkState():
                dest_files.append(item.data().path)

        copy_manager.copy_files(origin_character, dest_files)

    def open_eve_folder(self):
        subprocess.Popen(r'explorer /select,"{}"'.format(get_eve_path()))

    def manual_refresh(self):
        # self.reset_models()
        self.refresh()

    @pyqtSlot()
    def on_char_updates(self):
        # self.reset_models()
        self.refresh()
