"""
Module that stores the Data class for the profiles
"""
import re
import logging


class Server:
    """
    Class that the server discovered uses to hold all the information on the different servers.
    i.e. Singularity/Tranquility/Serenity
    """

    pretty = {
        "d_eve_sharedcache_sisi_singularity": "Singularity (Test)",
        "d_eve_sharedcache_tq_tranquility": "Tranquility (Live)",
        "d_eve_sharedcache_sr_serenity": "Serenity",
        "d_eve_sharedcache_du_duality": "Duality"
    }

    def __init__(self, name, path, profiles):
        self.name = name
        self.path = path
        self.profiles = profiles

    @property
    def pretty_name(self):
        try:
            return Server.pretty[self.name]
        except KeyError:
            return self.name

    def get_profile(self, text):
        """
        Returns the requested profile from the installation
        :param text: The profile text
        :return: A Profile
        """
        try:
            return self.profiles[text]
        except KeyError:
            return None

    def get_default(self):
        try:
            return self.get_profile('settings_Default')
        except KeyError:
            return self.profiles[0]

    def __str__(self):
        return self.pretty_name


class Profile:
    """
    Class that the profile discovered uses to hold all the information on the different profiles.
    i.e. Default
    """

    def __init__(self, path, name, accounts):
        self.path = path
        self.name = name
        self.accounts = accounts

    def __str__(self):
        return self.name


class Account:
    """
    Data object that contains all the information required for accounts/characters files.
    """

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

    def __str__(self):
        return self.name


