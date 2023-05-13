
import os
import eve_utils as utils
import data


class ServerDiscoverer:
    """
    This is the main class of the model builder mechanism.
    - Finds the installations in the EVE path
    """

    ignored_folder = ['Launcher', 'QtWebEngine', 'cache', 'Browser', 'LauncherCrashes', 'Installer']
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

            profiles = ProfileDiscoverer(folder, path).find_profiles()

            # Add the Server to the model
            server = data.Server(folder, path, profiles)
            self.model.add_server(server)

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


class ProfileDiscoverer:
    """
    Class the represents the different installations within the game.
    - Singularity/tranquility/serenity
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

    def find_profiles(self):
        profiles = {}

        for folder in os.listdir(self.path):
            path = os.path.join(self.path, folder)

            if os.path.isfile(path):
                continue  # Not a folder, we don't care here

            if self.is_folder_ignored(folder):
                continue  # Is ignored? Nothing to see here.

            print('  {}'.format(folder))

            chars = CharacterDiscoverer(path, folder).find_characters()
            profiles[folder] = data.Profile(path, folder, chars)

        return profiles

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


class CharacterDiscoverer:
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
        self.accounts = []  # TODO Refactor

    def find_characters(self):
        chars = []

        for file in os.listdir(self.path):
            path = os.path.join(self.path, file)

            if os.path.isdir(path):
                continue  # Not a file, we don't care here

            acc_file = data.Account(file, path)

            if acc_file.is_account:
                self.accounts.append(acc_file)

            if acc_file.is_character:
                self.shared_queue.put(acc_file.char_id)
                chars.append(acc_file)

            print('    {}'.format(file))

        return chars


class ApplicationModel:
    """
    Stores out data structures and keeps updated information on what is currently selected or active
    """

    def __init__(self):
        self.servers = {}

        # Active installations
        self.active_origin_server = None
        self.active_dest_server = None

        # Active profiles
        self.active_origin_profile = None
        self.active_dest_profile = None

        self.character_names = None

    def add_server(self, server):
        self.servers[server.name] = server

    def get_server(self, server):
        try:
            return self.servers[server]
        except KeyError:
            return self.get_default_server()

    def get_default_server(self):
        """
        Returns the first server that has the string 'tranquility' in it.
        :return:
        """
        server = [value for key, value in self.servers.items() if 'tranquility' in key.lower()][0]
        return server

