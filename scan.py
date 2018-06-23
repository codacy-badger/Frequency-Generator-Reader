"""
 **File Name:** scan.py                                                                          \n
 **Project:** CURRENTLY UNNAMED                                                                  \n
 **Company:** Research in Flows, Inc                                                             \n
 **Author:** David A. Gurevich                                                                   \n
 **Required Modules:**                                                                           \n
       * numpy                                                                                   \n
       * HantekDDS                                                                               \n

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

from ctypes import c_int, c_double, POINTER, CDLL

import numpy as np
import hantekdds.htdds_wrapper as hantekdds


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
    def __init__(self, iteration, dll_lib):
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

        self.rate = 20000000  # 20 MHz per Channel
        self.c_rate = c_int(self.rate)

        self.dur = 0.05  # x number of seconds
        self.c_dur = c_double(self.dur)

        self.P = POINTER(c_int)()
        self.len = int(2 * self.dur * self.rate)
        self.iter = iteration

        self.scanned = False

    def run(self):
        """
        Scan and retrieve information from USB 2020 module.

        Tries to scan to an integer pointer at a predetermined rate and duration.
        When scanned, set scanned to True in order to indicate to WRITER thread
        that it can start writing.
        """
        try:
            self.lib.scan(self.P, self.c_rate, self.c_dur)
            self.scanned = True
        except Exception:
            print('Scan error')
            sys.exit(1)


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

    def run(self):
        """
        Write information retrieved from Scanner thread.

        Checks if scanner thread has completed scan. If it has,
        Tries to convert pointer to list. Then, pickles and dumps
        the list. Finally, releases the pointer.
        """
        while True:
            if self.scan_thread.scanned:
                try:
                    self.to_write = np.fromiter(self.scan_thread.P, dtype=np.int, count=self.scan_thread.len)
                except Exception:
                    print("There was an error converting the pointer (", self.scan_thread.P, ") to an interable")

                try:
                    pickle.dump(self.to_write, open("Output/output" + self.iter + ".bin", "wb"))
                except Exception:
                    print("There was an error dumping the data.")

                self.scan_thread.lib.release(self.scan_thread.P)
                break


def initialize():
    """
    Getting values and hardware ready for scanning.

    Removes and existing 'Output' folder. Makes a new one.
    Connects to Hantek 1025G function generator. Drives a sine wave.

    Attributes:
        lib (ctypes.CDLL): DLL file that contains scanning function.

    Returns:
        lib (ctypes.CDLL): see above
    """
    lib = CDLL('src/scan.dll')
    shutil.rmtree('Output')
    pathlib.Path('Output').mkdir(parents=True, exist_ok=True)

    function_generator = hantekdds.HantekDDS()
    if not function_generator.connect():
        print("There was an error connecting to the Hantek 1025G generator module")
        sys.exit(1)
    function_generator.drive_periodic(frequency=1.0)

    return lib


if __name__ == '__main__':
    lib = initialize()

    thread_count = 2
    threads = []
    for i in range(thread_count):
        threads.append(Scanner(i, lib))
        threads[-1].start()
        threads.append(Writer(threads[-1], i).start())

        scan_threads = threads[::2]
        for thread in scan_threads:
            thread.join()
