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
        print("You did not enter a vslid time")

while True:
    try:
        SCAN_RATE = int(input("Input the Scan frequency (Hz): \n"))
        break
    except:
        print("You did not enter a valid frequency")

while True:
    try:
        SMOOTH_BOOL = str(input("Smooth output? (True/False): \n")).lower()
        if SMOOTH_BOOL == "true" or "t":
            SMOOTH_BOOL = True
            break
    except:
        print("You did not enter a valid input.")

if SMOOTH_BOOL:
    SMOOTH_DEGREE = int(input("To what degree should the output be smoothed?: \n"))

COUNT = SCAN_RATE * SECONDS

# ---------------- FUNCTION READER ------------------

WAVE = []

if __name__ == '__main__':
    try:
        function_generator = hantek.HantekDDS()
        if not function_generator.connect():
            print("Failed to Connect to Hantek DDS.")
            sys.exit()
        function_generator.drive_periodic(VOLTAGE, FREQUENCY)

        f = open('config.txt', 'w')
        f.write(str(COUNT) + "\n" + str(SCAN_RATE))
        f.close()

        DAQ.scan(WAVE)

        if SMOOTH_BOOL:
            WAVE = DAQ.smoothListGaussian(WAVE, SMOOTH_DEGREE)

        f = open('Final_Output.txt', 'w')
        for element in WAVE:
            f.write(str(element))
            f.write("\n")
        f.close()
        show_data(WAVE)
        sys.exit()

    except:
        print("Program Failed!")
        sys.exit()
