####################################################
# File Name: Main.py                               #
# Project: CURRENTLY UNNAMED                       #
# Company: Research in Flows, Inc                  #
# Author: David Gurevich                           #
# Required Modules:                                #
#       DAQ.py                                     #
#       ShowData.py                                #
#       hantekdds/ htdds_wrapper.py                #
####################################################

import sys

import DAQ
from ShowData import show_data
from hantekdds import htdds_wrapper as hantek

# ---------------- FUNCTION GENERATOR ---------------

while True:
    try:
        FREQUENCY = float(input("Input Frequency (Hz): \n"))
        break
    except:
        print("You did not enter a valid frequency!")

while True:
    try:
        VOLTAGE = float(input("Input Voltage (V): \n"))
        break
    except:
        print("You did not enter a valid voltage")

while True:
    try:
        SECONDS = int(input("How many seconds to run the scan?: \n"))
        break
    except:
        print("You did not enter a valid time")

while True:
    try:
        SCAN_RATE = int(input("Input the Scan frequency (Hz): \n"))
        break
    except:
        print("You did not enter a valid frequency")

COUNT = SCAN_RATE * SECONDS

# ---------------- FUNCTION READER ------------------


if __name__ == '__main__':
    function_generator = hantek.HantekDDS()
    if not function_generator.connect():
        print("Failed to Connect to Hantek DDS.")
        sys.exit()
    function_generator.drive_periodic(VOLTAGE, FREQUENCY)

    f = open('config.txt', 'w')
    f.write(str(COUNT) + "\n" + str(SCAN_RATE))
    f.close()

    DAQ.scan()
    f = open("Final Output.txt", "r")
    to_graph = [float(i) for i in f.readlines()]
    show_data(to_graph)
    sys.exit()
