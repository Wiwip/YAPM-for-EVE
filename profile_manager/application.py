from queue import Queue

import data
from esi.esi_queries import AsyncCharacterQueries
from folder_browser import CharacterDiscoverer, ApplicationModel, ServerDiscoverer


class ProfileManager:
    """
    Class encompassing the whole application controller component.
    """

    def __init__(self):
        """

        """
        self.shared_queue = Queue()
        self.shared_dict = {}

        data.Account.names_dict = self.shared_dict
        CharacterDiscoverer.shared_queue = self.shared_queue

        # Creates the model shared by all the app to share relevant data.
        self.model = ApplicationModel()
        self.model.character_names = self.shared_dict

        # Creates the folder walker that will find relevant folders and files
        self.walker = ServerDiscoverer(self.model)
        self.walker.generate()

        # Starts the character names query
        self.char_name_svc = AsyncCharacterQueries(self.shared_queue, self.shared_dict)
        self.char_name_svc.start()

    def start(self):
        pass

    def quit(self):
        pass

    @property
    def character_names(self):
        return self.shared_dict

