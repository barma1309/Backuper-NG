import os
from logging import getLogger

# Constants for directory paths
SOURCE_DIR = '/bigZbackup/4_1c-ftp/'
DESTINATION_DIR = '/mnt/long_1c/'

# Logger instance
logger = getLogger(__name__)


def os_detect():
    """Logs the detected operating system."""
    logger.info('Detected OS: %s', os.name)


def log_path(description, path):
    """Logs a description of a path consistently."""
    logger.info("%s path is %s", description, path)


def get_source_path():
    """Returns and logs the source directory path."""
    log_path("Source", SOURCE_DIR)
    return SOURCE_DIR


def get_destination_path():
    """Returns and logs the destination directory path."""
    log_path("Destination", DESTINATION_DIR)
    return DESTINATION_DIR
