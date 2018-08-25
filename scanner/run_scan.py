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
import queue
from ctypes import CDLL

import scanner.hantekdds.htdds_wrapper as hantekdds
from scanner.scanner_thread import Scanner
from scanner.writer_thread import Writer


def test_daq():
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


def initialize(fq, amp):
    """
    Getting values and hardware ready for scanning.

    Removes and existing 'Output' folder. Makes a new one.
    Connects to Hantek 1025G function generator. Drives a sine wave.

    Returns:
        lib (ctypes.CDLL): see above
    """
    lib = CDLL('scanner/src/scan.dll')  # Load DLL file
    pathlib.Path('Output').mkdir(parents=True, exist_ok=True)  # Make the output path if it doesn't already exist
    for the_file in os.listdir('Output'):  # If the output folder already exists, delete all the files inside it
        file_path = os.path.join('Output', the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except OSError:
            print("Error deleting files")

    if not test_daq():
        return False

    function_generator = hantekdds.HantekDDS()
    if not function_generator.connect():  # Attempt a connection to the function generator
        print("There was an error connecting to the hantek 1025G generator module")
        return False

    function_generator.drive_periodic(frequency=float(fq), amplitude=float(amp))  # Drive a sine wave of frequency fq
    return lib


def run_scan(fq, amp, rate, dur, thread_count):
    crit_time_list = []

    try:
        lib = initialize(fq, amp)
        if not lib:
            return False

        time_collector = queue.Queue()
        threads = []
        for i in range(int(thread_count)):
            threads.append(Scanner(i, lib, rate, dur, time_collector))  # Scanner thread first
            threads[-1].setName("Scanner " + str(i))
            threads[-1].start()  # Start the scanner thread
            threads.append(Writer(threads[-1], i, lib))  # Writer thread with corresponding scanner thread
            threads[-1].setName("Writer " + str(i))
            threads[-1].start()  # Start writer thread

        for i in range(int(thread_count)):
            start_time, end_time = time_collector.get()
            crit_time_list.append(str(start_time))
            crit_time_list.append(str(end_time))
            time_collector.task_done()

        while True:
            if all(thread.complete for thread in threads):
                return True, crit_time_list

    except:
        return False, crit_time_list
