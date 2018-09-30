"""
 **File Name:** run_scan.py                                                                          \n
 **Project:** CURRENTLY UNNAMED                                                                  \n
 **Company:** Research in Flows, Inc                                                             \n
 **Author:** David A. Gurevich                                                                   \n

Frequency-Generator Reader | Local software for generating and processing high-frequency signals
Copyright (C) 2018  David A. Gurevich
"""

import os
import pathlib
from ctypes import CDLL

import scanner.hantekdds.htdds_wrapper as hantekdds
from scanner.scanner_thread import Scanner
from scanner.writer_thread import Writer


def daq_connected():
    from mcculw import ul
    from mcculw.enums import ULRange
    from mcculw.ul import ULError

    board_num = 0
    channel = 0
    ai_range = ULRange.BIP5VOLTS

    try:
        ul.a_in(board_num, channel, ai_range)
        return True
    except ULError:
        return False


def function_generator_connected_and_initialize(fq, amp):
    function_generator = hantekdds.HantekDDS()
    if not function_generator.connect():
        return False
    else:
        function_generator.drive_periodic(frequency=float(fq), amplitude=float(amp))
        return True


def initialize(fq, amp):
    """
    Getting values and hardware ready for scanning.
    Test hardware to make sure it is there. Return any possible errors

    Removes and existing 'Output' folder. Makes a new one.
    Connects to Hantek 1025G function generator. Drives a sine wave.

    Returns:
        lib (ctypes.CDLL): see above
    """
    errors = []
    lib = False

    if os.path.exists('scanner/src/scan.dll'):
        lib = CDLL('scanner/src/scan.dll')  # Load DLL file
    else:
        errors.append("scan.dll file not found. Contact developer.")

    folder = 'Output/'
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            errors.append(e)

    if not daq_connected():
        errors.append("The Measurement Computing USB2020 module is not connected. Ensure that all drivers are "
                      + "installed and the USB is plugged in")

    if not function_generator_connected_and_initialize(fq, amp):
        errors.append("The Hantek 1025G function generator is not connected. Ensure that all drivers are installed "
                      + "and the USB is plugged in")

    return lib, errors


def run_scan(param_tup):
    fq, amp, rate, dur, thread_count = param_tup

    lib, errors = initialize(fq, amp)

    if errors:
        print("Scan could not be initialized due to existing errors. Errors: \n" + "\n".join(errors))
        return False, errors
    else:
        threads = []
        try:
            for i in range(int(thread_count)):
                threads.append(Scanner(i, lib, rate, dur))  # Scanner thread first
                threads[-1].setName("Scanner " + str(i))
                threads[-1].start()  # Start the scanner thread
                threads.append(Writer(threads[-1], i, lib))  # Writer thread with corresponding scanner thread
                threads[-1].setName("Writer " + str(i))
                threads[-1].start()  # Start writer thread
        except Exception as e:
            errors.append(e)
            return False, errors

        while True:
            if all(thread.complete for thread in threads):
                return True, errors
