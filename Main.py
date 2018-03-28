#############################################################
# File Name: Main.py                                        #
# Project: CURRENTLY UNNAMED                                #
# Company: Research in Flows, Inc                           #
# Author: David Gurevich                                    #
# Copyright (c) 2018, David Gurevich. All rights reserved   #
# Required Modules:                                         #
#       DAQ.py                                              #
#       Functions.py                                        #
#       hantekdds/htdds_wrapper.py                          #
#############################################################

import sys

import DAQ
from Functions import show_data, get_input
from hantekdds import htdds_wrapper as hantek

FREQUENCY, VOLTAGE, SECONDS, SCAN_RATE, SCAN_OPTION = get_input()
COUNT = SCAN_RATE * SECONDS

if __name__ == '__main__':
    function_generator = hantek.HantekDDS()
    if not function_generator.connect():
        print("Failed to Connect to HantekDDS.")
        sys.exit()
    function_generator.drive_periodic(VOLTAGE, FREQUENCY)

    f = open('config.txt', 'w')
    f.write(str(COUNT) + "\n" + str(SCAN_RATE) + "\n" + str(int(DAQ.SCAN_OPTIONS[SCAN_OPTION])))
    f.close()

    DAQ.scan(SCAN_OPTION)
    f = open("Final Output.txt", "r")
    to_graph = [float(i) for i in f.readlines()]
    show_data(to_graph)
    sys.exit()
