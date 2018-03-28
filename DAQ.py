#############################################################
# File Name: DAQ.py                                         #
# Project: CURRENTLY UNNAMED                                #
# Company: Research in Flows, Inc                           #
# Author: David Gurevich                                    #
# Copyright (c) 2018, David Gurevich. All rights reserved   #
# Required Modules:                                         #
#       mcculw                                              #
#############################################################

import os
import sys

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


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


def scan(scan_option):
    os.system("C_ScanA.exe")

    f = open("output.txt", "r")
    lines = f.readlines()
    lines = [int(x) for x in lines]
    f.close()
    print("Successfully Read Output.txt File.\n")
    lines.pop()

    f_write = open("Final Output.txt", "w")
    for x in range(len(lines)):
        f_write.write(str((ul.to_eng_units(board_num, SCAN_OPTIONS[scan_option], int(lines[x])))))
        f_write.write("\n")
        progress(x, len(lines))
    f_write.close()
