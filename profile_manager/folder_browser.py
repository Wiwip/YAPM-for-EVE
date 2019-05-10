import os


class EVEWalker:

    ignored_folder = ['Launcher', 'QtWebEngine', 'cache', 'Browser']
    appdata = os.getenv('LOCALAPPDATA')
    eve_path = '{}/CCP/EVE'.format(appdata)

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

    profiles_table = []
    ignored_folders = ['cache']

    def __init__(self, name, path):
        self.path = path
        self.name = name

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
            self.profiles_table.append(temp)

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

    @property
    def profiles(self):
        return self.profiles_table


class FolderProfiles:

    users = []
    accounts = []

    def __init__(self, path, name):
        self.path = path
        self.name = name

    def find_accounts(self):
        for folder in os.listdir(self.path):
            path = os.path.join(self.path, folder)

            if os.path.isdir(path):
                continue  # Not a file, we don't care here

            print('    {}'.format(folder))


class FolderModel:

    def __init__(self):
        self.installations = {}

    def add_installation_directory(self, directory):
        self.installations[directory.name] = directory

    def get_install(self, text):
        return self.installations[text]

    def get_profile(self, install):
        pass







