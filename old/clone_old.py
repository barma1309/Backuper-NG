# Backup NAS
import argparse  # arg parser
import os
import re
import subprocess
from datetime import datetime

import pyfiglet  # Banner

# from shlex import quote

if "__name__" == "__main__":

    parser = argparse.ArgumentParser(description="Parser backup files")
    parser.add_argument("-y", dest="year_backup", help="date(year) which directory will parse",
                        type=int, required=True)
    parser.add_argument("-m", dest="month", help="date(month) which directory will parse", type=int,
                        required=True)
    parser.add_argument("-d", dest="debug", help="debug mode - input 1 for debug", type=int,
                        required=False)
    # parser.add_argument("-delete", dest="", help="delete files from source directory", type=str,
    # required=False)
    args = parser.parse_args()
    # print(args.debug)

    # Logo Banner
    ascii_banner = pyfiglet.figlet_format("BaCKuPER 1.01")
    print(ascii_banner)

    z = os.name
    # print(z)
    print("Текущая директория:", os.getcwd())

    ftp_dir = '/mnt/4_1c-ftp/'
    print(f"Path to source directory parsing is: {ftp_dir} ")
    long_storage = '/mnt/long_1c/'
    print(f"Path to destination directory is: {long_storage} ")
    long_storage_date = '2022'

    version_script = '1.00b'
    print(f'------ Version {version_script}-----')


    # DEBUG MODE
    def debug(arg_4_print):
        # Printing variable
        if args.debug == 1:
            print('################# START DEBUG OUTPUT ##################')
            print(arg_4_print)
            print('################# END DEBUG OUTPUT ##################')
        else:
            pass

    if args.debug == 1:
        debug("----------------- DEBUG MODE ENABLED-----------------------")
    else:
        pass

    # Copying all files at special month with regular expression
    def copy_date_month(month: str, src_dir: str, dst_dir: str, year_backup: datetime):
        """

        :rtype: object
        :param month:
        :param src_dir:
        :param dst_dir:
        :param year_backup:
        """
        list_files_for_copy = []
        key_year = year_backup
        key_time = '21'
        key_date = ('01', '04', '05', '09', 10, 14, 15, 19, 20, 24, 25, 28)

        if int(month) < 10:
            month = "0" + str(month)

        month_dst_dir = dst_dir + str(key_year) + '/' + str(month)
        print(f'\n * Destination path is:{month_dst_dir}')
        print(f'\n * Checking destination path....')
        if not os.path.exists(dst_dir):
            print(f'\n * Creating destination path: {month_dst_dir} ...')
            # os.mkdir(month_dst_dir)
        else:
            print(f'\nDestination path: {month_dst_dir} - Exist')
        print(f'* Preparing for copy files.... from {src_dir} to {month_dst_dir}')
        # Forming list files witch should be copy
        # распечатать все файлы и папки рекурсивно

        for dirpath, dirnames, filenames in os.walk(src_dir):
            for filename in filenames:
                # print("Файл:", os.path.join(dirpath, filename))
                # text_look = f'{str(key_year)+str(month)+str(key_date)+str(key_time)}'
                # debug()

                for special_key_date in key_date:
                    text_look = f'{str(key_year) + str(month) + str(special_key_date) + str(key_time)}'
                    # debug(text_look)
                    # print(f'Comparing pattern: {text_look} with file: {filename}')
                    pattern_filename = re.compile(text_look)
                    # debug(pattern_filename)
                    # print(pattern_filename)
                    file_pattern = re.search(pattern_filename, filename)
                    # debug(file_pattern)
                    if file_pattern:
                        print(f" Matched pattern {pattern_filename} with {filename}")
                        # list_files_for_copy.append(filename)

                        # Move
                        # call_rsync_cmd = 'rsync -zvh --remove-source-files --progress '+ftp_dir+str(filename)+' '+str(long_storage)+str(key_year)+'/'+str(month)+'/'

                        # Copy
                        file_string_name1 = filename.replace("(","\(")
                        file_string_name2 = file_string_name1.replace(")","\)")
                        call_rsync_cmd = 'rsync -zvh --progress ' + ftp_dir + str(file_string_name2) + ' ' + str(long_storage) + str(key_year) + '/' + str(month) + '/'
                        debug(call_rsync_cmd)

                        #                    subprocess.run(['bash', call_rsync_cmd], check = True)
                        subprocess.run([call_rsync_cmd], shell=True)

                        # os.system(call_rsync_cmd)
        # print(f' List of files matched for copying {list_files_for_copy}')


    # print('\nDo - Call copy_data_month')
    copy_date_month(args.month, ftp_dir, long_storage, args.year_backup)
    print("FINISH...")
