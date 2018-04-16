"""
 **File Name:** input_func.py                                                                                         \n
 **Project:** CURRENTLY UNNAMED                                                                                       \n
 **Company:** Research in Flows, Inc                                                                                  \n
 **Author:** David Gurevich                                                                                           \n
 **Required Modules:**
       * matplotlib                                                                                                   \n
       * mcculw                                                                                                       \n

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""

from matplotlib import pyplot as pl

from mcculw.enums import ULRange

SCAN_OPTIONS = {
    "BIP5VOLTS": ULRange.BIP5VOLTS,
    "BIP2VOLTS": ULRange.BIP2VOLTS,
    "BIP1VOLTS": ULRange.BIP1VOLTS,
    "BIP10VOLTS": ULRange.BIP10VOLTS
}


def show_data(wave):
    """
    Use PyPlot from MatPlotLib to plot the wave, and then display it in a TKinter window.                             \n
    :param wave: List containing all voltage values of scanned wave.
    :type wave: list
    :return: None
    """
    pl.xlabel('Points')
    pl.ylabel('Voltage')
    pl.plot(wave)
    pl.savefig('Output/OutputPlot.png')
    pl.show()


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

    while True:
        try:
            grapher_input = str(
                input("Use MatLab to graph? (Y/N):\n-->")).lower()
            if grapher_input == "y":
                use_matlab = True
                break
            elif grapher_input == "n":
                use_matlab = False
                break
            else:
                print("You did not enter a valid input!")
        except ValueError:
            print("You did not enter a valid input!")

    # ADD ANY NEW INPUTS ABOVE THIS LINE
    return frequency, voltage, seconds, scan_rate, scan_option, graph_option, use_matlab
