import os
import re
import subprocess
from logging import getLogger

logger = getLogger(__name__)

# Constants
KEY_TIME = '00'
KEY_DATE_VALUES = ('01', '04', '05', '09', '10', '14', '15', '19', '20', '24', '25', '28')
RSYNC_CMD_TEMPLATE = 'rsync -zvh --progress {src_file} {dst_path}'


def ensure_directory_exists(directory: str):
    """Ensure the destination directory exists."""
    if not os.path.exists(directory):
        logger.info(f'\n * Creating destination path: {directory} ...')
        os.makedirs(directory)
    else:
        logger.info(f'Destination path: {directory} - Exists')


def format_month(month: str) -> str:
    """Ensure the month has two digits."""
    _=str(month)
    return _.zfill(2)


def find_matching_files(src_dir: str, key_year: str, month: str) -> list[str]:
    """
    Summary:
    This function retrieves a list of file paths from a specified source directory
    that match a specific pattern based on key year, month, and predefined constant
    values defined in the global list `KEY_DATE_VALUES`. It uses `os.walk` to traverse
    the directory tree and attempts to match each file name against a constructed
    pattern using regular expressions. Upon a match, the full file path is added
    to the resulting list.

    Args:
        src_dir (str): The source directory path where the search for matching files
        is performed.
        key_year (str): The year to be included in the search pattern.
        month (str): The month to be included in the search pattern.

    Returns:
        list: A list of file paths that match the constructed pattern.
    """
    matching_files = []
    for dirpath, _, filenames in os.walk(src_dir):
        for filename in filenames:
            for special_key_date in KEY_DATE_VALUES:
                pattern = f'{key_year}{month}{special_key_date}{KEY_TIME}'
                if re.search(pattern, filename):
                    full_path = os.path.join(dirpath, filename)
                    logger.debug(f"Matched pattern: {pattern} with file: {filename}")
                    matching_files.append(full_path)
                    break  # Exit after finding a match for this file
    return matching_files


def run_command(command):
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout

    except subprocess.CalledProcessError as e:
        logger.error('Command failed: %s', e.stderr.strip() or e)
        return None


def execute_rsync(src_file: str, dst_dir: str, key_year: str, month: str):
    """
    Executes the rsync command to transfer files from a source location to a specified
    destination directory. It constructs the rsync command dynamically, logs the
    generated command for tracking, and executes it using the subprocess module.

    Parameters:
        src_file (str): The path to the source file to be transferred. Allows escaping
            characters that are problematic for shell commands, such as parentheses.
        dst_dir (str): The base directory of the destination where the file will
            be transferred.
        key_year (str): The year to structure subdirectories in the destination path.
        month (str): The month to structure subdirectories in the destination path.

    Returns:
        None
    """
    dst_path = os.path.join(str(dst_dir), str(key_year), str(month))
    cmd_args = ['rsync', '-zvh', '--progress', src_file, dst_path]

    logger.info('Running rsync: %s -> %s', src_file, dst_path)
    logger.debug('Rsync command: %s', cmd_args)

    output = run_command(cmd_args)

    if output:
        logger.debug('Rsync output:\n%s', output.strip())


def copy_date_month(month: str, src_dir: str, dst_dir: str, key_year: str):
    """
    Copy files matching specific patterns from the source directory to the destination directory.

    :param month: Month (two digits)
    :param src_dir: Source directory to scan for files
    :param dst_dir: Destination base directory
    :param key_year: Year to use in pattern matching
    """
    logger.debug(f'Month: {month}, Src Dir: {src_dir}, Dst Dir: {dst_dir}, Key Year: {key_year}')
    formatted_month = format_month(month)
    month_dst_dir = os.path.join(str(dst_dir), str(key_year), str(formatted_month))

    logger.info(f'Destination path is: {month_dst_dir}')
    ensure_directory_exists(month_dst_dir)

    logger.info(f'\n * Copying files from {src_dir} to {month_dst_dir}')
    matching_files = find_matching_files(src_dir, key_year, formatted_month)
    logger.info('Found %d matching file(s)', len(matching_files))

    if not matching_files:
        logger.warning('No files matched patterns for %s-%s in %s', key_year, formatted_month, src_dir)
        return

    for index, file in enumerate(matching_files, start=1):
        logger.debug('Copying file %d/%d: %s', index, len(matching_files), file)
        execute_rsync(file, dst_dir, key_year, formatted_month)

    logger.info('Finished copying %d file(s)', len(matching_files))