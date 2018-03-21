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

        progress(i, window)

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


# def scan(wave, count):
#     for i in range(count):
#         try:
#             value = ul.a_in(board_num, channel, ai_range)
#             eng_units_value = ul.to_eng_units(board_num, ai_range, value)
#             wave.append(eng_units_value)
#         except ULError as e:
#             print("A UL error has occured. Code: ", str(e.errorcode), " Message: ", e.message)

def scan(wave):
    os.system("C_ScanA.exe")

    f = open("output.txt", "r")
    lines = f.readlines()
    f.close()

    f = open("output.txt", "w")
    f.writelines([item for item in lines[:-1]])
    f.close()

    f = open("output.txt", "r")
    for line in f.readlines():
        wave.append(ul.to_eng_units(board_num, ai_range, int(line)))
    f.close()
