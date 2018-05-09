"""
 **File Name:** input_func.py                                                                                         \n
 **Project:** CURRENTLY UNNAMED                                                                                       \n
 **Company:** Research in Flows, Inc                                                                                  \n
 **Author:** David Gurevich                                                                                           \n
 **Required Modules:**
       * mcculw                                                                                                       \n

Frequency-Generator Reader | Local software for generating and processing high-frequency signals
Copyright (C) 2018  David A. Gurevich

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
            if scan_option.upper() in SCAN_OPTIONS:
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
