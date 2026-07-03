import argparse
import sys
import time
from logging import DEBUG, INFO, Formatter, StreamHandler, basicConfig, getLogger

import pyfiglet

import copy_files.copying_files
import envir.environment_dirs

# Constants
LOG_FORMAT = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
BANNER_TEXT = "BaCKuPER NG 4.11.0"
LOGGER_NAME = 'backuper'


def initialize_logging(debug: bool = False):
    """
    Configures console logging for the application and its modules.

    Parameters
    ----------
    debug : bool
        When True, sets the logging level to DEBUG for all propagated loggers.

    Returns
    -------
    Logger
        The main application logger instance.
    """
    level = DEBUG if debug else INFO
    console = StreamHandler(sys.stdout)
    console.setLevel(level)
    console.setFormatter(Formatter(LOG_FORMAT))

    basicConfig(level=level, format=LOG_FORMAT, handlers=[console], force=True)

    logger = getLogger(LOGGER_NAME)
    logger.setLevel(level)
    logger.debug('Debug logging enabled')
    return logger


def print_banner():
    """Prints the ASCII banner."""
    banner = pyfiglet.figlet_format(BANNER_TEXT)
    print(banner)


def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Parser for backup files")
    parser.add_argument("-y", "--year", help="Year to parse the directory", type=int, required=True)
    parser.add_argument("-m", "--month", help="Month to parse the directory (1-12)", type=int, required=True)
    parser.add_argument(
        "-d", "--debug",
        help="Debug mode: pass 1 to enable verbose logging",
        type=int,
        choices=[0, 1],
        default=0,
    )
    return parser.parse_args()


def validate_arguments(args, logger):
    """Validates parsed CLI arguments and logs the resolved configuration."""
    if not 1 <= args.month <= 12:
        logger.error('Invalid month: %s. Expected a value between 1 and 12.', args.month)
        raise ValueError(f'Month must be between 1 and 12, got {args.month}')

    if args.year < 1970:
        logger.error('Invalid year: %s. Expected a value of 1970 or later.', args.year)
        raise ValueError(f'Year must be 1970 or later, got {args.year}')

    logger.info('Backup period: year=%s, month=%02d', args.year, args.month)
    if args.debug:
        logger.debug('CLI arguments: year=%s, month=%s, debug=%s', args.year, args.month, args.debug)


if __name__ == '__main__':
    args = parse_arguments()
    logger = initialize_logging(debug=bool(args.debug))

    print_banner()

    logger.info('Service BACKUPER NG started')
    started_at = time.perf_counter()

    try:
        validate_arguments(args, logger)

        envir.environment_dirs.os_detect()

        source = envir.environment_dirs.get_source_path()
        destination = envir.environment_dirs.get_destination_path()
        logger.debug('Resolved paths: source=%s, destination=%s', source, destination)

        logger.info('Starting backup for %s-%02d', args.year, args.month)
        copy_files.copying_files.copy_date_month(args.month, source, destination, args.year)

        elapsed = time.perf_counter() - started_at
        logger.info('Service BACKUPER NG stopped successfully in %.2f s', elapsed)
    except Exception:
        elapsed = time.perf_counter() - started_at
        logger.exception('Service BACKUPER NG stopped with an error after %.2f s', elapsed)
        sys.exit(1)