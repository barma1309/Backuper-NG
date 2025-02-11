import argparse
import os
import re
import subprocess
from datetime import datetime
import pyfiglet

# Constants
ASCII_BANNER = pyfiglet.figlet_format("BaCKuPER 1.01")
DEBUG_START = "################# START DEBUG OUTPUT ##################"
DEBUG_END = "################# END DEBUG OUTPUT ##################"
FTP_DIR = "/mnt/4_1c-ftp/"
LONG_STORAGE_DIR = "/mnt/long_1c/"
SCRIPT_VERSION = "1.00b"
KEY_TIME = "21"
KEY_DATES = ("01", "04", "05", "09", "10", "14", "15", "19", "20", "24", "25", "28")


def print_debug_message(message: str, debug_flag: int):
    """
    Print debug message if debug_flag is set to 1.
    """
    if debug_flag == 1:
        print(DEBUG_START)
        print(message)
        print(DEBUG_END)


def ensure_month_format(month: str) -> str:
    """
    Ensure the month is in two-digit format.
    """
    return month.zfill(2)


def ensure_directory_exists(directory: str):
    """
    Check if the directory exists, and create it if necessary.
    """
    if not os.path.exists(directory):
        print(f"\n * Creating destination path: {directory} ...")
        os.makedirs(directory)  # Create directories recursively if needed
    else:
        print(f"\nDestination path: {directory} - Exists")


def construct_rsync_command(ftp_dir: str, filename: str, long_storage: str, backup_year: str, month: str) -> str:
    """
    Construct the rsync command for copying files.
    """
    sanitized_filename = filename.replace("(", r"\(").replace(")", r"\)")  # Escape special characters
    return f'rsync -zvh --progress {ftp_dir}{sanitized_filename} {os.path.join(long_storage, backup_year, month)}/'


def copy_monthly_files(month: str, src_dir: str, dst_dir: str, year_backup: int, debug_flag: int):
    """
    Copy files matching specific patterns from a source directory to a destination directory.
    """
    print_debug_message("Starting copy_monthly_files function", debug_flag)

    # Ensure proper formatting of month and destination directory
    month = ensure_month_format(str(month))
    backup_year = str(year_backup)  # Format backup year as string
    destination_dir = os.path.join(dst_dir, backup_year, month)
    print(f"\n * Destination path is: {destination_dir}")
    print(f"\n * Checking destination path....")
    ensure_directory_exists(destination_dir)

    # Walk through source files to find matching patterns
    print(f"* Preparing to copy files from {src_dir} to {destination_dir}")
    for dirpath, _, filenames in os.walk(src_dir):
        for filename in filenames:
            for special_date in KEY_DATES:
                pattern_text = f"{backup_year}{month}{special_date}{KEY_TIME}"
                pattern_filename = re.compile(pattern_text)
                if re.search(pattern_filename, filename):
                    print(f"Matched pattern {pattern_filename} with {filename}")
                    rsync_command = construct_rsync_command(src_dir, filename, dst_dir, backup_year, month)
                    print(f"Executing: {rsync_command}")
                    subprocess.run([rsync_command], shell=True)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Parser backup files")
    parser.add_argument("-y", dest="year_backup", help="Year (e.g., 2022) which directory will parse", type=int,
                        required=True)
    parser.add_argument("-m", dest="month", help="Month (1-12) which directory will parse", type=int, required=True)
    parser.add_argument("-d", dest="debug", help="Debug mode - input 1 for debug", type=int, required=False, default=0)
    args = parser.parse_args()

    # Display ASCII banner and basic information
    print(ASCII_BANNER)
    print(f"Current directory: {os.getcwd()}")
    print(f"Path to source directory parsing is: {FTP_DIR}")
    print(f"Path to destination directory is: {LONG_STORAGE_DIR}")
    print(f"------ Version {SCRIPT_VERSION} -----")

    debug_flag = args.debug
    if debug_flag == 1:
        print_debug_message("Debug mode is ENABLED", 1)

    # Perform the file copying process
    copy_monthly_files(args.month, FTP_DIR, LONG_STORAGE_DIR, args.year_backup, debug_flag)

    print("FINISH...")
