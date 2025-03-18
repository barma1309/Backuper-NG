import argparse
from logging import getLogger, basicConfig, INFO, StreamHandler
import pyfiglet
import copy_files.copying_files
import envir.environment_dirs

# Constants
LOG_FORMAT = '%(asctime)s : %(name)s : %(levelname)s : %(message)s\n\r'
BANNER_TEXT = "BaCKuPER NG 4.11.0"


def initialize_logging():
    """
    Initializes and configures the logging framework for console output.

    This function sets up a basic logger with a stream handler configured
    to output logging messages to the console. The logging level and
    message format are configured as specified in the function.

    Returns
    -------
    Logger
        An instance of the configured logger.
    """
    logger = getLogger()
    console = StreamHandler()
    console.setLevel(INFO)
    basicConfig(level=INFO, format=LOG_FORMAT, handlers=[console])
    return logger


def print_banner():
    """Prints the ASCII banner."""
    banner = pyfiglet.figlet_format(BANNER_TEXT)
    print(banner)


def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Parser for backup files")
    parser.add_argument("-y", "--year", help="Year to parse the directory", type=int, required=True)
    parser.add_argument("-m", "--month", help="Month to parse the directory", type=int, required=True)
    parser.add_argument("-d", "--debug", help="Debug mode - input 1 for debug", type=int, required=False)
    return parser.parse_args()


if __name__ == '__main__':
    # Initialize logging and logger
    logger = initialize_logging()

    # Print banner
    print_banner()

    logger.info("Service BACKUPER NG started")

    # Detect OS environment
    envir.environment_dirs.os_detect()

    # Parse arguments
    args = parse_arguments()

    # Execute file copying
    source = envir.environment_dirs.get_source_path()
    destination = envir.environment_dirs.get_destination_path()
    copy_files.copying_files.copy_date_month(args.month, source, destination, args.year)

    logger.info("Service BACKUPER NG stopped")
