####################################################
# File Name: DAQ.py                                #
# Project: CURRENTLY UNNAMED                       #
# Company: Research in Flows, Inc                  #
# Author: David Gurevich                           #
# Required Modules:                                #
#       mcculw                                     #
#       numpy                                      #
####################################################

import os
import sys

import numpy
from mcculw import ul
from mcculw.enums import ULRange

board_num = 1
channel = 0
ai_range = ULRange.BIP2VOLTS


def smoothListGaussian(list, degree=5):
    window = degree * 2 - 1

    weight = numpy.array([1.0] * window)

    weightGauss = []

    for i in range(window):
        i = i - degree + 1

        frac = i / float(window)

        gauss = 1 / (numpy.exp((4 * (frac)) ** 2))

        weightGauss.append(gauss)

    weight = numpy.array(weightGauss) * weight

    smoothed = [0.0] * (len(list) - window)

    for i in range(len(smoothed)):
        smoothed[i] = sum(numpy.array(list[i:i + window]) * weight) / sum(weight)

    return smoothed


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


def scan():
    os.system("C_ScanA.exe")

    f = open("output.txt", "r")
    lines = f.readlines()
    lines = [int(x) for x in lines]
    f.close()
    print("Successfully Read Output.txt File.\n")

    lines.pop()
    # IF YOU WOULD LIKE TO SMOOTH THE DATA, UNCOMMENT THE FOLLOWING LINE
    # lines = smoothListGaussian(lines, 10)

    f_write = open("Final Output.txt", "w")
    for x in range(len(lines)):
        f_write.write(str((ul.to_eng_units(board_num, ai_range, int(lines[x])))))
        f_write.write("\n")
        progress(x, len(lines))
    f_write.close()
