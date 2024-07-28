from logging import getLogger, basicConfig, DEBUG, ERROR, INFO, FileHandler, StreamHandler

import copy_files.copying_files
import pyfiglet  # Banner
import argparse  # arg parser
import envir.environment_dirs


#Dev

# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# -------------LOGGING ----------

logger = getLogger()
FORMAT = '%(asctime)s : %(name)s : %(levelname)s : %(message)s\n\r'
# file_handler = FileHandler('test.log')
# file_handler.setLevel(DEBUG)
console = StreamHandler()
console.setLevel(DEBUG)
basicConfig(level=DEBUG, format=FORMAT, handlers=[console])
# ------------------------------

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Logo Banner
    ascii_banner = pyfiglet.figlet_format("BaCKuPER NG 4.00")
    print(ascii_banner)
    logger.info("Service BACKUPER NG started ")

    envir.environment_dirs.os_detect()

    #--------------- parsing arguments ----------------------
    parser = argparse.ArgumentParser(description="Parser backup files")
    parser.add_argument("-y", dest="year_backup", help="date(year) which directory will parse", type=int, required=True)
    parser.add_argument("-m", dest="month", help="date(month) which directory will parse", type=int, required=True)
    parser.add_argument("-d", dest="debug", help="debug mode - input 1 for debug", type=int, required=False)
    args = parser.parse_args()
    #---------------- end parsing arguments -----------------



    copy_files.copying_files.copy_date_month(args.month, envir.environment_dirs.path_source(), envir.environment_dirs.path_destination(), args.year_backup)





    logger.info("Service BACKUPER NG stopped")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
