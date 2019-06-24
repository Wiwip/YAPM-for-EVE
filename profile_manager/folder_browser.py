import logging
import os
import re
import eve_utils as utils


class EVEWalker:

    ignored_folder = ['Launcher', 'QtWebEngine', 'cache', 'Browser']
    appdata = utils.get_appdata()
    eve_path = utils.get_eve_path()

    def __init__(self, model):
        self.model = model

    def generate(self):
        for folder in os.listdir(self.eve_path):
            path = os.path.join(self.eve_path, folder)

            if os.path.isfile(path):
                continue  # Not a folder, we don't care here

            if self.is_folder_ignored(folder):
                continue  # Is ignored? Nothing to see here.

            print(folder)

            temp = FolderInstall(folder, path)
            temp.find_profiles()
            self.model.add_installation_directory(temp)

    def is_folder_ignored(self, folder):
        """
        Looks in the ignored_folder table to figure if the folder is to be ignored or not.
        :param folder: The folder name to verify against.
        :return: True or False
        """
        if folder in self.ignored_folder:
            return True
        else:
            return False

    @property
    def walk(self):
        return os.walk(self.eve_path)


class FolderInstall:
    """
    Class the represents the different installations within the game.
    """

    ignored_folders = ['cache']

    def __init__(self, name, path):
        """
        Constructor for the installation class.
        :param name: The name of the installation
        :param path: The full path to the installation
        """
        self.path = path
        self.name = name
        self.profiles = {}

    def find_profiles(self):
        for folder in os.listdir(self.path):
            path = os.path.join(self.path, folder)

            if os.path.isfile(path):
                continue  # Not a folder, we don't care here

            if self.is_folder_ignored(folder):
                continue  # Is ignored? Nothing to see here.

            print('  {}'.format(folder))

            temp = FolderProfiles(path, folder)
            temp.find_accounts()
            self.profiles[folder] = temp

    def get_profile(self, text):
        """
        Returns the requested profile from the installation
        :param text:
        :return:
        """
        try:
            return self.profiles[text]
        except KeyError:
            return None

    def is_folder_ignored(self, folder):
        """
        Looks in the ignored_folder table to figure if the folder is to be ignored or not.
        :param folder: The folder name to verify against.
        :return: True or False
        """
        if folder in self.ignored_folders:
            return True
        else:
            return False


class FolderProfiles:
    """
    Class that represent the different profiles that can be used to launch the game.
    """

    shared_queue = None

    def __init__(self, path, name):
        """

        :param path:
        :param name:
        """
        self.path = path
        self.name = name
        self.users = []
        self.accounts = []

    def find_accounts(self):
        for file in os.listdir(self.path):
            path = os.path.join(self.path, file)

            if os.path.isdir(path):
                continue  # Not a file, we don't care here

            acc_file = AccountFile(file, path)

            if acc_file.is_account:
                self.accounts.append(acc_file)

            if acc_file.is_character:
                self.shared_queue.put(acc_file.char_id)
                self.users.append(acc_file)

            print('    {}'.format(file))


class AccountFile:

    names_dict = None

    def __init__(self, name, path):
        self._fullname = name
        self.path = path

    @property
    def is_account(self):
        m = re.findall("core_user_(\d+)", self._fullname)
        if m:
            return True
        return False

    @property
    def is_character(self):
        m = re.findall("core_char_(\d+)", self._fullname)
        if m:
            return True
        return False

    @property
    def char_id(self):
        try:
            m = re.findall("\d+", self._fullname)
            return m[0]
        except IndexError:
            pass
        return self._fullname

    @property
    def name(self):
        try:
            return "{} ({})".format(self.names_dict[self.char_id], self.char_id)
        except KeyError:
            logging.warning("Character ID ({}) could not be found.".format(self._fullname))
        except ValueError:
            pass
        return self._fullname


class FolderModel:

    def __init__(self):
        self.installations = {}

        # Active installations
        self.active_origin_install = None
        self.active_dest_install = None

        # Active profiles
        self.active_origin_profile = None
        self.active_dest_profile = None

        self.character_names = None

    def add_installation_directory(self, directory):
        self.installations[directory.name] = directory

    def get_install(self, text):
        try:
            return self.installations[text]
        except KeyError:
            return None

    def get_origin_profile(self):
        try:
            return self.active_origin_install
        except KeyError:
            return None








