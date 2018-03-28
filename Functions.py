#############################################################
# File Name: Functions.py                                   #
# Project: CURRENTLY UNNAMED                                #
# Company: Research in Flows, Inc                           #
# Author: David Gurevich                                    #
# Copyright (c) 2018, David Gurevich. All rights reserved   #
# Required Modules:                                         #
#       DAQ.py                                              #
#       matplotlib                                          #
#############################################################

from matplotlib import pyplot as pl

import DAQ


def show_data(wave):
    pl.plot(wave)
    pl.show()


def get_input():
    while True:
        try:
            FREQUENCY = float(input("Input Frequency (Hz): \n-->"))
            break
        except:
            print("You did not enter a valid frequency!")

    while True:
        try:
            VOLTAGE = float(input("Input Voltage (V): \n-->"))
            break
        except:
            print("You did not enter a valid voltage")

    while True:
        try:
            SECONDS = float(input("How many seconds to run the scan?: \n-->"))
            break
        except:
            print("You did not enter a valid time")

    while True:
        try:
            SCAN_RATE = int(input("Input the Scan frequency (Hz): \n-->"))
            break
        except:
            print("You did not enter a valid frequency")

    while True:
        try:
            SCAN_OPTION = str(input("Input the Scan options (ex. BIP5VOLTS):\n-->"))
            if SCAN_OPTION in DAQ.SCAN_OPTIONS:
                break
            else:
                print("You did not enter a valid scan option.")
        except:
            print("You did not enter a valid scan option")

    return FREQUENCY, VOLTAGE, SECONDS, SCAN_RATE, SCAN_OPTION
