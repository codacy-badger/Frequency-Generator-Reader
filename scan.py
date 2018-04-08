#!/usr/bin/env python

"""
 **File Name:** scan.py                                                       \n
 **Project** CURRENTLY UNNAMED                                                \n
 **Company:** Research in Flows, Inc                                          \n
 **Author:** David Gurevich                                                   \n
 **Required Modules:**
       * input_func.py                                                        \n
       * hantekdds/htdds_wrapper.py                                           \n

This work is licensed under the Creative Commons
Attribution-NonCommercial-NoDerivs 3.0 Unported License.
To view a copy of this license, visit
http://creativecommons.org/licenses/by-nc-nd/3.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""

import os
import sys
import pathlib

from input_func import show_data, get_input, SCAN_OPTIONS
from hantekdds import htdds_wrapper as hantek

if __name__ == '__main__':
    FUNCTION_GENERATOR = hantek.HantekDDS()
    if not FUNCTION_GENERATOR.connect():
        print("Failed to Connect to HantekDDS.")
        sys.exit()

    FREQUENCY, VOLTAGE, SECONDS, SCAN_RATE, SCAN_OPTION, GRAPH_OPTION = get_input()
    COUNT = SCAN_RATE * SECONDS
    FUNCTION_GENERATOR.drive_periodic(VOLTAGE, FREQUENCY)

    pathlib.Path('Output').mkdir(parents=True, exist_ok=True)
    FILE = open('Output/config.txt', 'w')
    FILE.write(str(COUNT) + "\n" + str(SCAN_RATE) + "\n" + str(int(SCAN_OPTIONS[SCAN_OPTION])))
    FILE.close()

    os.system("C_ScanA.exe")

    if GRAPH_OPTION:
        FILE = open("Output/voltage output.txt", "r")
        TO_GRAPH = [float(i) for i in FILE.readlines()]
        show_data(TO_GRAPH)

    sys.exit()
