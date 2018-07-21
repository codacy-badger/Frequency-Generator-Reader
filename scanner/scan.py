"""
 **File Name:** scan.py                                                                          \n
 **Project:** CURRENTLY UNNAMED                                                                  \n
 **Company:** Research in Flows, Inc                                                             \n
 **Author:** David A. Gurevich                                                                   \n

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

import pathlib
import pickle
import sys
import threading
import shutil
import os
import numpy as np

import scanner.hantekdds.htdds_wrapper as hantekdds

from ctypes import c_int, c_double, POINTER, CDLL


class Scanner(threading.Thread):
    """
    Thread responsible for retrieving information from USB-2020 Module.

    This class if a child class of the threading.Thread class. It is to be
    executed as a thread ( thread.start() .)

    Attributes:
        lib (ctypes.CDLL):           CTypes DLL file to use for scanning functions.
        lib.scan.argtypes (list):    Arguments that the scan function takes (from DLL.)
        lib.scan.restype  (list):    Return values of scan function (from DLL.)
        lib.release.argtypes (list): Arguments that the release function takes (from DLL.)
        lib.release.restype (list):  Return values of release function (from DLL.)
        rate (int):                  Scan rate.
        c_rate (c_int):              CTypes c_int version of rate.
        dur (float):                 Duration of scan in seconds.
        c_dur (c_double):            CTypes c_double version of dur.
        P (POINTER(c_int)):          List "retrieval" from scan function.
        len (int):                   Number of points to scan.
        iter (int):                  Number generated in for loop when designating threads.
        scanned (bool):              Indicator for Writer() thread when to dump information.
    """

    def __init__(self, iteration, dll_lib, rate, dur):
        """
        Initialization of Scanner thread.

        Args:
            iteration (int):       for loop iteration when generating thread. For identification purposes.
            dll_lib (ctypes.CDLL): CTypes DLL file to be used for scanning functions.

        """
        threading.Thread.__init__(self)
        self.lib = dll_lib

        # void scan(int** input, int rate, double dur) {}
        self.lib.scan.argtypes = [POINTER(POINTER(c_int)), c_int, c_double]
        self.lib.scan.restype = None

        # void release(int* input) {}
        self.lib.release.argtypes = [POINTER(c_int)]
        self.lib.release.restype = None

        self.rate = int(rate)           # Convert rate (float) to integer
        self.c_rate = c_int(self.rate)  # convert self.rate to C integer

        self.dur = dur
        self.c_dur = c_double(self.dur) # Convert duration to C double

        self.p = POINTER(c_int)()       # Generate integer pointer
        self.len = int(2 * self.rate * self.dur)
        self.iter = iteration           # Thread identifier

        self.complete = False           # Completion signal to check when data can be written

    def run(self):
        """
        Scan and retrieve information from USB 2020 module.

        Tries to scan to an integer pointer at a predetermined rate and duration.
        When scanned, set scanned to True in order to indicate to WRITER thread
        that it can start writing.
        """
        self.lib.scan(self.p, self.c_rate, self.c_dur)
        self.complete = True


class Writer(threading.Thread):
    """
    Thread responsible for writing information retrieved by scanner thread.

    Checks if scanner thread is finished scanning.
    If it is, convert the information (from pointer) into an iterable that Python
    understands. Then, pickle and dump the information. Finally, release the pointer.

    Attributes:
        iter (int):                    iter argument saved to corresponsing thread.
        to_write (list):               Iterable that the pointer will be converted into.
        scan_thread (Scanner() Class): scan_thread argument saved to corresponsing thread.
    """

    def __init__(self, scan_thread, iter):
        """
        Initialization of Writer thread.

        Args:
            scan_thread (Scanner() Class):The writer's corresponding scan thread that it reports to.
            iter (int):                    Iteration of for loop that generates the thread.
        """
        threading.Thread.__init__(self)
        self.iter = str(iter)
        self.to_write = []
        self.scan_thread = scan_thread
        self.complete = False

    def run(self):
        """
        Write information retrieved from Scanner thread.

        Checks if scanner thread has completed scan. If it has,
        Tries to convert pointer to list. Then, pickles and dumps
        the list. Finally, releases the pointer.
        """
        while True:
            if self.scan_thread.complete:       # Check if scanner thread is complete
                try:
                    self.to_write = np.fromiter( # Generate numpy iterable from integer pointer
                        self.scan_thread.p, dtype=np.int, count=self.scan_thread.len)
                except Exception:
                    print("There was an error convertering the pointer(",
                          self.scan_thread.p, ") to an iterable")
                    sys.exit(1)

                try:
                    pickle.dump(self.to_write, open( # Dump the data to a bin file
                        "Output/output" + self.iter + ".bin", "wb"))
                except Exception:
                    print("There was an error dumping the data")

                self.scan_thread.lib.release(self.scan_thread.p) # Release the thread when done
                self.complete = True
                break


def initialize(fq):
    """
    Getting values and hardware ready for scanning.

    Removes and existing 'Output' folder. Makes a new one.
    Connects to Hantek 1025G function generator. Drives a sine wave.

    Attributes:
        lib (ctypes.CDLL): DLL file that contains scanning function.

    Returns:
        lib (ctypes.CDLL): see above
    """
    lib = CDLL('scanner/src/scan.dll')  # Load DLL file
    pathlib.Path('Output').mkdir(parents=True, exist_ok=True) # Make the output path if it doesn't already exist
    for the_file in os.listdir('Output'): # If the output folder alreaady exists, delete all the files inside it
        file_path = os.path.join('Output', the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception:
            print("Error deleting files")

    function_generator = hantekdds.HantekDDS()
    if not function_generator.connect(): # Attempt a connection to the function generator
        print("There was an error connecting to the hantek 1025G generator module")
        sys.exit(1)

    function_generator.drive_periodic(frequency=float(fq)) # Drive a sine wave of frequency fq
    return lib


def run_scan(fq, rate, dur, thread_count):
    lib = initialize(fq)

    threads = []
    for i in range(int(thread_count)):
        threads.append(Scanner(i, lib, rate, dur)) # Scanner thread first
        threads[-1].start()                        # Start the scanner thread
        threads.append(Writer(threads[-1], i))     # Writer thread with corresponding scanner thread
        threads[-1].start()                        # Start writer thread

        scan_threads = threads[::2]
        for thread in scan_threads:
            thread.join()

    while True:
        if all(thread.complete for thread in threads):
            return True
            break

    if __name__ == '__main__':
        run_scan(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
