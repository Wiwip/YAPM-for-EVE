
import os
import logging
import shutil
import eve_utils


def backup_eve_information(name, extension='zip'):
    """

    :param extension:
    :param name:
    :return:
    """

    try:
        logging.info("Archive operation started: {}".format(name))
        shutil.make_archive(name, extension, root_dir=eve_utils.get_tranquility_path())
        src_filename = os.path.join(eve_utils.get_working_directory(), '{}.{}'.format(name, extension))
        dst_filename = os.path.join(eve_utils.get_eve_path(), '{}.{}'.format(name, extension))

        logging.info("File [{}] was copied to destination [{}]".format(src_filename, dst_filename))

        shutil.move(src_filename, dst_filename)
        logging.info("Archive operation completed.")
    except FileNotFoundError:
        logging.warning("File not found error occurred.", exc_info=True)


def restore_eve_information(name, extension='zip'):
    """

    :return:
    """
    logging.info("Restore operation started: {}".format(name))
    shutil.rmtree(eve_utils.get_tranquility_path(), ignore_errors=True)

    try:
        os.mkdir(eve_utils.get_tranquility_path())
        logging.info("Created tranquility folder.")
    except FileExistsError:
        pass  # Folder exits, expected behaviour.

    filename = os.path.join(eve_utils.get_eve_path(), '{}.{}'.format(name, extension))

    logging.info("Unpacking archive")
    shutil.unpack_archive(filename, eve_utils.get_tranquility_path())

    logging.info("Archive operation completed")
