"""
 **File Name:** input_func.py                                                                                         \n
 **Project:** CURRENTLY UNNAMED                                                                                       \n
 **Company:** Research in Flows, Inc                                                                                  \n
 **Author:** David Gurevich                                                                                           \n
 **Required Modules:**
       * mcculw                                                                                                       \n

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""

from mcculw.enums import ULRange

SCAN_OPTIONS = { # THIS IS FOR THE USB2020 MODULE
    "BIP5VOLTS": ULRange.BIP5VOLTS,
    "BIP2VOLTS": ULRange.BIP2VOLTS,
    "BIP1VOLTS": ULRange.BIP1VOLTS,
    "BIP10VOLTS": ULRange.BIP10VOLTS
}


def get_input():
    """
    Prompts the user with multiple messages, each to enter a certain element of information, each prompt is
    "idiot proof" (Hopefully).                                                                                        \n

    :FREQUENCY: The frequency the generator should generate the function at.
    :VOLTAGE: The voltage the generator should generate the function at.
    :SECONDS: How long to scan the wave for (in seconds).
    :SCAN_RATE: The frequency the DAQ should probe the analog value of the input at.
    :SCAN_OPTION: The MCCULW range used to determine the expected range of the analog input. (ex: BIP5VOLTS)

    :return: FREQUENCY, VOLTAGE, SECONDS, SCAN_RATE, SCAN_OPTION
    :rtype: tuple
    """

    frequency = 0
    voltage = 0

    while True:
        try:
            gen_fq = str(
                input("Use this program to generate frequency? (Y/N):\n-->")).lower()
            if gen_fq == "y":
                gen_fq_bool = True
                break
            elif gen_fq == "n":
                gen_fq_bool = False
                break
            else:
                print("You did not enter a valid input!")
        except ValueError:
            print("You did not enter a valid input!")
    if gen_fq_bool:
        while True:
            try:
                frequency = float(input("Input Frequency (Hz): \n-->"))
                break
            except ValueError:
                print("You did not enter a valid frequency!")

        while True:
            try:
                voltage = float(input("Input Voltage (V): \n-->"))
                break
            except ValueError:
                print("You did not enter a valid voltage")

    while True:
        try:
            seconds = float(input("How many seconds to run the scan?: \n-->"))
            break
        except ValueError:
            print("You did not enter a valid time")

    while True:
        try:
            scan_rate = int(input("Input the Scan frequency (Hz): \n-->"))
            break
        except ValueError:
            print("You did not enter a valid frequency")

    while True:
        try:
            scan_option = str(
                input("Input the Scan options (ex. BIP5VOLTS):\n-->"))
            if scan_option in SCAN_OPTIONS:
                break
            else:
                print("You did not enter a valid scan option.")
        except ValueError:
            print("You did not enter a valid scan option")

    while True:
        try:
            graph_option_input = str(
                input("Graph result? (Y/N):\n-->")).lower()
            if graph_option_input == "y":
                graph_option = True
                break
            elif graph_option_input == "n":
                graph_option = False
                break
            else:
                print("You did not enter a valid input!")
        except ValueError:
            print("You did not enter a valid input!")


    # ADD ANY NEW INPUTS ABOVE THIS LINE
    return gen_fq_bool, frequency, voltage, seconds, scan_rate, scan_option, graph_option
