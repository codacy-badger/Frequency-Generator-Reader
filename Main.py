#!/usr/bin/env python

"""
 **File Name:** Main.py                                                                                               \n
 **Project** CURRENTLY UNNAMED                                                                                        \n
 **Company:** Research in Flows, Inc                                                                                  \n
 **Author:** David Gurevich                                                                                           \n
 **Required Modules:**
       * DAQ.py                                                                                                       \n
       * Functions.py                                                                                                 \n
       * hantekdds/htdds_wrapper.py                                                                                   \n

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""

import sys

import DAQ
from Functions import show_data, get_input
from hantekdds import htdds_wrapper as hantek

if __name__ == '__main__':
    function_generator = hantek.HantekDDS()
    if not function_generator.connect():
        print("Failed to Connect to HantekDDS.")
        sys.exit()

    FREQUENCY, VOLTAGE, SECONDS, SCAN_RATE, SCAN_OPTION = get_input()
    COUNT = SCAN_RATE * SECONDS
    function_generator.drive_periodic(VOLTAGE, FREQUENCY)

    f = open('config.txt', 'w')
    f.write(str(COUNT) + "\n" + str(SCAN_RATE) + "\n" + str(int(DAQ.SCAN_OPTIONS[SCAN_OPTION])))
    f.close()

    DAQ.scan(SCAN_OPTION)
    f = open("Final Output.txt", "r")
    to_graph = [float(i) for i in f.readlines()]
    show_data(to_graph)
    sys.exit()
