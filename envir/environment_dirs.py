import os
from logging import getLogger, basicConfig, DEBUG, ERROR, INFO, FileHandler, StreamHandler

logger = getLogger(__name__)

def os_detect():
    print(f'Detected OS: {os.name}')

def path_source():
    ftp_dir = '/mnt/4_1c-ftp/'
    logger.info("Source path is %s", ftp_dir)
    return ftp_dir

def path_destination():
    long_storage = '/mnt/long_1c/'
    logger.info("Destination path is %s", long_storage)
    return long_storage



#if "__name__" == "__main__":
    # z = os.name
    # print(z)
    # print("Текущая директория:", os.getcwd())
    #
    # ftp_dir = '/mnt/4_1c-ftp/'
    # print(f"Path to source directory parsing is: {ftp_dir} ")
    # long_storage = '/mnt/long_1c/'
    # print(f"Path to destination directory is: {long_storage} ")
    # long_storage_date = '2022'

