import os


def get_appdata():
    """
    Returns the Local App Data where the EVE Online data resides.
    :return:
    """
    return os.getenv('LOCALAPPDATA')


def get_eve_path():
    """
    Returns the full eve path
    :return:
    """
    return '{}\\CCP\\EVE'.format(get_appdata())


def get_tranquility_path():
    """
    Returns the path where the tranquility data resides
    :return:
    """
    return os.path.join(get_appdata(), 'CCP\\EVE\\d_eve_sharedcache_tq_tranquility')


def get_singularity_path():
    """
    Returns the path where the singularity (test servers) data resides
    :return:
    """
    return os.path.join(get_appdata(), 'CCP\\EVE\\d_eve_sharedcache_sisi_singularity')


def get_working_directory():
    """
    Returns the working directory. Mostly to move the archive to eve path.
    :return:
    """
    return os.getcwd()

