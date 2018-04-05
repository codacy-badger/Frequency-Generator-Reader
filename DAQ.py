"""
 **File Name:** DAQ .py                                                                                               \n
 **Project:** CURRENTLY UNNAMED                                                                                       \n
 **Company:** Research in Flows, Inc                                                                                  \n
 **Author:** David Gurevich                                                                                           \n
 **Copyright (c) 2018, David Gurevich. All rights reserved**                                                          \n
 **Required Modules:**
       * mcculw/ul.py                                                                                                 \n
       * mcculw/enums.py                                                                                              \n
       * hantekdds/htdds_wrapper.py                                                                                   \n

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""

import os
import sys
import time

from mcculw import ul
from mcculw.enums import ULRange

board_num = 1
channel = 0

SCAN_OPTIONS = {
    "BIP5VOLTS": ULRange.BIP5VOLTS,
    "BIP2VOLTS": ULRange.BIP2VOLTS,
    "BIP1VOLTS": ULRange.BIP1VOLTS,
    "BIP10VOLTS": ULRange.BIP10VOLTS
}


def progress(count, total, duration):
    """
    Print Progress bar and estimated time until completion.                                                           \n
    :param count: Current Number out of the Total to display (ex: 36 (out of 100))
    :type count: int
    :param total: The total that the count is out of.
    :type total: int
    :param duration: The duration (in milliseconds) that the process requires
    :type duration: int
    :return: None
    """
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    remaining_time = int(((total - count) * duration) / 250000)

    sys.stdout.write('[%s] %s%s ... %s seconds remaining %s\r' % (bar, percents, '%', remaining_time, ' '))
    sys.stdout.flush()


def scan(scan_option):
    """
    Execute "C_ScanA.exe", which produces the "Output.txt" file, with raw analog values.                             \n
    Open "output.txt", in read mode, and create a list (lines) which consists of each line of the file.              \n
    Convert each element of the list "lines" from str to int.                                                        \n
    Close the file, and eliminate the last element of the list, since it is empty, and will mess everything up.      \n
    Open a new file, "Final Output.txt" which will contain the converted values from analog to voltage.              \n
    Determine the amount of time it takes to convert one element from analog to voltage and store in
    variable "duration".                                                                                             \n
    For every element in the list "lines" (subtract 1) write the conversion of the analog value to voltage in the
    file "Final Output.txt", finally update the progress bar.                                                        \n
    Finally, close the file.                                                                                         \n

    :param scan_option: The MCCULW analog input range, for example BIP5VOLTS
    :type scan_option: str
    :return: None
    """
    os.system("C_ScanA.exe")

    f = open("output.txt", "r")
    lines = f.readlines()
    lines = [int(x) for x in lines]
    f.close()
    print("Successfully Read Output.txt File.\n")
    lines.pop()

    f_write = open("Final Output.txt", "w")

    start_time = int(round(time.time() * 1000))
    f_write.write(str((ul.to_eng_units(board_num, SCAN_OPTIONS[scan_option], int(lines[0])))))
    f_write.write("\n")
    duration = int(round(time.time() * 1000)) - start_time

    for x in range(len(lines) - 1):
        f_write.write(str((ul.to_eng_units(board_num, SCAN_OPTIONS[scan_option], int(lines[x])))))
        f_write.write("\n")
        progress(x, len(lines), duration)
    f_write.close()
    del lines
