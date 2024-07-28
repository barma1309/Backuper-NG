from datetime import datetime
import os
from logging import getLogger, basicConfig, DEBUG, ERROR, INFO, FileHandler, StreamHandler

logger = getLogger(__name__)

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

    logger.info(f'Destination path is:{month_dst_dir} \n')
    logger.info(f'* Checking destination path.... \n')

    if not os.path.exists(dst_dir):
        #print(f'\n * Creating destination path: {month_dst_dir} ...')
        logger.info(f'\n * Creating destination path: {month_dst_dir} ...')
        # os.mkdir(month_dst_dir)
    else:
        #print(f'\nDestination path: {month_dst_dir} - Exist')
        logger.info(f'Destination path: {month_dst_dir} - Exist')
    #print(f'* Preparing for copy files.... from {src_dir} to {month_dst_dir}')
    logger.info(f'\n * Copying files from {src_dir} to {month_dst_dir}')

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
                logger.debug(f"Comparing pattern: {text_look} with file: {filename}")
                pattern_filename = re.compile(text_look)
                # debug(pattern_filename)
                # print(pattern_filename)
                file_pattern = re.search(pattern_filename, filename)
                # debug(file_pattern)
                if file_pattern:
                    #print(f" Matched pattern {pattern_filename} with {filename}")
                    logger.debug(f" Matched pattern {pattern_filename} with {filename}")
                    # list_files_for_copy.append(filename)

                    # Move
                    # call_rsync_cmd = 'rsync -zvh --remove-source-files --progress '+ftp_dir+str(filename)+' '+str(long_storage)+str(key_year)+'/'+str(month)+'/'

                    # Copy
                    file_string_name1 = filename.replace("(", "\(")
                    file_string_name2 = file_string_name1.replace(")", "\)")
                    call_rsync_cmd = 'rsync -zvh --progress ' + ftp_dir + str(file_string_name2) + ' ' + str(
                        long_storage) + str(key_year) + '/' + str(month) + '/'
                    debug(call_rsync_cmd)

                    #                    subprocess.run(['bash', call_rsync_cmd], check = True)
                    subprocess.run([call_rsync_cmd], shell=True)