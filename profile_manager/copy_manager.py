"""Util functions to manage user

"""

import os
import shutil


def copy_file(source_file, destination_file):
    """

    :return:
    """
    shutil.copyfile(source_file, destination_file, follow_symlinks=False)


def copy_files(source_file, destination_files):
    """
    Wrapper function allowing multiple destination files to be used at once.
    :return: None
    """
    for file in destination_files:
        copy_file(source_file, file)


